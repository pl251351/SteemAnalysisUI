import json

import nltk
from nltk import WordPunctTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from steemanalysis.database_repo import DataRepository

nltk.download('vader_lexicon')

repo = DataRepository('../instance/repo.db')
steem_entry_urls = repo.select_text_with_values(5000, -1)

sid = SentimentIntensityAnalyzer()
for row in steem_entry_urls:
    text = row[3]
    url_id = row[1]
    # clean text
    lower_case_text = text.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_text)
    clean_text = (' '.join(words)).strip()
    response = sid.polarity_scores(text)
    json_dumps = json.dumps(response)
    repo.create_responses([json_dumps, url_id])
