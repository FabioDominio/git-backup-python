from .base_model import BaseModel
import requests
from requests.auth import HTTPBasicAuth
import json

class GitlabModel(BaseModel):

    BASE_URL = "https://gitlab.com/api/v4/"

    # Constructor
    def __init__(self):        
        pass
    
    def __init__(self, username=None, password=None, token=None):
        self.token = token
        self.headers = {"Accept": "application/json", "PRIVATE-TOKEN" : token}
        super().__init__()
    
    def getNamespaces(self):
        url = self.BASE_URL + 'groups?pagination=keyset&per_page=100&order_by=id&sort=asc'
        #use the 'auth' parameter to send requests with HTTP Basic Auth:
        res = requests.get(url, headers=self.headers)     
        if ( res.links.get('next')):
            next_url = res.links.get('next').get('url')
        else:
            next_url = None
        current_list = list(map(lambda x :
            {
             'id' : x['id'],
             'name': x['name'].strip(),
             'description': x['description'].strip()
            }, res.json()))
        while (next_url!=None):
            res = requests.get(next_url, headers=self.headers)        
            if ( res.links.get('next')):
                next_url = res.links.get('next').get('url')
            else:
                next_url = None
            current_list += list(map(lambda x :
                {
                    'id' : x['id'],
                    'name': x['name'].strip(),
                    'description': x['description'].strip(),
                    'url': x['http_url_to_repo']
                }, res.json()))
        return current_list
    
    def getNamespaceRepositories(self, id: str):
        url = self.BASE_URL + "groups/" + id + "/projects?simple=true&pagination=keyset&per_page=100&order_by=id&sort=asc"        
        #use the 'auth' parameter to send requests with HTTP Basic Auth:
        res = requests.get(url, headers=self.headers)     
        if ( res.links.get('next')):
            next_url = res.links.get('next').get('url')
        else:
            next_url = None
        current_list = list(map(lambda x :
            {
             'id' : x['id'],
             'name': x['name'].strip(),
             'description': x['description'].strip(),
             'url': x['http_url_to_repo']
            }, res.json()))
        while (next_url!=None):
            res = requests.get(next_url, headers=self.headers)        
            if ( res.links.get('next')):
                next_url = res.links.get('next').get('url')
            else:
                next_url = None
            current_list += list(map(lambda x :
                {
                    'id' : x['id'],
                    'name': x['name'].strip(),
                    'description': x['description'].strip(),
                    'url': x['http_url_to_repo']
                }, res.json()))
        return current_list

