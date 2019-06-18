import sys
import urllib2
import html2text
import pymongo
import nltk
import nltk.corpus
import nltk.tokenize.punkt
import nltk.stem.snowball
import string from nltk.stem
import WordNetLemmatizer from pymongo
import MongoClient from nltk.stem
import SnowballStemmer
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(string.punctuation) stopwords.append()

lemma = SnowballStemmer("english")
def is_ci_token_stopword_set_match(a, b, threshold=0.05):
    tokens_a = [token.lower().strip(string.punctuation) for token in nltk.word_tokenize(a) if
                token.lower().strip(string.punctuation) not in stopwords]
    tokens_b = [token.lower().strip(string.punctuation) for token in nltk.word_tokenize(b) if
                token.lower().strip(string.punctuation) not in stopwords]
    tokens_a = map(lemma.stem, tokens_a)
    tokens_b = map(lemma.stem, tokens_b)
    ratio = len(set(tokens_a).intersection(tokens_b)) / len(set(tokens_a))
    return (ratio >= threshold)
url = sys.argv[1]
page = urllib2.urlopen(url)
html_content = page.read()
h = html2text.HTML2Text()
rendered_content = h.handle( html_content.decode('utf8') )
client = MongoClient()
db = client.codic
out = db.coldb.find()
cnt = 1
for tuple in out:
    flg = 0
    sentout = []
    cooltext = tuple['coolabilities']
    sent_text = nltk.sent_tokenize(cooltext)
    for sent in sent_text:
        if is_ci_token_stopword_set_match(sent, rendered_content):
            flg = 1
            sentout.append(sent)
    if flg == 1:
        print tuple['disorder'], sentout
    cnt = cnt + 1