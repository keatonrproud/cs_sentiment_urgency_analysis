# load packages
import flask.debughelpers
from deep_translator import GoogleTranslator, exceptions
from luga import language
from flask import Flask, render_template, request, url_for, redirect, send_from_directory
import os
import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__, template_folder='templates', static_folder='staticFiles')

app.config['FILE_UPLOADS'] = 'flask_upload'

sia = SentimentIntensityAnalyzer()

@app.route('/')
def init():
    return redirect(url_for('entry'))

@app.route('/entry', methods=['POST', 'GET'])
def entry():
    return render_template('index.html', title='hello')

@app.route('/classify_string', methods=['POST', 'GET'])
def classify_string():
    string = request.form['classify_string']
    if string:
        try:
            trans_text, lang = translate_str(string)
        except exceptions.LanguageNotSupportedException:
            msg = f"Language detected {language(string).name} is not supported for translation."
            return render_template('classify_string_error.html', error=msg)
        except exceptions.TooManyRequests:
            msg = f"Too many requests for translations have been made through the API. Please try again in a few minutes"
            return render_template('classify_string_error.html', error=msg)

        (sentiment, urgency, classification) = get_classification(trans_text)
    else:
        msg = 'No string was entered.'
        return render_template('classify_string_error.html', error=msg)
    if request.method == 'POST':
        return render_template('classify_string.html', string=string,
                               classification=classification,
                               language=lang,
                               sentiment=sentiment,
                               urgency=urgency)

def translate_str(text):
    lang = language(text).name
    if lang == 'zh':
        lang = 'zh-CN'
    return GoogleTranslator(source=lang, target='en').translate(text), lang.upper()

def v_polarity(text):
    return sia.polarity_scores(text)['compound']
def v_negativity(text):
    return sia.polarity_scores(text)['neg']

def get_classification(text):

    polarity = v_polarity(text)
    negativity = v_negativity(text)

    min_positive = 0.3
    min_neutral = 0

    if polarity > min_positive and (negativity == 0 or polarity > 0.7):
        sentiment = 'Positive'
    elif polarity < min_neutral or negativity > 0:
        sentiment = 'Negative'
    else:
        sentiment = 'Neutral'

    high_urgency_max = -0.5
    mid_urgency_max = -0.35
    low_urgency_min = -0.2

    if polarity < high_urgency_max:
        urgency = 4
    elif polarity > low_urgency_min and sentiment != 'Positive':
        urgency = 1
    elif mid_urgency_max <= polarity and polarity <= low_urgency_min:
        urgency = 2
    elif high_urgency_max <= polarity and polarity <= mid_urgency_max:
        urgency = 3
    else:
        urgency = -5

    urgent_words = ['need', 'urgent', 'urgency', 'urgently', 'please', 'help', 'useless', 'immediate', 'immediately', 'dire', 'asap', 'pay', 'paid', 'worst', 'worse', 'terrible', 'terribly', 'broke', 'broken', 'disappoint', 'disappointed', 'disappointingly', 'disappointing', 'quick', 'fast', 'fuck', 'fucking', 'shit', 'damn', 'fucker', 'wrong', 'hell']
    urgent_symbols = ['!', '$', '?']

    count = 0
    for symbol in urgent_symbols:
        count += text.count(symbol)/2

    txt = ''.join([a for a in text if a.isalpha() or a == " "])

    to_check = txt.split()
    for word in urgent_words:
        count += to_check.count(word)

    if polarity != 'Positive':
        if count >= 3:
            urgency += 2
        elif count >= 1.5:
            urgency += 1

    if urgency == 6:
        classification = "HIGH"
    elif urgency == 5:
        classification = "HIGH"
    elif urgency == 4:
        classification = "Mid-High"
    elif urgency == 3:
        classification = "Low-Mid"
    elif urgency == 2:
        classification = "Low"
    elif urgency == 1:
        classification = "Lowest"
    else:
        classification = "No"

    return sentiment, urgency, classification

