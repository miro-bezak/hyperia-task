"""Simple programme to parse out information about job opportunities at the
Hyperia company."""
import json
import re
import requests
from bs4 import BeautifulSoup


class WebPage:
    """Class to store the mark-up and BeautifulSoup of a single web page."""

    def __init__(self, url):
        self.url = url
        self.html = requests.get(self.url)
        self.soup = BeautifulSoup(self.html.text, "html.parser")
        self.data = {}

    def add_job_data(self):
        """Scrape the Hyperia website and put the information about jobs
        into the `data` dictionary."""
        print("Adding job data...")
        job_divs = self.soup.find_all("div", class_="job")
        self.data['jobs'] = []

        for job_div in job_divs:
            detail_url = job_div.a.attrs['href']
            detail = WebPage("https://www.hyperia.sk/" + detail_url)
            site = re.sub("(<!--.*?-->)", "", detail.html.text,
                          flags=re.DOTALL)
            job_email = re.findall(r"[a-z0-9\.\-+_]+@hyperia.sk",
                                   site, re.I)
            job_email = "NULL" if not job_email else job_email[0]

            job_title = self.find_div_class(job_div, "job_box_1")
            job_city = self.find_div_class(job_div, "job_city")
            job_date = self.find_div_class(job_div, "job_date")

            self.data['jobs'].append({
                "title": job_title,
                "city": job_city,
                "date": job_date,
                "contact-email": job_email
            })
        print("Job data successfully added.")

    @staticmethod
    def find_div_class(job_div, class_name):
        """Search for the class in the given div."""
        inner_div = job_div.a.find_all("div", class_=class_name)[0].string
        return re.split('[<|>]', inner_div)[0].strip()

    def output_json(self):
        """Output the job data into a json file."""
        with open("job_opportunities.json", "w") as outfile:
            json.dump(self.data, outfile)
        print("JSON output finished.")


# ---------- DRIVER PROGRAMME ----------
print("Hyperia Web scraper started.")
HYPERIA_JOBS = WebPage("https://www.hyperia.sk/kariera")

HYPERIA_JOBS.add_job_data()
HYPERIA_JOBS.output_json()
print("Script successfully finished.")
