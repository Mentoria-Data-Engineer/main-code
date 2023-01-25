# importar as bibliotecas
import requests
import json
import os

BEARER_TOKEN=os.environ.get("BEARER_TOKEN")

# autorizar a requisição
headers = {'Authorization': f"Bearer {BEARER_TOKEN}"}

# configurar uma url
query='' #required
tweet_fields='' #optional
user_fields='' 
start_time=''
end_time=''
url=f'''https://api.twitter.com/2/tweets/search/recent?
    query={query}&{tweet_fields}&{user_fields}&
    start_time={start_time}&end_time={end_time}'''

# fazer a requisição
r = requests.post(url, data=headers)
