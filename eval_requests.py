# load packages
from easynmt import EasyNMT
from flask import Flask
import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)

@app.route('/')
def hello():
    print('hello world')

# # ### Load and prepare data
#
# # load data
# raw = pd.read_parquet('translated.parquet.gzip')
#
# # access your multilingual data and ensure it is lowercase
# multi = pd.DataFrame()
# multi['trans_text'] = raw.trans_text.str.lower()
#
# # ### Translate multilingual tickets into English for processing
# # build translation model
# trans = EasyNMT('mbart50_m2en')
#
# # translate multilingual to english
# strings = multi.trans_text.tolist()
# multi['en_text'] = trans.translate(strings, target_lang='en', max_new_tokens=200)
#
# # ### Create initial urgency ratings based on sentiment and strength of the negative sentiment
# # run sentiment analysis to find negatives and potential negatives
# sia = SentimentIntensityAnalyzer()
#
# def v_polarity(text):
#     return sia.polarity_scores(text)['compound']
#
# def v_negativity(text):
#     return sia.polarity_scores(text)['neg']
#
# multi['polarity'] = multi['en_text'].apply(v_polarity)
# multi['negativity'] = multi['en_text'].apply(v_negativity)
#
# # label tickets as positive, negative, or neutral
# min_positive = 0.3
# min_neutral = 0
#
# multi['polarity_class'] = np.select([((multi['polarity'] > min_positive) & ((multi['negativity'] == 0) | (multi['polarity'] > 0.7))),
#                                      ((multi['polarity'] < min_neutral) | (multi['negativity'] > 0)),
#                                      ((min_positive >= multi['polarity']) & (multi['polarity'] >= min_neutral))],
#                                     ['Positive', 'Negative', 'Neutral'])
#
# # classify urgency based on level of negativity
# high_urgency_max = -0.5
# mid_urgency_max = -0.35
# low_urgency_min = -0.2
#
# multi['urgency_polarity'] = np.select([(multi['polarity'] < high_urgency_max),
#                                        ((multi['polarity'] > low_urgency_min) & (multi['polarity_class'] != "Positive")),
#                                        ((mid_urgency_max <= multi['polarity']) & (multi['polarity'] <= low_urgency_min)),
#                                        ((high_urgency_max <= multi['polarity']) & (multi['polarity'] <= mid_urgency_max))],
#                                      [4, 1, 2, 3],
#                                      -5).astype(int)
#
# # ### Adjust urgency rating based on words and characters used in the ticket
# # keywords for urgency; score based on number of words in text
# urgent_words = ['need', 'urgent', 'urgency', 'urgently', 'please', 'help', 'useless', 'immediate', 'immediately', 'dire', 'asap', 'pay', 'paid', 'worst', 'worse', 'terrible', 'terribly', 'broke', 'broken', 'disappoint', 'disappointed', 'disappointingly', 'disappointing', 'quick', 'fast']
# urgent_symbols = ['!', '$', '?']
#
# def urgent_word_count(text):
#     count = 0
#     for symbol in urgent_symbols:
#         count += text.count(symbol)/2
#
#     text = ''.join([a for a in text if a.isalpha() or a == " "])
#
#     to_check = text.split()
#     for word in urgent_words:
#         count += to_check.count(word)
#
#     return count
#
#
# # get counts of urgent text
# multi['urgency_text'] = multi['en_text'].apply(urgent_word_count)
#
# # get key urgency stats
# urgency_text_90th_p = multi.urgency_text.iloc[round(len(multi.urgency_text)*.1)]
# urgency_text_75th_p = multi.urgency_text.iloc[round(len(multi.urgency_text)*.25)]
#
# # increase urgency level based on num of urgency text score
# multi['urgency_rating'] = np.where(((multi['polarity'] != 'Positive') & (multi['urgency_text'] > urgency_text_75th_p) & (multi['urgency_polarity'] > 0)),
#                                   multi['urgency_polarity'] + 1,
#                                   multi['urgency_polarity'])
#
# multi['urgency_rating'] = np.where(((multi['polarity'] != 'Positive') & (multi['urgency_text'] > urgency_text_90th_p) & (multi['urgency_polarity'] > 0)),
#                                   multi['urgency_rating'] + 1,
#                                   multi['urgency_rating'])
#
# # ### Create final urgency classification based on above
# # create classification based on urgency ratings
# multi['urgency_class'] = np.select([(multi['urgency_rating'] == 6), (multi['urgency_rating'] == 5), (multi['urgency_rating'] == 4), (multi['urgency_rating'] == 3), (multi['urgency_rating'] == 2), ((multi['urgency_rating'] == 1) & (multi['urgency_text'] > 0)), ((multi['urgency_rating'] == 1) & (multi['urgency_text'] == 0))],
#                                   ['HIGH', 'HIGH', 'Mid-High', 'Low-Mid', 'Low', 'Lowest', 'None'],
#                                   'None')
#
# # make urgency classes sortable
# multi.urgency_class = pd.Categorical(multi.urgency_class,
#                                     categories=['None', 'Lowest', 'Low', 'Low-Mid', 'Mid-High', 'HIGH'],
#                                     ordered=True)
#
# multi.sort_values(by='urgency_class', ascending=False)
