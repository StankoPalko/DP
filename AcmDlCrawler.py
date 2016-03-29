import psycopg2
import re
import requests
from bs4 import BeautifulSoup
from time import sleep
from random import randint
import sys
from datetime import datetime
from datetime import timedelta
from os import listdir
from os.path import isfile, join

def get_doxloaded_files():
    mypath = "C:/Users/Stanko/PycharmProjects/DP/tmp"

    onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]

    file_numbers = []

    for file in onlyfiles:
        file_numbers.append(str(file.split(".")[0]))

    return file_numbers

def download_pdf(url,user_id,doc_id,folder_id,name,conn):

    #print("URL = ", url)
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    headings  = soup.findAll('h1',{'class':'mediumb-text'})
    title = headings[0].string
    #print("File name: ", title)

    #for link in soup.findAll('a'):
     #   href = link.get('href')
     #   name = link.string
        #print(name)
        #print(href)
        #print()
    file = False
    for link in soup.findAll('a',{'name':'FullTextPDF'}):
        href = link.get('href')

        #print(href)

        file_url = 'http://dl.acm.org/' + href
        response = requests.get(file_url)
        # re.sub(r'[^a-zA-Z\d\s:]', '', title) -> replaces all whitespaces
        with open('C:/Users/Stanko/PycharmProjects/DP/tmp/'+str(name)+'.pdf', 'wb') as f:
            f.write(response.content)
            f.close()
            file = True

    cur_2 = conn.cursor()
    try:
        cur_2.execute("INSERT INTO dp_data.dl_acm_documents (user_id,doc_id,folder_id,url,title,file_name,has_file) VALUES (%s, %s, %s, %s,%s, %s, %s)",(user_id, doc_id, folder_id, url,title,str(name),file))
    except:
        print(" Failed to insert")
    conn.commit()


#-----------------------------------------------------------------------------------------------------------------------
#start_date = datetime.now()

conn = psycopg2.connect(database="postgres", user="postgres", password="stankopalko", host="127.0.0.1", port="5433")
#print ("Opened database successfully")

base_url = 'http://dl.acm.org/citation.cfm?doid='

cur = conn.cursor()
cur.execute("SELECT doc.url,has.user_id,has.document_id,has.folder_id FROM documents doc join user_has_documents has ON  doc.id= has.document_id where doc.url LIKE '%dl.acm.org/cit%' and doc.url LIKE '%id=%'and not ( doc.url   LIKE '%springer%' Or doc.url  LIKE '%ieee%' Or doc.url  LIKE '%book%' or not  doc.url  ~ 'id=[0-9]') and has.folder_id is not NULL ORDER BY doc.url")
rows = cur.fetchall()

print ('Fetched rows: ' + str(len(rows)))

urls = []
doc_id = []
user_id = []
folder_id = []

for row in rows:

    match = re.search(r'^http://dl.acm.org/citation|^https://dl.acm.org/citation',row[0])

    if not match:
        #print ("WRONG URL = ", row[0])
        #print (str(row[0]).index('http://dl.acm'))
        index = str(row[0]).index('http://dl.acm')
        #print ("    GOOD URL =", str(row[0])[index:])
        urls.append(str(row[0])[index:])
    else :
        urls.append(str(row[0]))

    user_id.append(row[1])
    doc_id.append(row[2])
    folder_id.append(row[3])

#for user in user_id:
    #print ("user = ", user)

intialize = requests.get('http://dl.acm.org/')


#sys.exit()

#i = 928
file_name = 1944

for i in range(951,len(urls)):

    print (str(i)+ ". " + urls[i])
    download_pdf(urls[i],user_id[i],doc_id[i],folder_id[i],file_name,conn)
    i += 1
    file_name += 1
    print()
    sleep(randint(5,8))

    #end_date = datetime.now()
    #time_difference = end_date - start_date
    #time_difference_in_minutes = time_difference / timedelta(minutes=1)

    #if time_difference_in_minutes > 2:
    #    start_date = datetime.now()

    print ()
    #print (time_difference_in_minutes)