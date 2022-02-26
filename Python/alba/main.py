from math import ceil
import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"

r = requests.get(alba_url)
soup = BeautifulSoup(r.text, 'html.parser')

def goods_url(goods_data):
  superbrand = goods_data.find("div", {"id":"MainSuperBrand"})
  goods_box = superbrand.find("ul", {"class":"goodsBox"})
  goods_li = goods_box.find_all("li", {"class":"impact"})
  goods_impact = []
  for good in goods_li:
    good_company = good.find("span", {"class":"company"}).string
    good_info = [[good.find("a")["href"]],good_company]
    goods_impact.append(good_info)
  return goods_impact

def job_paging(brand, brand_name):
  # print(brand)
  # print(brand_name)
  
  g = requests.get(brand)
  soup = BeautifulSoup(g.text, 'html.parser')

  if soup.find("p", {"class":"jobCount"}).find('strong') is None:
    job_count = soup.find("p", {"class":"listCount"}).find('strong').string
  else:
    job_count = soup.find("p", {"class":"jobCount"}).find('strong').string
  # print(job_count)
  max_page = ceil(int(job_count.replace(',',''))/50)

  file = open(f'{brand_name}.cvs', 'w')
  writer = csv.writer(file)
  writer.writerow(["place","title", "time", "pay", "date"])
  
  for page in range(max_page):
    url = brand  + f'job/brand/?page={page+1}&pagesize=50'
    g = requests.get(url)
    soup = BeautifulSoup(g.text, 'html.parser')
    jobs_list = soup.find("div", {"id":"NormalInfo"}).find("tbody").find_all("tr")
    for job in (jobs_list):
      if(job.find("td", {"class":"local"}) != None):
        place = job.find("td", {"class":"local"}).get_text()
        title = job.find("span", {"class":"company"}).string.strip()
        # print(job.find("span", {"class":"title"}).string)
        time = job.find("td", {"class":"data"}).get_text()
        pay = job.find("td", {"class":"pay"}).get_text()
        date = job.find("td", {"class":"regDate"}).get_text()
        print(place, title, time, pay, date)
        writer.writerow([place, title, time, pay, date])
  file.close()

brand = goods_url(soup)
for one_brand in brand:
  job_paging(one_brand[0][0], one_brand[1])
