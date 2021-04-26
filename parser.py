import requests
import json
import re
from bs4 import BeautifulSoup

HOMEPAGE = "https://jo.opensooq.com/en/real-estate-for-sale/all"
ROOTPAGE = "https://jo.opensooq.com"

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36',
    'accept': '*/*'
}

"""
        We input url, parse the given html with beautiful soup
        In next step, we upload parsed information to json file
        After this we apply pymovie library in order to make a video
        And we automatically post it on youtube.
"""


def get_html(url, parameters=None):
    """This function requests html file from url"""
    r = requests.get(url, headers=HEADERS, params=parameters)
    return r


def parse_ul(html_element):
    result = {}
    for sub in html_element.find_all('li', recursive=False):
        if sub.a is None:
            continue
        data = {k: v for k, v in sub.a.attrs.items() if k != 'class'}
        if sub.ul is not None:
            # recurse down
            data['children'] = parse_ul(sub.ul)
        result[sub.a.get_text(strip=True)] = data
    return result


def get_content(html):

    """ This function takes html and parses all the main information about real estate"""

    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div', class_="rectLiDetails tableCell vMiddle p8")
    all_estate = {"Real Estate": []}

    for item in items:

        full_link = item.find('a').get('href')
        full_title = item.find('a').get('title')
        list_link = full_link.split('/')
        del list_link[-1]
        new_link = ROOTPAGE + "/".join(list_link)
        article_html = get_html(new_link)
        new_soup = BeautifulSoup(article_html.text, "html.parser")
        final_html = new_soup.find('div', class_="customP overflowHidden")
        final_html = final_html.find('ul')
        all_info = {'Title': full_title, 'Link': new_link}

        for tag in final_html.find_all("li"):
            original_string = "{0}".format(tag.text)
            nice_string = re.sub(r"\r\n", " ", original_string)
            nice_list = nice_string.split()
            nice_string = " ".join(nice_list)
            nice_list = nice_string.split(":")
            all_info[nice_list[0]] = nice_list[1]

        all_estate["Real Estate"].append(all_info)

    return all_estate


def parser():
    html = get_html(HOMEPAGE)
    if html.status_code == 200:
        json_dictionary = get_content(html.text)
        with open('real_estate.json', 'w') as file:
            json.dump(json_dictionary, file, indent=2, ensure_ascii=False)
            print("Success!")
    else:
        print("Error!")


parser()
