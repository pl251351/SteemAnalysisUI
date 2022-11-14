import csv
import json
import random

import requests as requests

from steemanalysis.database_repo import DataRepository

PREFIX_POST_URL = 'https://steemit.com/hive-114435/'
PREFIX_TRENDING_URL = "https://steemit.com/trending/%s"

repo = DataRepository('../instance/repo.db')

# there are some records with only 4 field like
# ['1998600', '', 'beatsfrxdo', 'beats']
# ['2021302', '', 'testasrimantas', 'testas']
# ignroing those
# post_id is not unique
# using a sample json
# for querying json use
#   https://devopsheaven.com/sqlite/databases/json/python/api/2017/10/11/sqlite-json-data-python.html
# json only has 100 entries to I have to reset it  to get all with some value for test

with open('../comment-month-4.csv', 'r') as csvfile:
    # open csv reader
    reader = csv.reader(csvfile)
    # skip header row
    next(reader)

    # just get some random json
    countries_api_res = requests.get('http://api.worldbank.org/countries?format=json&per_page=100')
    countries = countries_api_res.json()[1]

    i = 0

    # iterate over all rows in file
    for row in reader:
        # if less than 5 column skip it
        if len(row) < 5:
            print(row)
        else:
            # this is hard coded
            file_name = 'comment-month-4.csv'
            # create comments
            row.append(file_name)
            comment_id = repo.create_comments(row)

            # if first column in empty then it is trending URL
            if row[1]:
                # create post URL
                urls_1 = (PREFIX_POST_URL + "@%s/%s" % (row[1], row[2],), None, None, comment_id, None, None)
            else:
                # create trending URL
                urls_1 = (None, None, PREFIX_TRENDING_URL % row[2], None, None, comment_id)

            # store URL in DB
            url_1_id = repo.create_urls(urls_1)

            # store response in DB
            response_1 = repo.create_responses([json.dumps(countries[i]), url_1_id])
            # print("response is %s" % response_1)

            # create random value for test and store in DB for main post
            repo.create_value_earned([random.uniform(1.00, 100.00), 'some post text' + str(i), url_1_id])

            i = i + 1
            # create comment URL
            # we may not want to do this - as I think main post is more important  - need to clarify
            urls_1 = (None, PREFIX_POST_URL + "@%s/%s" % (row[3], row[4],), None, None, comment_id, None)
            url_1_id = repo.create_urls(urls_1)
            # get its response and save in DB
            response_2 = repo.create_responses([json.dumps(countries[i]), url_1_id])
            # print("response is %s" % response_2)
            i = i + 1

            if i == 100:
                i = 0

            # store value of comment in DB
            repo.create_value_earned([random.uniform(1.00, 100.00), "some comment text" + str(i), url_1_id])
