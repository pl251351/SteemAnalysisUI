import json

import nltk
from flair.data import Sentence
from flair.models import TextClassifier
from google.cloud import language
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_watson.natural_language_understanding_v1 import Features, EntitiesOptions, KeywordsOptions
from nltk import WordPunctTokenizer
from nltk.sentiment import SentimentIntensityAnalyzer
from textblob import TextBlob

from steemanalysis.credentials import API_KEY, URL

nltk.download('vader_lexicon', download_dir='.', quiet=True)


def clean_text(text):
    # clean text
    lower_case_text = text.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_text)
    return (' '.join(words)).strip()


def analyze_google_text_sentiment(text):
    text = clean_text(text)
    client = language.LanguageServiceClient()
    document = language.Document(content=text, type_=language.Document.Type.PLAIN_TEXT)

    response = client.analyze_sentiment(document=document)

    sentiment = response.document_sentiment
    results = dict(
        score=sentiment.score,
        magnitude=sentiment.magnitude,
    )
    # results = dict(
    #     score=f"{sentiment.score:.1%}",
    #     magnitude=f"{sentiment.magnitude:.1%}",
    # )

    return json.dumps(results)


def analyze_vader_text_sentiment(text):
    text = clean_text(text)
    sid = SentimentIntensityAnalyzer()
    response = sid.polarity_scores(text)

    return json.dumps(response)


def analyze_ibm_watson_sentiment(text):
    text = clean_text(text)
    authenticator = IAMAuthenticator(API_KEY)
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2022-04-07',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(URL)

    features = Features(entities=EntitiesOptions(emotion=True, sentiment=True),
                        keywords=KeywordsOptions(emotion=True, sentiment=True))
    response = natural_language_understanding.analyze(
        text=text,
        features=features).get_result()

    return json.dumps(response)


def analyze_textblob_sentiment(text):
    text = clean_text(text)
    return TextBlob(text).sentiment


def analyze_flair_sentiment(text):
    text = clean_text(text)
    classifier = TextClassifier.load('en-sentiment')
    sentence = Sentence(text)
    classifier.predict(sentence)
    return sentence.labels
