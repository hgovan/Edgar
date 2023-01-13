import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date



def request(url: str):
    '''
    error handle for requests to the edgar database
    :param url: you guessed it the url for the specific query
    rtype: if connected returns requests class else an empty string
    '''
    header = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
    "(KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36",}
    response = requests.get(url, headers=header)
    if response.ok:
        return response
    else:
        print(f"{response.status_code}\nRequest error for {url}")
        return []

def get_fours_for_day(query_date):
    # All forms for ghe current business day
    # https://www.sec.gov/cgi-bin/current?q1=0&q2=6&q3=
    biz_days_prior = (date.today()-query_date).days
    query_str = f"https://www.sec.gov/cgi-bin/current?q1={biz_days_prior}&q2=0&q3=4"
    response = request(query_str)
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find("pre").find_all("a")
    company_action = {}
    document = set()
    for a_tags in items:
        if "/Archives/edgar" in a_tags['href']:
            document = (a_tags.text,a_tags['href'])
        elif a_tags.text in company_action:
            company_action[a_tags.text].append(document)
        else:
            company_action[a_tags.text] = [document]
    return company_action

def parse_four(file_url):
    base_url = "https://www.sec.gov"
    response = request(base_url+file_url)
    soup = BeautifulSoup(response.content, 'html.parser')
    links = soup.find_all("a")
    xml_links =[]
    for link in links:
        if link["href"].find("xml") != -1:
            xml_links.append(link["href"])
    return xml_links

    # a_tags = table.find("table", {"class": "tableFile"})
    return soup
if __name__ == "__main__":
    url = "https://www.edgarcompany.sec.gov/servlet/CompanyDBSearch?start_row=-1&end_row=-1&main_back=1&cik=&company_name=TESLA&reporting_file_number=&series_id=&series_name=&class_contract_id=&class_contract_name=&state_country=NONE&city=&state_incorporation=NONE&zip_code=&last_update_from=&last_update_to=&page=summary&submit_button=View+Summary"
    b = date(2011,11,17)
    