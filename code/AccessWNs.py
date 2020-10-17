import nltk
from nltk.corpus import WordNetCorpusReader
wn2 = WordNetCorpusReader("/Users/gary/Documents/perl/package/WordNet-2.1/dict", nltk.data.find("/Users/gary/Documents/perl/package/WordNet-2.1/dict"))

wn16 = WordNetCorpusReader("/Users/gary/Documents/NLP/WordNetVersions/wordnet-1.6/dict", nltk.data.find("/Users/gary/Documents/NLP/WordNetVersions/wordnet-1.6/dict"))

print(wn16.get_version())
