from os import listdir
from os.path import isfile, join
import psycopg2
import re
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import sys

def download_pdf(url,name,conn,cur):


    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    headings  = soup.findAll('h1',{'class':'mediumb-text'})
    title = headings[0].string

    for link in soup.findAll('a',{'name':'FullTextPDF'}):
        print("Dondload")
        href = link.get('href')

        file_url = 'http://dl.acm.org/' + href
        print(file_url)
        response = requests.get(file_url)
        print(response.status_code)
        print(len(response.content))

        file = False
        with open('C:/Users/Stanko/PycharmProjects/DP/tmp/'+str(name)+'.pdf', 'wb') as f:
            try:
                print("Writing to file: C:/Users/Stanko/PycharmProjects/DP/tmp/" +str(name)+ ".pdf")
                f.write(response.content)
                f.close()
                file = True
            except :
                print ("Error")
        if file:
            cur.execute("UPDATE dp_data.dl_acm_documents SET has_file = true WHERE file_name = " + "'" + str(name) + "'")
            conn.commit()
#-----------------------------------------------------------------------------------------------------------------------

mypath = "C:/Users/Stanko/PycharmProjects/DP/tmp"

onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

file_numbers = []
missing_file_numbers = []

for file in onlyfiles:
    file_numbers.append(int(file.split(".")[0]))

conn = psycopg2.connect(database="postgres", user="postgres", password="stankopalko", host="127.0.0.1", port="5433")
cur = conn.cursor()
cur.execute("select tab.file_name from dp_data.dl_acm_documents tab where tab.has_file = false")
rows = cur.fetchall()

print(len(rows))

for row in rows:
    missing_file_numbers.append(row[0])

print (missing_file_numbers)


intialize = requests.get('http://dl.acm.org/')

for i in range(len(missing_file_numbers)):

    print (str(i) + ": " +missing_file_numbers[i])
    cur.execute("SELECT url FROM dp_data.dl_acm_documents tab where tab.file_name = "+ "'" + missing_file_numbers[i] + "'")
    rows = cur.fetchall()

    url = rows[0][0]
    print(url)

    download_pdf(url,missing_file_numbers[i],conn,cur)
    sleep(randint(5,8))
    print("-------------------------------------------------------------------------------")
