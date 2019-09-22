import requests

def accesError(Exception):
    Exception._init_(self)
    self.cause = cause

def accesoAPI(url):
    #con la url que le pasamos hace la llamada
    try:
        response= requests.get(url)    
    except requests.exceptions.ConnectionError as e:
        print('error en acceso API')
    except Exception as e:
        print (e)

    if response.status_code == 200:
        return(response.text)
    