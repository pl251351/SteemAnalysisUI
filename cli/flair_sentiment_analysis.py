import json

from flair.data import Sentence
from flair.models import TextClassifier
from nltk import WordPunctTokenizer

from steemanalysis.database_repo import DataRepository

repo = DataRepository('../instance/repo.db')
steem_entry_urls = repo.select_text_with_values(100000, -1)

classifier = TextClassifier.load('sentiment')

for row in steem_entry_urls:
    text = row[3]
    url_id = row[1]
    # clean text
    lower_case_text = text.lower()
    tok = WordPunctTokenizer()
    words = tok.tokenize(lower_case_text)
    clean_text = (' '.join(words)).strip()

    clean_text = clean_text.strip()
    if clean_text:
        sentence = Sentence(clean_text)
        classifier.predict(sentence)

        if sentence and sentence.labels:
            labels_ = sentence.labels[0]
            labels__score = labels_.score
            if labels_.value == 'NEGATIVE':
                labels__score *= -1
            x = {
                'score': labels__score,
                'value': labels_.value,
            }

            json_dumps = json.dumps(x)

            repo.create_flair_responses([json_dumps, url_id])
