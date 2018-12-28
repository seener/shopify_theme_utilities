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
    all_comments = html_head.find_all(text=lambda t: isinstance(t, Comment))
    out = None
    for comment in all_comments:
        if "stylesheets for" in str.lower(comment.extract()):
            out = comment.extract().strip()
    return out


FILE = input("Provide full path to the file with URLS: ")
with open(FILE, 'r') as f:
    URLS = f.read().split("\n")

for link in URLS:
    HEAD = get_page(link).head  # get just the head of the page
    STYLE = get_style_sheet(HEAD)  # get the style sheet used
    print(link + ": " + STYLE)
