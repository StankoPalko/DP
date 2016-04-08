import scipy.sparse
from sklearn import cross_validation

import DataGetterOld
import DataGetter
from scipy.sparse import hstack
import numpy as np
import scipy.sparse
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import PassiveAggressiveClassifier
from sklearn.linear_model import Perceptron
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import MultinomialNB
import psycopg2

import  sklearn.metrics as metric
##########################################################################
def get_users():

    users = []

    conn = psycopg2.connect(database="postgres", user="postgres", password="stankopalko", host="127.0.0.1", port="5433")
    #print ("Opened database successfully")

    base_url = 'http://dl.acm.org/citation.cfm?doid='

    cur = conn.cursor()
    cur.execute("SELECT user_id, count(*) FROM (SELECT user_id,folder_id,count(folder_id) as pocet FROM dp_data.dl_acm_documents where has_file = true group by user_id,folder_id order by user_id) data where pocet > 1 group by user_id having count(*) > 1")
    rows = cur.fetchall()

    for row in rows:
        users.append(row[0])

    return users

def test_user(user):

    texts,text_classes,text_ids = DataGetter.get_user_data(user)

    count_vect = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer()
    X_train_counts = count_vect.fit_transform(texts)
    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    train_features = X_train_tfidf

    classifiers = []

    PA = PassiveAggressiveClassifier()
    Percep = Perceptron()
    SVM = LinearSVC()
    NB = MultinomialNB(alpha=0.001)
    RF = RandomForestClassifier(n_estimators=1000)
    AB = AdaBoostClassifier(n_estimators=10)

    classifiers.append(Percep)
    classifiers.append(PA)
    classifiers.append(SVM)
    classifiers.append(NB)
    classifiers.append(RF)
    classifiers.append(AB)

    total_acc = []

    loo = cross_validation.LeaveOneOut(len(texts))

    for clf in classifiers:
        was_right = cross_validation.cross_val_score(clf, train_features,text_classes, cv=loo)
        total_acc.append(np.mean(was_right))

    print(total_acc)
    return total_acc

users = get_users()

print (users)

acs = []

for user in users:
    acs.append(test_user(user))

for ac in acs:
    myFormattedList = [ '%.2f' % elem for elem in ac ]
    print(myFormattedList)


