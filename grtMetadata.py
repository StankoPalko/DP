import re
import requests
from bs4 import BeautifulSoup
from time import sleep
import psycopg2
from random import randint
import operator
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk,string
import  DataGetter
import Cosine

def get_metadata(user_id):

    ids = DataGetter.get_user_data(user_id)[2]

    conn = psycopg2.connect(database="postgres", user="postgres", password="stankopalko", host="127.0.0.1", port="5433")
    cur = conn.cursor()

    ids_string = "("

    for id in ids:
        ids_string = ids_string + str(id) + ","

    ids_string = ids_string[:-1]+")"
    print(ids_string)

    cur.execute("select * from dp_data.dl_acm_doc_references tab where tab.doc_id IN " + ids_string)
    reference_rows = cur.fetchall()
    #print ("Pocet referencii:" + str(len(reference_rows)))

    cur.execute("select * from dp_data.dl_acm_doc_authors tab where tab.doc_id IN " + ids_string)
    author_rows = cur.fetchall()
    #print (len(authors))

    autorovi = {}
    index = 0
    docs = []
    doc_autors = {}
    a = 0
    for aut in author_rows:
        docs.append(aut[0])

        if  not autorovi.__contains__(aut[1]):
            autorovi[aut[1]] = index;
            index+=1

        if  not doc_autors.__contains__(aut[0]):
            doc_aut = []
            doc_aut.append(aut[1])
            doc_autors[aut[0]] = doc_aut
            a+=1
        else:
            doc_autors[aut[0]].append(aut[1])
            a+=1

    #print("toto je A:" + str(a))
    doc_set = set(docs)
    docs = list(doc_set)

    #print (len(autorovi))
    #sorted_x = sorted(autorovi.items(), key=operator.itemgetter(1))

    zeros = [0] * len(autorovi)

    for key, value in doc_autors.items():
        zeros = [0] * len(autorovi)
        for val in value:
            zeros[autorovi[val]] = 1
        doc_autors[key] = zeros
        #print(zeros)
    #end of author vector string-----------------------------------------------------------------------------------------------------------

    #--------------Not my code

    stemmer = nltk.stem.porter.PorterStemmer()
    remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

    def stem_tokens(tokens):
        return [stemmer.stem(item) for item in tokens]

    '''remove punctuation, lowercase, stem'''
    def normalize(text):
        return stem_tokens(nltk.word_tokenize(text.lower().translate(remove_punctuation_map)))

    vectorizer = TfidfVectorizer(tokenizer=normalize, stop_words='english')

    def cosine_sim(text1, text2):
        tfidf = vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0,1]

    def is_in_dictionary(referencie,text):

        for value in referencie:
            if cosine_sim(value,text) > 0.5 :
                return True
        return False

    unique_refernces = []
    doc_references = {}

    index = 0
    for ref in reference_rows:

        if  not doc_references.__contains__(ref[0]):
            doc_ref = []
            doc_ref.append(ref[1])
            doc_references[ref[0]] = doc_ref
        else:
            doc_references[ref[0]].append(ref[1])

        #print(index)
        #if is_in_dictionary(unique_refernces,ref[1]):
        #    continue
        #else:
        #    unique_refernces.append(ref[1])
        #index += 1

    #print("Dlzka referencii: " + str(len(unique_refernces)))

    #print("Counting ref lenghts")

    for key, value in doc_references.items():
        zeros = [0] * len(reference_rows)
        for val in value:
            index = 0
            for ref in reference_rows:
                #print(cosine_sim(val,ref[1]))
                #print(Cosine.get_cosine(Cosine.text_to_vector(val),Cosine.text_to_vector(ref[1])))
                #if cosine_sim(val,ref[1]) > 0.5 :
                if Cosine.get_cosine(Cosine.text_to_vector(val),Cosine.text_to_vector(ref[1])) > 0.5 :
                    zeros[index] = 1
                index += 1
        doc_references[key] = zeros

    final_vectors = {}

    for key, value in doc_references.items():
        final_vectors[key] = doc_references[key] + doc_autors[key]

    print(len(final_vectors))
    return final_vectors












