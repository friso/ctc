import bz2
import nltk
import re
import math
from collections import Counter


"""
Some global state here. Don't tell me about using globals. I know!
"""
document_frequencies = Counter()

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now', 'also', '']

def normed_tf_idf(term_frequencies, st):
    tf = term_frequencies[st] / float(max(term_frequencies.values()))
    idf = math.log((len(document_frequencies) or 1) / float(document_frequencies.get(st, 1)) + 1.0)
    return tf * idf

"""
Return the TDIDF score for each term in the given document.
Possibly update the global state.
"""
def get_tf_idf(document, update_state = False):
    tokenizer = nltk.RegexpTokenizer("\w+")
    stemmer = nltk.PorterStemmer()

    terms = filter(lambda t: t not in stopwords, tokenizer.tokenize(document))

    stemmed_to_terms = {}
    for term in terms:
        stem = stemmer.stem(term.lower())
        cnt = stemmed_to_terms.get(stem, Counter())
        cnt.update([term])
        stemmed_to_terms[stem] = cnt

    term_frequencies = Counter([stemmer.stem(t.lower()) for t in terms])

    if update_state:
        document_frequencies.update(stemmed_to_terms.keys())

    tf_idfs = [{ 'score':normed_tf_idf(term_frequencies, t), 'term':stemmed_to_terms[t].most_common(1)[0][0] } for t in term_frequencies.keys()]
    tf_idfs = sorted(tf_idfs, key = lambda x: x['score'], reverse = True)
    return tf_idfs

def extract_term_frequencies(tokens):
    result = {}
    for token in tokens:
        result[token] = result.get(token, 0) + 1
    return result

def init():
    print "loading... ",
    with file('corpus_1000.txt') as f:
        paragraph = ""
        for line in f.readlines():
            paragraph += line
            if line.strip() == "":
                get_tf_idf(paragraph, True)
                paragraph = ""
    print "done"
