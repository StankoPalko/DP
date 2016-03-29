import numpy as np

categories = ['alt.atheism', 'soc.religion.christian',
         'comp.graphics', 'sci.med']

from sklearn.datasets import fetch_20newsgroups

twenty_train = fetch_20newsgroups(
     subset='train', categories=categories,
     shuffle=True, random_state=42)

# data -> fulltext
#file_names -> nazvy suborou
#targetnames -> nazvy kategrii
#target -> kategorie pre jednotlive dokumenty

#print(twenty_train.target_names)

#for i in range(len(twenty_train.target)):
#    if (twenty_train.target[i] == 2) :
#       print(twenty_train.filenames[i])



def print_a(pocet):
    for t in twenty_train.target[:int(pocet)]:
        print (twenty_train.target_names[t])
        print (twenty_train.filenames[t])
        print (twenty_train.data[t])
    return

from sklearn.feature_extraction.text import CountVectorizer

count_vect = CountVectorizer(stop_words='english')
X_train_counts = count_vect.fit_transform(twenty_train.data)
print(X_train_counts.shape)
print (count_vect.vocabulary_.get(u'algorithm'))
print (X_train_counts[0])

from sklearn.feature_extraction.text import TfidfTransformer
tfidf_transformer = TfidfTransformer()
X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)

print (X_train_tfidf[0])

twenty_test = fetch_20newsgroups(
subset='test', categories=categories,
shuffle=True, random_state=42)

docs_test = twenty_test.data
docs_test = count_vect.transform(docs_test)
docs_test = tfidf_transformer.transform(docs_test)

from sklearn.naive_bayes import MultinomialNB
NBclf = MultinomialNB().fit(X_train_tfidf, twenty_train.target)
#-----------------------------------------------------------------------------

docs_new = ['God is love', 'OpenGL on the GPU is fast','Path: cantaloupe.srv.cs.cmu.edu!das-news.harvard.edu!noc.near.net!howland.reston.ans.net!usenet.ins.cwru.edu!cleveland.Freenet.Edu!bj368 From: bj368@cleveland.Freenet.Edu (Mike E. Romano) Newsgroups: sci.med Subject: Re: Drop your drawers and the doctor will see you Date: 3 May 1993 06:40:18 GMT Organization: Case Western Reserve University, Cleveland, Ohio (USA) Lines: 11 Message-ID: <1s2eoi$i8o@usenet.INS.CWRU.Edu> NNTP-Posting-Host: hela.ins.cwru.edu   This is not an unusual practice if the doctor is also a member of a nudist colony.    --  Sir, I admit your genral rule That every poet is a fool; But you yourself may serve to show it, That every fool is not a poet.    A. Pope ']
X_new_counts = count_vect.transform(docs_new)
X_new_tfidf = tfidf_transformer.transform(X_new_counts)

#predicted = NBclf.predict(X_new_tfidf)
predicted = NBclf.predict(docs_test)
print(np.mean(predicted == twenty_test.target))

#for doc, category in zip(docs_new, predicted):
 #   print ('%r => %s' % (doc, twenty_train.target_names[category]))

from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC

#classif = OneVsRestClassifier(SVC(kernel='linear'))
#classif.fit(X_train_tfidf, twenty_train.target)
#predicted = classif.predict(X_new_tfidf)

#for doc, category in zip(docs_new, predicted):
  #  print ('%r => %s' % (doc, twenty_train.target_names[category]))


#predicted = classif.predict(docs_test)
#print(np.mean(predicted == twenty_test.target))
print("Tu sa inkluduje")
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import Perceptron

PA = PassiveAggressiveClassifier()
Percep = Perceptron()

print("Tu je PA")
Percep.fit(X_train_tfidf, twenty_train.target)
predicted = Percep.predict(docs_test)
print(np.mean(predicted == twenty_test.target))

PA.fit(X_train_tfidf, twenty_train.target)
predicted = PA.predict(docs_test)
print(np.mean(predicted == twenty_test.target))

