import nltk
import re
import math
from collections import Counter


"""
Some global state here. Don't tell me about using globals. I know!
"""
document_frequencies = Counter()
document_count = 0

stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(['also', ''])



"""
Return the TDIDF score for each term in the given document.
Possibly update the global state.
"""
def get_tfidf(document, update_state = False):
	tokenizer = nltk.RegexpTokenizer("\w+")
	stemmer = nltk.PorterStemmer()



	terms = map(lambda w: (w, stemmer.stem(w.lower())), filter(lambda t: t not in stopwords, tokenizer.tokenize(document)))
	term_frequencies = Counter(map(lambda x: x[1], terms))
	document_frequencies.update(map(lambda x: x[1], terms))

	#tfidf with normed tf
	result = map(lambda t: (t[0], t[1], (term_frequencies[t[1]] / float(max(term_frequencies.values()))) * (math.log(len(document_frequencies)) / float(document_frequencies[t[1]]))), terms)
		


def extract_term_frequencies(tokens):
	result = {}
	for token in tokens:
		result[token] = result.get(token, 0) + 1
	return result