@app.route('/classify_file', methods=['POST', 'GET'])
def classify_file():
    try:
        file = request.files['tickets_file']
    except flask.debughelpers.DebugFilesKeyError:
        print('error 1')
        msg = "No file was uploaded."
        return render_template('classify_file_error.html', error=msg)
    path = os.path.join(app.config['FILE_UPLOADS'], file.filename)
    try:
        file.save(path)
    except FileNotFoundError:
        print('error 2')
        msg = "No file was uploaded."
        return render_template('classify_file_error.html', error=msg)
    try:
        data = pd.read_csv(path, header=None)
    except UnicodeDecodeError:
        print('unicode error')
        msg = "The file you have submitted is not encoded properly for the given text. Ensure it is saved as a .csv UTF-8 and not a normal .csv."
        return render_template('classify_file_error.html', error=msg)

    data.rename(columns={0: "input"}, inplace=True)

    # translate data
    data['input_english'] = data['input'].apply(translate_str).str[0]
    data['input_english'] = data['input_english']
    data['polarity'] = data['input_english'].apply(v_polarity)
    data['negativity'] = data['input_english'].apply(v_negativity)
    
    # get main sentiment ratings
    min_positive = 0.3
    min_neutral = 0

    data['sentiment'] = np.select([((data['polarity'] > min_positive) & ((data['negativity'] == 0) | (data['polarity'] > 0.7))),
                                         ((data['polarity'] < min_neutral) | (data['negativity'] > 0)),
                                         ((min_positive >= data['polarity']) & (data['polarity'] >= min_neutral))],
                                        ['Positive', 'Negative', 'Neutral'])

    high_urgency_max = -0.5
    mid_urgency_max = -0.35
    low_urgency_min = -0.2

    data['urgency_polarity'] = np.select([(data['polarity'] < high_urgency_max),
                                           ((data['polarity'] > low_urgency_min) & (data['sentiment'] != "Positive")),
                                           ((mid_urgency_max <= data['polarity']) & (data['polarity'] <= low_urgency_min)),
                                           ((high_urgency_max <= data['polarity']) & (data['polarity'] <= mid_urgency_max))],
                                         [4, 1, 2, 3],
                                         -5).astype(int)

    urgent_words = ['need', 'urgent', 'urgency', 'urgently', 'please', 'help', 'useless', 'immediate', 'immediately', 'dire', 'asap', 'pay', 'paid', 'worst', 'worse', 'terrible', 'terribly', 'broke', 'broken', 'disappoint', 'disappointed', 'disappointingly', 'disappointing', 'quick', 'fast']
    urgent_symbols = ['!', '$', '?']

    def urgent_word_count(text):
        count = 0
        for symbol in urgent_symbols:
            count += text.count(symbol)/2

        text = ''.join([a for a in text if a.isalpha() or a == " "])

        to_check = text.split()
        for word in urgent_words:
            count += to_check.count(word)

        return count


    # get counts of urgent text
    data['urgency_text'] = data['input_english'].apply(urgent_word_count)

    # # increase urgency level based on num of urgency text score
    if len(data) > 20:
        urgency_text_level2 = data.urgency_text.iloc[round(len(data.urgency_text)*.1)]
        urgency_text_level1 = data.urgency_text.iloc[round(len(data.urgency_text)*.25)]    
    else:
        urgency_text_level2 = 3
        urgency_text_level1 = 1

    data['urgency_rating'] = np.where(((data['polarity'] != 'Positive') & (data['urgency_text'] > urgency_text_level2) & (data['urgency_polarity'] > 0)),
                                      data['urgency_polarity'] + 1,
                                      data['urgency_polarity'])

    data['urgency_rating'] = np.where(((data['polarity'] != 'Positive') & (data['urgency_text'] > urgency_text_level1) & (data['urgency_polarity'] > 0)),
                                      data['urgency_rating'] + 1,
                                      data['urgency_rating'])

    # create classification based on urgency ratings
    data['classification'] = np.select([(data['urgency_rating'] == 6),
                                       (data['urgency_rating'] == 5),
                                       (data['urgency_rating'] == 4),
                                       (data['urgency_rating'] == 3),
                                       (data['urgency_rating'] == 2),
                                       ((data['urgency_rating'] == 1) & (data['urgency_text'] > 0)),
                                       ((data['urgency_rating'] == 1) & (data['urgency_text'] == 0))],
                                      ['HIGH', 'HIGH', 'Mid-High', 'Low-Mid', 'Low', 'Lowest', 'Not Urgent'],
                                      'Not Urgent')

    # make urgency classes sortable
    data.classification = pd.Categorical(data.classification,
                                        categories=['Not Urgent', 'Lowest', 'Low', 'Low-Mid', 'Mid-High', 'HIGH'],
                                        ordered=True)
    data.sentiment = pd.Categorical(data.sentiment,
                                    categories=['Negative', 'Neutral', 'Positive'],
                                    ordered=True)

    data.sort_values(by='urgency_rating', ascending=False, inplace=True)

    data = data[['input', 'input_english', 'classification', 'sentiment', 'negativity', 'urgency_rating']]

    data.columns = data.columns.str.capitalize()

    if request.method == 'POST':
        return render_template('classify_file.html',
                               row_data=list(data.values.tolist()),
                               column_names=data.columns.values,
                               zip=zip)

if __name__ == '__main__':
    app.run(debug=True)
