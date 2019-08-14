import requests
import hashlib
import sys
import time
import json

def generatefbtoken(id,password):
    pwd = password
    API_SECRET = '62f8ce9f74b12f84c123cc23437a4a32'
    data = {
        "api_key":"882a8490361da98702bf97a021ddc14d",
        "credentials_type":"password",
        "email":id,
        "format":"JSON", 
        "generate_machine_id":"1",
        "generate_session_cookies":"1",
        "locale":"en_US",
        "method":"auth.login",
        "password":pwd,
        "return_ssl_resources":"0",
        "v":"1.0"
        }
    sig = 'api_key=882a8490361da98702bf97a021ddc14dcredentials_type=passwordemail='+id+'format=JSONgenerate_machine_id=1generate_session_cookies=1locale=en_USmethod=auth.loginpassword='+pwd+'return_ssl_resources=0v=1.0'+API_SECRET
    x = hashlib.new('md5')
    x.update(sig.encode('utf-8'))
    # x.update(sig)
    data.update({'sig':x.hexdigest()})
    # return data
    r = requests.get('https://api.facebook.com/restserver.php',params=data)
    jsondata = r.json()
    # print(jsondata)
    try:
        token = jsondata["access_token"]
        return token 
    except Exception as err:
        print(jsondata["error_msg"])
        # sys.exit(err)
    # return token

def getemailfriendfb(token):
    arrayemail = []
    url = "https://graph.facebook.com/v3.2/me/friends/?fields=name,email&access_token="+token+"&limit=5000"
    r = requests.get(url)
    frindsobj = r.json()
    datas = frindsobj["data"]
    for data in datas:
        try:
            arrayemail.append(data["email"])
        except Exception:
            pass
    
    return arrayemail

def emailvalid(email):

if __name__ == '__main__':
   token = generatefbtoken('akubukanhejes','Systemcodedx(^_^)321~~~~Q~1')
   if token is None:
       sys.exit("INVALID TOKEN")
   list_email = getemailfriendfb(token)
   count = 0
   for email in list_email:
       if '@yahoo' in email:
            print(email)

            # emailvalid(email)
            # count+=1
            # # time.sleep(2)
            # # if(count==10):
            # #     sys.exit(1)