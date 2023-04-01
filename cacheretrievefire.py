import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import firestore
import hashlib

if not firebase_admin._apps:
#Fetch the service accound key JSON file contents
    cred = credentials.Certificate('jyothish-cache-firebase-adminsdk-dnwk6-69bbb02424.json')

    #Initialize the app with a service account, granting admin privilages 
    firebase_admin.initialize_app(cred)

    db = firestore.client()

def RetrieveCache(query):

    query_encrpt = hashlib.md5(query.encode('utf-8')).hexdigest()

    doc_ref = db.collection(u'cache-query').document(query_encrpt)
    doc = doc_ref.get()
    response  = doc.get("response")
    print(str(response))
    if response==None:
        return ""
    else:
        return response

def Storeuserquery(query,response):
    #Encrypt the query before writing to firestore
    query_encrpt = hashlib.md5(query.encode('utf-8')).hexdigest()
    print(str(query_encrpt))
    data = {
            u'query' : query,
            u'response' : response
    }

    # Add a new doc in collection Bot_Users
    db.collection('user-queries').document(str(query_encrpt)).set(data)
    print('Record Added Successfully')
