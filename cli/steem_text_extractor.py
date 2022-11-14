import requests
from bs4 import BeautifulSoup

from steemanalysis.database_repo import DataRepository

repo = DataRepository('../instance/repo.db')
steem_entry_urls = repo.select_random_post_url(500)

for steem_url in steem_entry_urls:
    # http request to get page
    url_ = steem_url[0]
    r = requests.get(url_)
    if r.status_code != 200:
        print(url_)
        continue
    # get text from request
    page_html = r.text
    # parse the request
    page_soup = BeautifulSoup(page_html, "html.parser")
    # find tag which has link to image file. MarkdownViewer > div:nth-child(1)
    # entries = page_soup.select_one(".MarkdownViewer > div:nth-child(1)")
    entries = page_soup.select_one(".PostFull__body > div:nth-child(1)")
    money_integer = page_soup.select_one(".integer")
    money_decimal = page_soup.select_one(".decimal")
    # collect all links in a list
    money = 0.0
    if money_integer and money_decimal:
        money = float("%s%s" % (money_integer.text, money_decimal.text))
        # print("Money is %s%s" % (money_integer.text, money_decimal.text))
        text = ''
        for res in entries:
            # print(res.text)
            text = text + res.text
            text = text + '\n'
        text = text.strip()
        if len(text) < 5:
            print("URL:%s, text is:%s" % (url_, text))
        repo.create_value_earned([money, text, steem_url[1]])
    else:
        print(url_)
