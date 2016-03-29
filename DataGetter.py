import psycopg2
from sklearn.cross_validation import train_test_split

def get_file_text(name):
    path = "C:/Users/Stanko/PycharmProjects/DP/fulltexts/"+name+".txt"
    with open(path) as f:
        text = f.read()
    return text

def get_user_data(number):

    conn = psycopg2.connect(database="postgres", user="postgres", password="stankopalko", host="127.0.0.1", port="5433")
    cur = conn.cursor()

    cur.execute("SELECT folder_id FROM dp_data.dl_acm_documents where has_file = true and user_id = "+str(number)+" group by user_id,folder_id Having count (folder_id) > 1 order by user_id")
    rows = cur.fetchall()

    folder_ids = ""

    for row in rows:
        folder_ids = folder_ids + str(row[0]) + ","
    folder_ids = folder_ids[:-1]

    cur.execute("SELECT * FROM dp_data.dl_acm_documents where user_id = "+str(number)+" and has_file = true and folder_id in (" + folder_ids +")")
    rows = cur.fetchall()

    classes = []
    fulltexts = []

    for row in rows:
        classes.append(row[2])
        fulltexts.append(get_file_text(row[5]))

    print (len(classes))
    print (len(fulltexts))

    X_train, X_test, y_train, y_test = train_test_split( fulltexts, classes, test_size=0.33)

    return X_train, X_test, y_train, y_test