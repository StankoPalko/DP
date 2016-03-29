import scipy.sparse
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




def print_metrics(true,predicted):
    print("Real: " + str(true))
    print("Predicted: " + str(predicted))

    print("Precision: " + str(metric.precision_score(true,predicted,average = 'macro')))
    print("Recall: " + str(metric.recall_score(true,predicted,average = 'macro')))
    print("Accuracy: " + str(metric.accuracy_score(true,predicted)))
    print("F1: " + str(metric.f1_score(true,predicted,average = 'macro')))
    print("-----------------------------------------------------------------------------------------------------------")

def test_user(user):

    accuracy = []
    train_data,test_data,train_labels,test_labels = DataGetter.get_user_data(user)

    #train_data =  DataGetterOld.data("TRAIN")
    #test_data =  DataGetterOld.data("TEST")

    PA = PassiveAggressiveClassifier()
    Percep = Perceptron()
    SVM = LinearSVC()
    NB = MultinomialNB(alpha=0.001)
    RF = RandomForestClassifier(n_estimators=1000)
    AB = AdaBoostClassifier(n_estimators=10)

    count_vect = CountVectorizer(stop_words='english')
    tfidf_transformer = TfidfTransformer()

    X_train_counts = count_vect.fit_transform(train_data)
    X_test_counts = count_vect.transform(test_data)

    X_train_tfidf = tfidf_transformer.fit_transform(X_train_counts)
    #x = np.hstack((X_train_tfidf.toarray(),train_data.vectors.toarray()))
    #train_features = scipy.sparse.csr_matrix(x)
    train_features = X_train_tfidf

    X_test_tfidf = tfidf_transformer.transform(X_test_counts)
    #x = np.hstack((X_test_tfidf.toarray(),test_data.vectors.toarray()))
    #test_features = scipy.sparse.csr_matrix(x)
    test_features = X_test_tfidf

    ###print(X_train_tfidf.shape)
    ###print(X_test_tfidf.shape)

    ###print("Perceptron")
    Percep.fit(train_features, train_labels)
    predicted = Percep.predict(test_features)
    #print_metrics(test_labels,predicted)
    accuracy.append(metric.accuracy_score(test_labels,predicted))

    ###print("Passive Agressive")
    PA.fit(train_features,  train_labels)
    predicted = PA.predict(test_features)
    #print_metrics(test_labels,predicted)
    accuracy.append(metric.accuracy_score(test_labels,predicted))

    ###print("SVM")
    SVM.fit(train_features,  train_labels)
    predicted = SVM.predict(test_features)
    #print_metrics(test_labels,predicted)
    accuracy.append(metric.accuracy_score(test_labels,predicted))

    ###print("Naive Bayes")
    NB.fit(train_features,  train_labels)
    predicted = NB.predict(test_features)
    #print_metrics(test_labels,predicted)
    accuracy.append(metric.accuracy_score(test_labels,predicted))

    ###print("RF")
    RF.fit(train_features,  train_labels)
    predicted = RF.predict(test_features)
    #print_metrics(test_labels,predicted)
    accuracy.append(metric.accuracy_score(test_labels,predicted))

    ###print("AB")
    AB.fit(train_features,   train_labels)
    predicted = AB.predict(test_features)
    #print_metrics(test_labels,predicted)
    accuracy.append(metric.accuracy_score(test_labels,predicted))

    print("User: " + str(user))
    print(accuracy)
    print()

    return accuracy


users = get_users()

print (users)

#test_user(user)

acs = []

for user in users:
    acs.append(test_user(user))

for ac in acs:
    myFormattedList = [ '%.2f' % elem for elem in ac ]
    print(myFormattedList)
