import requests
import re
from bs4 import BeautifulSoup


def off():
    url1 = "https://www.hyperia.sk/kariera"
    response = requests.get(url1)
    soup = BeautifulSoup(response.text, "html.parser")

    one_div = soup.find_all("div", class_="job")[0]
    print(one_div, '\n')
    print(type(one_div), '\n')

    print(one_div.a.find_all("div", class_="job_box_1")[0], '\n')
    job_box = one_div.a.find_all("div", class_="job_box_1")[0].string

    print(type(job_box))
    job_box = re.split('[<|>]', job_box)[0].strip()
    print(job_box)


class WebPage:
    def __init__(self, url):
        self.url = url
        self.html = requests.get(self.url)
        self.soup = BeautifulSoup(self.html.text, "html.parser")
        self.jobs = []

    def add_job_data(self):
        job_divs = self.soup.find_all("div", class_="job")
        for job_div in job_divs:
            job = Job()
            detail_url = job_div

class Job:
    def __init__(self):
        self.title = None
        self.city = None
        self.date = None
        self.city = None


start_site = WebPage("https://www.hyperia.sk/kariera")
