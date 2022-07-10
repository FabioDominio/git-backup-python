from .base_model import BaseModel
import requests
from requests.auth import HTTPBasicAuth
import json

class BitbucketModel(BaseModel):    
    BASE_URL = "https://api.bitbucket.org/2.0/"

    # Constructor
    def __init__(self):        
        pass
    
    def __init__(self, username=None, password=None, token=None):        
        self.headers = {"Accept": "application/json"}
        if token is None:
            self.auth = HTTPBasicAuth(username, password)
        else:
            self.headers['Authorization'] = 'Bearer ' + token
        super().__init__()
    
    def getNamespaces(self):        
        url = self.BASE_URL + 'workspaces'
        #use the 'auth' parameter to send requests with HTTP Basic Auth:
        res = requests.get(url, headers=self.headers, auth=self.auth)   
        data = res.json()  
        if  'next' in data:
            next_url = data['next']
        else:
            next_url = None        
        current_list = list(map(lambda x :
            {
             'id' : x['slug'],
             'name': x['slug'].strip()
            }, data["values"]))
        while (next_url!=None):
            res = requests.get(next_url, headers=self.headers, auth=self.auth)        
            data = res.json()  
            if  'next' in data:
                next_url = data['next']
            else:
                next_url = None 
            current_list += list(map(lambda x :
                {
                    'id' : x['id'],
                    'name': x['name'].strip(),                    
                    'url': x['http_url_to_repo']
                }, res.json()))
        return current_list
    
    def getNamespaceRepositories(self, id: str):
        url = self.BASE_URL + "repositories/" + id        
        #use the 'auth' parameter to send requests with HTTP Basic Auth:
        res = requests.get(url, headers=self.headers, auth=self.auth)  
        data = res.json()  
        if  'next' in data:
            next_url = data['next']
        else:
            next_url = None 
        current_list = list(map(lambda x :
            {
             'id' : x['slug'],
             'name': x['name'].strip(),             
             'url': x['links']['clone'][0]['href']
            }, data["values"]))
        while (next_url!=None):
            res = requests.get(next_url, headers=self.headers, auth=self.auth)        
            data = res.json()  
            if  'next' in data:
                next_url = data['next']
            else:
                next_url = None 
            current_list += list(map(lambda x :
            {
             'id' : x['slug'],
             'name': x['name'].strip(),             
             'url': x['links']['clone'][0]['href']
            }, data["values"]))
        return current_list

