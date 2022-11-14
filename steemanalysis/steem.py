import json

import requests
from bs4 import BeautifulSoup
from flask import (
    Blueprint, render_template, request, redirect, session
)
from flask import current_app

from steemanalysis.analysis import analyze_vader_text_sentiment, analyze_google_text_sentiment, \
    analyze_ibm_watson_sentiment, analyze_textblob_sentiment, analyze_flair_sentiment
from steemanalysis.db import get_repo
from steemanalysis.page import PageForm, AnalysisForm
from steemanalysis.statistical_analysis import analyze as stat_analyze

bp = Blueprint('steem', __name__)


@bp.route('/')
def index():
    with open('imported_files.json', 'r') as json_file:
        file_list = json.load(json_file)
        file_list = [detail for detail in file_list if detail['imported']]

    analysis_form = AnalysisForm()
    analysis_form.drop_bottom.data = 0.01
    analysis_form.drop_top.data = 0.99
    analysis_form.use_records_with_value.data = 0.0
    analysis_form.drop_zero_value_earned.data = False
    return render_template('steem/index.html', file_list=file_list, form=analysis_form)


@bp.route('/<string:key_id>/view', methods=["GET", "POST"])
def view_file(key_id):
    if request.method == 'POST':
        form = PageForm()
        if not form.validate_on_submit():
            return redirect(f'/{key_id}/view')
        session['per_page'] = form.numberofpages.data
        session['view_all'] = form.view_all.data

    repo = get_repo()

    view_all = session['view_all'] if 'view_all' in session else None
    if not view_all:
        view_all = request.args.get('view_all', False, type=int)

    count = repo.count_comment_by_file_name(key_id, view_all)

    per_page = session['per_page'] if 'per_page' in session else 10
    if per_page == 10:
        # check request for per page
        per_page = request.args.get('per_page', 10, type=int)  # define how many results you want per page
    page = request.args.get('page', 1, type=int)
    pages = count // per_page  # this is the number of pages
    offset = (page - 1) * per_page  # offset for SQL query
    limit = 20 if page == pages else per_page  # limit for SQL query

    steem_records = {'total_pages': pages, 'previous_page': page - 1 if page - 1 > 0 else -1,
                     'next_page': page + 1 if page + 1 < count else -1,
                     'records': repo.select_comment_by_file_name(key_id, limit, offset, view_all)}

    page_form = PageForm()

    return render_template('steem/page.html', records=steem_records, form=page_form)


@bp.route('/<int:key_id>/view_post_detail')
def view_post_detail(key_id):
    text_record = {
        'text': 'Not extracted yet',
        'value': 0.00
    }
    repo = get_repo()
    val = repo.select_post_details_from_url(key_id)
    if val:
        text_record['text'] = val['extracted_text']
        text_record['value'] = val['value_earned']
    text_record['url_id'] = key_id

    return render_template('steem/post_detail.html', records=text_record)


@bp.route('/<int:key_id>/extract_text')
def extract_text(key_id):
    text_record = {
        'text': 'Not extracted yet',
        'value': 0.00
    }

    repo = get_repo()
    fetchone = repo.select_post_url_from_post_id(key_id)
    url = fetchone[0]
    row_id = fetchone[1]

    # http request to get page
    r = requests.get(url)
    if r.status_code != 200:
        current_app.logger.warning("Unable to fetch text for: %s, returned status code: %d" % (url, r.status_code))
    else:
        # get text from request
        page_html = r.text
        # parse the request
        page_soup = BeautifulSoup(page_html, "html.parser")
        # find tag which has link to image file. MarkdownViewer > div:nth-child(1)
        entries = page_soup.select_one(".PostFull__body > div:nth-child(1)")
        money_integer = page_soup.select_one(".integer")
        money_decimal = page_soup.select_one(".decimal")
        # collect all links in a list
        if money_integer and money_decimal:
            money = float("%s%s" % (money_integer.text, money_decimal.text))
            # print("Money is %s%s" % (money_integer.text, money_decimal.text))
            text = ''
            for res in entries:
                # print(res.text)
                text = text + res.text
                text = text + '\n'
            repo.create_value_earned([money, text, row_id])
            text_record['text'] = text
            text_record['value'] = money
        else:
            current_app.logger.warning("Unable to extract text for: %s, skipping it" % url)

    return render_template('steem/post_detail.html', records=text_record)


@bp.route('/<int:key_id>/view_analysis')
def view_analysis(key_id):
    text_analysis = {'text': 'No analysis yet', 'uri': None}
    repo = get_repo()

    val = repo.select_response_from_url(key_id)
    if val:
        text_analysis['text'] = val[0]

    text_analysis['uri'] = key_id

    return render_template('steem/sentiment_analysis.html', records=text_analysis)


@bp.route('/<int:key_id>/view_google_analysis')
def view_google_analysis(key_id):
    text_analysis = {'text': 'No analysis yet', 'uri': None}
    repo = get_repo()

    val = repo.select_google_response_from_url(key_id)
    if val:
        text_analysis['text'] = val[0]

    text_analysis['uri'] = key_id

    return render_template('steem/google_sentiment_analysis.html', records=text_analysis)


