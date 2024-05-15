import json
import time
import datetime
import requests
import smtplib
import pymongo
import certifi



client = pymongo.MongoClient("mongodb+srv://root:root@cluster0.yfjkznw.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tlsCAFile=certifi.where())
db = client["db"]
col = db["bucketList"]

headers = {
        "Accept":"application/json, text/plain, */*",
        "Content-Type":"application/json",
        "Content-Length": "10000",
        "User-Agent":"PostmanRuntime/7.37.3"
}

my_email =  "getvaccinated3@gmail.com"
password = "sxyo snbr wpxh nozw"

def getdate():
    return datetime.datetime.today().strftime('%d-%m-%Y')
    
def getrequest(productId):
    URL = "https://opsg-api-in.oppo.com/mall/product/page/detail/fetch"
    data = {
        "productCode": productId,
        "storeViewCode": "in",
        "storeCode": "in",
        "configModule": 3,
        "countryCode": "IN",
        "deviceType": 2
    }

    response = requests.post(URL, headers=headers, data=json.dumps(data))
    return response.json()


def get_List(x, dic):
    for i in x:
        r = getrequest(i['pincode'])
        print("checked for: " + i['email'])
        message = '\n Phone available at :'
        flag, count = False, 1
        if 'error' in r:
            continue
        for j in r['data']['mainSkuList']:
            if j['outStock']==False:
                flag = True
                message += '\n{}.) Product Name -  {}'.format(count, j['skuName'])
                count+=1
        if flag and i['email'] not in dic:
            send_mail(i['email'], message)

def send_mail(email, message):
    SUBJECT = "Product available"
    mess = 'Subject: {}\n\n{}'.format(SUBJECT, message)
    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(my_email, password)
    s.sendmail(my_email,email, mess)
    s.quit()
    print("mail sent to "+email)
    dic[email] = None

c, dic = 0, {}
while True:
    x = col.find()
    get_List(x, dic)
    c+=1
    time.sleep(10)
    if c == 600:
      c = 0
      dic = {}