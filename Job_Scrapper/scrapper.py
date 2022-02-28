import requests
from bs4 import BeautifulSoup

  # 사이트가 다 이상해요..

def get_stackoverflow(word):
  site = "https://stackoverflow.com"
  addr = f"{site}/jobs?q={word}&r=true"
  r = requests.get(addr)
  soup = BeautifulSoup(r.text, 'html.parser')
  # /jobs?q=python&amp;r=true&amp;so_source=JobSearch&amp;so_medium=Internal&amp;pg=8 # 왜 이럴까..
  jobs = []
  listResults = soup.find("div", {"class":"listResults"}).find_all("div",{"class":"-job"})
  for result in listResults:
    title = result.find("div",{"class":"fl1"}).find("h2").find("a")['title']
    link = site + result.find("div",{"class":"fl1"}).find("h2").find("a")['href']
    company = result.find("div",{"class":"fl1"}).find("h3").find("span").get_text().strip()
    location = result.find("div",{"class":"fl1"}).find("h3").find("span",{"class":"fc-black-500"}).get_text().strip()
    jobs.append([title, company, location, link])
  return jobs

def get_weworkremotely(word):
  site = "https://weworkremotely.com"
  addr = f"{site}/remote-jobs/search?term={word}"
  r = requests.get(addr)
  soup = BeautifulSoup(r.text, 'html.parser')
  jobs = []
  categorys = ("category-2", "category-18", "category-4")
  for category in categorys:
    listResults = soup.find("div", {"id":"job_list"}).find("section", {"id":category}).find("article").find("ul").find_all("li")
    for result in listResults[:-1]:
      title = result.find("span", {"class":"title"}).get_text()
      company = result.find("span", {"class":"company"}).get_text()
      location = result.find("span", {"class":"region"}).get_text()
      link = site + result.select('a')[1]["href"]
      jobs.append([title, company, location, link])
  return jobs

def get_remoteok(word):
  site = "https://remoteok.com"
  addr = f"{site}/remote-{word}-jobs"
  r = requests.get(addr)
  soup = BeautifulSoup(r.text, 'html.parser')
  # 503 Service Temporarily Unavailable
  jobs = []
  return jobs

def get_jobs(word):

  stackoverflow_job = get_stackoverflow(word)
  # return stackoverflow_job # fot unit testing
  weworkremotely_job = get_weworkremotely(word)
  # return weworkremotely_job # fot unit testing
  remoteok_job = get_remoteok(word)
  # return remoteok_job # fot unit testing

  jobs = stackoverflow_job + weworkremotely_job + remoteok_job
  
  return jobs