@bp.route('/<int:key_id>/view_ibm_analysis')
def view_ibm_analysis(key_id):
    text_analysis = {'text': 'No analysis yet', 'uri': None}
    repo = get_repo()

    val = repo.select_ibm_response_from_url(key_id)
    if val:
        text_analysis['text'] = val[0]

    text_analysis['uri'] = key_id

    return render_template('steem/ibm_sentiment_analysis.html', records=text_analysis)


@bp.route('/<int:key_id>/view_textblob_analysis')
def view_textblob_analysis(key_id):
    text_analysis = {'text': 'No analysis yet', 'uri': None}
    repo = get_repo()

    val = repo.select_textblob_response_from_url(key_id)
    if val:
        text_analysis['text'] = val[0]

    text_analysis['uri'] = key_id

    return render_template('steem/textblob_sentiment_analysis.html', records=text_analysis)


@bp.route('/<int:key_id>/view_flair_analysis')
def view_flair_analysis(key_id):
    text_analysis = {'text': 'No analysis yet', 'uri': None}
    repo = get_repo()

    val = repo.select_flair_response_from_url(key_id)
    if val:
        text_analysis['text'] = val[0]

    text_analysis['uri'] = key_id

    return render_template('steem/flair_sentiment_analysis.html', records=text_analysis)


@bp.route('/<int:key_id>/new_vader_analysis')
def new_vader_analysis(key_id):
    text_record = {
        'text': 'Not extracted yet',
        'value': 0.00
    }

    repo = get_repo()
    row = repo.select_extracted_text_from_url(key_id)
    if row:
        text = row[0]

        json_dumps = analyze_vader_text_sentiment(text)

        repo = get_repo()
        repo.create_responses([json_dumps, row[1]])

        text_record['text'] = json_dumps

    return render_template('steem/post_detail.html', records=text_record)


@bp.route('/<int:key_id>/new_google_analysis')
def new_google_analysis(key_id):
    # export GOOGLE_APPLICATION_CREDENTIALS=~/key.json
    text_record = {
        'text': 'Not extracted yet',
        'value': 0.00
    }

    repo = get_repo()
    row = repo.select_extracted_text_from_url(key_id)
    if row:
        text = row[0]

        json_dumps = analyze_google_text_sentiment(text)

        repo = get_repo()
        repo.create_google_responses([json_dumps, row[1]])

        text_record['text'] = json_dumps

    return render_template('steem/post_detail.html', records=text_record)


@bp.route('/<int:key_id>/new_ibm_analysis')
def new_ibm_analysis(key_id):
    # get ibm analysis here
    text_record = {
        'text': 'Not extracted yet',
        'value': 0.00
    }

    repo = get_repo()
    row = repo.select_extracted_text_from_url(key_id)
    if row:
        text = row[0]

        json_dumps = analyze_ibm_watson_sentiment(text)

        repo = get_repo()
        repo.create_ibm_responses([json_dumps, row[1]])

        text_record['text'] = json_dumps

    return render_template('steem/post_detail.html', records=text_record)


@bp.route('/<int:key_id>/new_textblob_analysis')
def new_textblob_analysis(key_id):
    # get textblob analysis here
    text_record = {
        'text': 'Not extracted yet',
        'value': 0.00
    }

    repo = get_repo()
    row = repo.select_extracted_text_from_url(key_id)
    if row:
        text = row[0]

        json_dumps = analyze_textblob_sentiment(text)

        repo = get_repo()
        repo.create_textblob_responses([json_dumps, row[1]])

        text_record['text'] = json_dumps

    return render_template('steem/post_detail.html', records=text_record)


@bp.route('/<int:key_id>/new_flair_analysis')
def new_flair_analysis(key_id):
    # get textblob analysis here
    text_record = {
        'text': 'Not extracted yet',
        'value': 0.00
    }

    repo = get_repo()
    row = repo.select_extracted_text_from_url(key_id)
    if row:
        text = row[0]

        json_dumps = analyze_flair_sentiment(text)

        repo = get_repo()
        repo.create_flair_responses([json_dumps, row[1]])

        text_record['text'] = json_dumps

    return render_template('steem/post_detail.html', records=text_record)


@bp.route('/stat_analysis', methods=["POST"])
def stat_analysis():
    form = AnalysisForm()
    if not form.validate_on_submit():
        return redirect('/')

    # get ibm analysis here
    details = ('EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY', 'EMPTY')

    # sentiment_engines = ['vader', 'google', 'ibm', 'tb', 'flair']
    sentiment_engines = ['vader', 'google', 'ibm']

    repo = get_repo()
    df = repo.select_for_combined_correlation_analysis()
    if not df.empty and form:
        data = form.analyze_for.data
        value_data = form.use_records_with_value.data
        bottom_data = form.drop_bottom.data
        top_data = form.drop_top.data
        drop_zero_value_earned = form.drop_zero_value_earned.data

        for se in sentiment_engines:
            if not se == data:
                del df[se]

        details = stat_analyze(df, data, value_data, bottom_data, top_data, drop_zero_value_earned)

    return render_template('steem/stat_detail.html', records=details, form=form)
