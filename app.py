#create a flask app
from flask import Flask, request, jsonify
import requests as rq
import wikipedia as wk 
app = Flask(__name__)

CA_TERR_URL = "https://native-land.ca/api/?maps=territories&position="
CA_LANG_URL = "https://native-land.ca/api/?maps=languages&position="
CA_TREAT_URL = "https://native-land.ca/api/?maps=treaties&position="

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
    return '<h1>Homee</h2>'

@app.route('/coord',methods=['POST'])
def post():
    if request.method == 'POST':
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
if __name__ == '__main__':
    app.run(debug=True)