import json

from google.cloud import language
from nltk import WordPunctTokenizer

from steemanalysis.database_repo import DataRepository

# https://codelabs.developers.google.com/codelabs/cloud-natural-language-python3#4

def analyze_text_sentiment(text):
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


repo = DataRepository('../instance/repo.db')
steem_entry_urls = repo.select_text_with_values(2000, -1)

for row in steem_entry_urls:
    text = row[3]
    url_id = row[1]

    # clean text
    lower_case_text = text.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_text)
    clean_text = (' '.join(words)).strip()

    try:
        response = analyze_text_sentiment(clean_text)
        repo.create_google_responses([response, url_id])
    except:
        pass
