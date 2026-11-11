import requests
import dotenv
import os
import json
from pprint import pprint
dotenv.load_dotenv()
client_secret = os.getenv('CLIENTSECRET')
client_id = os.getenv('CLIENTID')


auth_url="https://tdx.transportdata.tw/auth/realms/TDXConnect/protocol/openid-connect/token"
base_url='https://tdx.transportdata.tw/api/basic/'
iata='RMQ'
endpoints = {
    'airport': 'v2/Air/Airport/'+iata,
    'fids_depart': '/v2/Air/FIDS/Airport/Departure/'+iata,
    'fids_arrival': '/v2/Air/FIDS/Airport/Arrival/'+iata,
    'airline':'/v2/Air/Airline',
    'general_schedule': '/v2/Air/GeneralSchedule/Domestic'
}
params={
    'format':'JSON',
    'top':1,
}
class Auth():

    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret

    def get_auth_header(self):
        content_type = 'application/x-www-form-urlencoded'
        grant_type = 'client_credentials'

        return{
            'content-type' : content_type,
            'grant_type' : grant_type,
            'client_id' : self.client_id,
            'client_secret' : self.client_secret
        }

class data():

    def __init__(self, client_id, client_secret, auth_response):
        self.client_id = client_id
        self.client_secret = client_secret
        self.auth_response = auth_response

    def get_data_header(self):
        auth_JSON = json.loads(self.auth_response.text)
        access_token = auth_JSON.get('access_token')

        return{
            'authorization': 'Bearer ' + access_token,
            'Accept-Encoding': 'gzip'
        }

if __name__ == '__main__':
    try:
        for name in endpoints:
            if name=='general_schedule':
                params['$filter']="DepartureAirportID eq 'RMQ' or ArrivalAirportID eq 'RMQ'"
            d = data(client_id, client_secret, auth_response)
            data_response = requests.get(base_url+endpoints[name], headers=d.get_data_header(),params=params)
            print(f'================{name}===================')
            print(data_response)
            pprint(data_response.text)
    except:
        a = Auth(client_id, client_secret)
        auth_response = requests.post(auth_url, a.get_auth_header())
        for name in endpoints:
            if name=='general_schedule':
                params['$filter']="DepartureAirportID eq 'RMQ' or ArrivalAirportID eq 'RMQ'"
            d = data(client_id, client_secret, auth_response)
            data_response = requests.get(base_url+endpoints[name], headers=d.get_data_header(),params=params)
            print(f'================{name}===================')
            print(data_response)
            pprint(data_response.text)
    

