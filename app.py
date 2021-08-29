#create a flask app
from flask import Flask, request, jsonify,render_template,redirect,url_for
import requests as rq
import wikipedia as wk 
from firebase_admin import credentials, firestore, initialize_app


app = Flask(__name__)


CA_TERR_URL = "https://native-land.ca/api/?maps=territories&position="
CA_LANG_URL = "https://native-land.ca/api/?maps=languages&position="
CA_TREAT_URL = "https://native-land.ca/api/?maps=treaties&position="


# Initialize Firestore DB
cred = credentials.Certificate({
  "type": "service_account",
  "project_id": "kurius-b1fb6",
  "private_key_id": "9f75b343e13e0d60c11fac8dc50df69e37d3b9fc",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQC76F7gFZ08RCt6\nxs2ovd8vjTZn7y5L3yFYY3OPMlHKOz+INocfMvtjDj8xaO6xuHf/WYrVRG4JtVuZ\nYVqK55C5/IEtSalqLsjwDVdFJZrLlPdAR4oY8qW/LDFacAkzpWIavPtRc7QvPqSX\nDJ5gURgvgU17hi/sSQ1ye6+BVpFduduOA9ZwBLqNRzUn9XIbdHYA6L87TiJw6zch\n3txv93O3OzA33jPOco8/++uRSZTxNUdBBocsmhwfOpMhU5ca0Ftp0cfMa/SWYiSn\naKavT5Guj3vN7cpLKqcg6brT2FupwHZmENPhbOl4Wvcl+JIYGj1s0unxfGdNFwZN\nKxwU08d3AgMBAAECggEAAIpcD3/walZ1244L1GLra+sXj3f4JZ64LVVn5S8LXi4K\ncj1Z6SSP5YqKcv1uxlMWAUWEKTXfrSZ443mMtZ6R438O7g7qrlQBHvOi3x+LEO/W\nQDiUdJrqECEz6SMuW5grrpEBlgvjpkkjVw3hvLwu+iAAlYzewWq6X6xsZk5V77OS\nYnK7SgmDEoplWXMhvEbhc+yO6GLu8zcOHyb7mJJS2bQ21Vr8+sR7lhfop7ZL6kqj\npi5LPhJ3xlPFpNSQRk3aDs3PfGb0DWBTk37hLE/5FpvoyGPQL7EhZUse3r5Fjmci\nNXLvk8tiKgBdl4lX+Nagc1B/CgPDvNXKj5Ae+exyVQKBgQDupAYyb8p944DRwkDg\nRNk+7esjx8dx+tOEkPz9pJ//kzlcPZ1JZezl0T2vLX1Af7v98ciRpF9BqWq1rjpB\nqm2RYGx//ilzjcqodxXMQlSxIl0r6IJftW1xvX52ZIP1oGs3MAGRDaoatW+d1Bp6\naBTUClgD47m+3H30pRM3ZTqf6wKBgQDJk5gj+bT+zHMD3JBUK1RIUMTLvRQnF7K9\n0/dDOBkWZRuUu1g6MDZpf7nS+UDz5jIRMXD93NMq3aRyBX2wnFomLOKCmATF2Tkp\nlj2S3YDIq2+Stx05AfTFcwPUk844TaieKlHFkfJlqm709D8vNPrVbsZ4tm4dGaQT\nNnInK/ffpQKBgHNU0C3l+y3WGnbFc8cvXvLb1w1GyuwZ9cmWrL4EptLEmy8qE+7a\nFKCI/E/CI0tdsEQtauqATw0TzJ+bYUpFDIj62dUNx4iyGSRL0TwTPo0Q94h16TRK\nIWeb1hdvwpqd+dMFH2yz9ubLkvLrBBTuYkqL6TeQAj/sne7zLJNUF/4bAoGAFRGq\nO0hkVKWF+AdbxpBo1M4sY6c1rghaFGFNXOdGKAMVaOxUAnD7nvdMsvJ+iX+sCAQE\n7WPhZn+YKprMUmNlQMw8OK4vAYb85I3hjbI9Pbw9gzZEhargrKqi4ds5GMV1NGLz\n/RSOI3Y29r94wzRka16SvBdFVyFQ9vkf4VxFIkkCgYBJKYJfMaoWPzTqBhP1BRHL\nZxUvAuFEPiOsjvu+a1QuEbMF3GFHfsDiZT4a5ycol4ZSKLdD5Q59agOIdACUOTjx\nHHwaedKlGwAgt5r38RgTTkEUQgrK/cBRnTAhXKZkdLU6ZPPMs74JWIlWGOBeWmAa\nSRTMooKGTYqhDsqPksK6Sg==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-yzwuu@kurius-b1fb6.iam.gserviceaccount.com",
  "client_id": "103923078493677214728",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-yzwuu%40kurius-b1fb6.iam.gserviceaccount.com"
}
)
default_app = initialize_app(cred)
db = firestore.client()
verified_ref = db.collection('verified')
pending_ref = db.collection('pending')


def terr_parse(data):
    if data==[]:
        return []
    liTerrs=[]
    for d in data:
        liTerrs.append(d['properties']['Name'])
    return liTerrs

#create a route for the index page
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/getCoord',methods=['GET'])
def post():
    if request.method == 'GET':
        lati =(request.get_json()["lat"])
        longi = (request.get_json()["long"])
        res1=rq.get(CA_TERR_URL+str(lati)+","+str(longi))
        res2=rq.get(CA_LANG_URL+str(lati)+","+str(longi))
        res3=rq.get(CA_TREAT_URL+str(lati)+","+str(longi))
        result={}
        result['territories']=terr_parse(res1.json())
        result['languages']=terr_parse(res2.json())
        result['laws']=terr_parse(res3.json())
        return jsonify(result)

@app.route('/summary', methods=['GET'])
def terr_wiki():
    val=request.args.get("q")
    result={}
    result['summary']=wk.summary(val,sentences=5)
    return jsonify(result)
    


#admin functions 
#templates
def getAll():
    all_todos = [doc.to_dict() for doc in pending_ref.stream()]
    return all_todos

def moveTo(q):
        data = pending_ref.document(q).get()
        verified_ref.document(q).set(data.to_dict())
        pending_ref.document(q).delete()
        return jsonify({"msg":"success"})

@app.route('/getData',methods=['GET'])
def getData():
    all_todos = [doc.to_dict() for doc in verified_ref.stream()]
    return jsonify(all_todos), 200
    
@app.route('/admin',methods=['GET','POST'])
def admin():
    if request.method == 'POST':
        latLong=request.form.get("lat")

        print(latLong)
    
        moveTo( latLong)
    return render_template('admin.html',data=getAll())

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        user = request.form['user']
        passw = request.form['password']
        if user=='admin' and passw=='admin':
            return redirect(url_for('admin'))   
    return render_template('login.html')


@app.route('/addData',methods=['POST'])
def addData():
    if request.method == 'POST':
        data=request.get_json()
        print(data)
        pending_ref.document(data["lat"]).set(data)
        return jsonify({"msg":"success"})
    
if __name__ == '__main__':
    app.run(debug=True)