import auth
import yaml
import requests
import dotenv
import os 
import pprint

dotenv.load_dotenv()
client_secret = os.getenv('CLIENTSECRET')
client_id = os.getenv('CLIENTID')


auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
base_url='https://tdx.transportdata.tw/api/basic/'


endpoint_list = ['airport', 'airline'
                 , 'fids_arrival', 'fids_depart'
                 , 'general_schedule']


with open('../config/endpoints.yml',mode='r', encoding="utf-8") as f:
    config=yaml.safe_load(f)
    

def call_API():
    a = auth.Auth(client_id, client_secret)
    auth_response = requests.post(auth_url, a.get_auth_header())

    endpoints=config['endpoints']
    for name in endpoint_list:
        e=endpoints[name]
        d = auth.data(client_id, client_secret, auth_response)
        data_response = requests.get(base_url+e['path'], headers=d.get_data_header(),params=e['params'])
