import json

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions, SentimentOptions
from nltk import WordPunctTokenizer

from steemanalysis.credentials import API_KEY, URL
from steemanalysis.database_repo import DataRepository


def analyze_ibm_watson_sentiment(text):
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(URL)

    # features = Features(entities=EntitiesOptions(emotion=True, sentiment=True),
    #                     keywords=KeywordsOptions(emotion=True, sentiment=True))

    features = Features(sentiment=SentimentOptions(document=True))
    watson_response = natural_language_understanding.analyze(
        text=text,
        features=features).get_result()

    return json.dumps(watson_response)


repo = DataRepository('../instance/repo.db')
steem_entry_urls = repo.select_text_with_values(3000, -1)

for row in steem_entry_urls:
    text = row[3]
    url_id = row[1]

    # clean text
    lower_case_text = text.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_text)
    clean_text = (' '.join(words)).strip()

    try:
        response = analyze_ibm_watson_sentiment(clean_text)
        repo.create_ibm_responses([response, url_id])
    except Exception as e:
        print(e)
