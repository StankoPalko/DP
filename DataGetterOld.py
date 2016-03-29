import os.path
import numpy as np
from scipy.sparse import csr_matrix
from scipy import sparse
from os import walk
import codecs

def get_texts(scenario):


    path = 'C:/Users/Stanko/PycharmProjects/DP/'+scenario+' FILES/Texts'

    #files = []
    #for (dirpath, dirnames, filenames) in walk(path):
    #    files.extend(filenames)
    #    break

    if scenario == "TRAIN":
        opp = 'textak'
    else:
        opp = 'textak2'

    with open(opp) as f:
        files = f.read().splitlines()

    #files = files.sort()
    texts = []

    for file_name in files:
        #print (file_name)
        with codecs.open(path + "/" + file_name,'r',encoding='utf8') as f:
            text = f.read()

        #file = open ( path + "/" + file_name, 'r')
        #text = file.read()

        texts.append(text)

    return texts

def get_vectors(scenario):

    path = 'C:/Users/Stanko/PycharmProjects/DP/'+scenario+' FILES/vectors.txt'

    with open(path) as f:
        classes = f.read().splitlines()
        classes_strings = [ list(vector)for vector in classes]

    for i in range(len(classes_strings)):
        classes_strings[i] = [int(numeric_string) for numeric_string in classes_strings[i]]

    return sparse.csr_matrix(classes_strings)

def get_classes(scenario):
    path = 'C:/Users/Stanko/PycharmProjects/DP/'+scenario+' FILES/text_classes.txt'

    with open(path) as f:
        classes = f.read().splitlines()

    classes_int = [int(numeric_string) for numeric_string in classes]
    return np.array(classes_int)

def get_class_names(scenario):
    path = 'C:/Users/Stanko/PycharmProjects/DP/'+scenario+' FILES/class_names.txt'

    with open(path) as f:
        class_names = f.read().splitlines()

    return class_names

class data():

     def __init__(self,scenario):
         self.data = get_texts(scenario)
         self.target = get_classes(scenario)
         self.target_names = get_class_names(scenario)
         self.vectors = get_vectors(scenario)


