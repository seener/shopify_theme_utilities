# -*- coding: utf-8 -*-
"""
Created on Wed Dec 26 13:14:08 2018

@author: Sean Howard
"""


from bs4 import BeautifulSoup, Comment
from requests import get
from requests.exceptions import RequestException


def get_page(url):
    """
    Function returns the hmtl content of a webpage provide as a url

    Dependency
    ----------
    get from requests
    BeautifulSoup from bs4

    Parameters
    ----------
    url: webpage address

    Returns
    -------
    result: hmtl object parsed by the BeautifulSoup function

    """
    try:
        with get(url, stream=True) as resp:
            html = BeautifulSoup(resp.content, 'html.parser')
            return html
    except RequestException as error:
        print("There was a problem accessing {0}: {1}".format(url, error))
        return None


def get_style_sheet(html_head):
    """
    Returns the style sheet comment string from the head of the html

    Dependency
    ----------
    Comment from bs4

    Parameters
    ----------
    html_head: the head object from the parsed html page

    Returns
    -------
    result: string with the stylesheet information
    """
    for comments in html_head.find_all(text=lambda text: isinstance(text, Comment)):
        if "stylesheets for" in str.lower(comments.extract()):
            return comments.extract().strip()


FILE = input("Provide full path to the file with URLS: ")
with open(FILE, 'r') as f:
    URLS = f.read().split("\n")

for url in URLS:
    HEAD = get_page(url).head  # get just he head of the page
    STYLE = get_style_sheet(HEAD)  # get the style sheet used
    print(url + ": " + STYLE)
