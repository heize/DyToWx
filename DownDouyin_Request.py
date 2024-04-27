import requests
import configparser
import json

class DownDouyin_Request:
    RequestDomain = "https://www.yourdomainxxx.com/"

    def __init__(self):
        self.config = configparser.ConfigParser()

    def login(self, u:str, p:str) -> bool:
        d = {"u":u,"p":p}
        res = requests.post(f"{self.RequestDomain}/ssclient/login.ashx",data=d)
 
        if res.text == "a":
            return False
        
        self.token = res.text

        # config.read('config.ini')
        # database_host = config.get('Database', 'host')
        # database_port = config.getint('Database', 'port')

        self.config['Userinfo'] = {'token': res.text}
        with open('config.ini', "w") as config_file:
            self.config.write(config_file)
        return True

    def load_gh(self):
        d = {"t": self.token}
        res = requests.post(f"{self.RequestDomain}/ssclient/ghList.ashx",data=d)

        if res.text == "a" or res.text == "":
            self.ghlist = None
        else:
            self.ghlist = json.loads(res.text)
    
    def load_config(self) -> bool:
        self.config.read('config.ini')
        if self.config.has_option("Userinfo","token"):
            self.token = self.config.get('Userinfo', 'token')
            return True
        else:
            return False

    def ana_dy(self, sharetext):
        d = {"t": self.token,"c": sharetext}
        res = requests.post(f"{self.RequestDomain}/ssclient/AnaDy.ashx",data=d)

        if res.text == "a" or res.text == "":
            return None
        else:
            return json.loads(res.text)
        
    def record_upload(self, file, title):
        d = {"t": self.token,"ff": file, "tt":title}
        res = requests.post(f"{self.RequestDomain}/ssclient/UpVideo.ashx",data=d)
        if res.text == "a" or res.text == "":
            return "0"
        else:
            return res.text

