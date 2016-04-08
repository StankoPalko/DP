# http://stackoverflow.com/questions/15173225/how-to-calculate-cosine-similarity-given-2-sentence-strings-python
import re, math
from collections import Counter

WORD = re.compile(r'\w+')

def get_cosine(vec1, vec2):
     intersection = set(vec1.keys()) & set(vec2.keys())
     numerator = sum([vec1[x] * vec2[x] for x in intersection])

     sum1 = sum([vec1[x]**2 for x in vec1.keys()])
     sum2 = sum([vec2[x]**2 for x in vec2.keys()])
     denominator = math.sqrt(sum1) * math.sqrt(sum2)

     if not denominator:
        return 0.0
     else:
        return float(numerator) / denominator

def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

text1 = 'Peng Yan , Wei Jin, Mining semantic relationships between concepts across documents incorporating wikipedia knowledge, Proceedings of the 13th international conference on Advances in Data Mining: applications and theoretical aspects, p.70-84, July 16-21, 2013, New York, NY, USA'
text2 = 'Gaël Dias , Raycho Mukelov , Guillaume Cleuziou, Fully unsupervised graph-based discovery of general-specific noun relationships from web corpora frequency counts, Proceedings of the Twelfth Conference on Computational Natural Language Learning, August 16-17, 2008, Manchester, United Kingdom'

vector1 = text_to_vector(text1)
vector2 = text_to_vector(text2)

cosine = get_cosine(vector1, vector2)

print (str(cosine))