import requests
import datetime
from flask import Flask, render_template, request, jsonify
import json
import pymongo
import certifi

app = Flask(__name__, static_url_path='/static')
mongo = pymongo.MongoClient("mongodb+srv://root:root@cluster0.yfjkznw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tlsCAFile=certifi.where())
@app.route('/')
def home():
    return render_template('newsletter.html')    

@app.route('/addemail', methods=["GET", "POST"])
def addemail():
    if request.method == "POST":
        bucketList = mongo.db.bucketList
        jso = {'productId':request.form['ProductId'], "number": '', 'email':request.form['email']}
        if bucketList.find(jso).count() == 0:
            bucketList.insert(jso)
            print("Inserted")
            return render_template('newsletter.html')
        else:
            return render_template('newsletter.html')
    else:
        return render_template('newsletter.html')


    
if __name__ == '__main__':
    app.run()
