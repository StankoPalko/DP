import re
import requests
from bs4 import BeautifulSoup
from time import sleep
import psycopg2
from random import randint

def get_data(cur):

    cur.execute("select tab.doc_id,tab.url from dp_data.dl_acm_documents tab where tab.has_file = true")
    rows = cur.fetchall()

    return rows
#---------------------------------------------------------

conn = psycopg2.connect(database="postgres", user="postgres", password="stankopalko", host="127.0.0.1", port="5433")
cur = conn.cursor()
rows = get_data(cur)


flat = "&preflayout=flat#CIT"

index = 0
for row in rows:

    url = row[1]
    doc_id = row[0]

    if "#references" in url:
        url = url[:url.index("#references")]

    url = url + flat
    print(str(index)+". "+url)
    index +=1

    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)

    headings = soup.findAll('span',{'class':'heading'})
    refIndef = 1

    for heading in headings:

        if heading.text.lower() == 'references':
            break
        refIndef += 1

    authors  = soup.findAll('a', {'title':re.compile("^author")})
    for author in authors:
        cur.execute ("INSERT INTO dp_data.dl_acm_doc_authors (doc_id,aut_name) VALUES (%s, %s)",(doc_id, author.text))
        conn.commit()
        print(author.text)

    citations = soup.findAll('div',{'class':'flatbody'})
    cit = citations[refIndef].findAll('div')
    i = 1

    reference = ""

    for c in cit:
        ref = c.findAll('a')

        if(len(ref) > 0):
            print(str(i)+ ". " + ref[0].text.strip())
            reference = ref[0].text.strip()
            cur.execute ("INSERT INTO dp_data.dl_acm_doc_references (doc_id,reference) VALUES (%s, %s)",(doc_id, reference))
            conn.commit()
        else:
            if not c.text.strip().isdigit():
                print(str(i)+ ". " + c.text.strip())
                reference = c.text.strip()
                cur.execute ("INSERT INTO dp_data.dl_acm_doc_references (doc_id,reference) VALUES (%s, %s)",(doc_id, reference))
                conn.commit()
        i += 1


    sleep(randint(2,5))