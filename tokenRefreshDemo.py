import requests
import json
import time

## Enter your initial Access_Token that was generated using an Integration.
bearer = {"token": " "}

url_people = 'https://webexapis.com/v1/people/me'
url_refresh = 'https://webexapis.com/v1/access_token'


def sendSparkGET(url_people):
    response = requests.get(url_people,
                           headers={"Accept" : "application/json",
                                    "Content-Type":"application/json",
                                    "Authorization": "Bearer "+str(bearer['token'])})
    return response

def refreshToken(url_refresh):
    ## Enter your Client_Id, Client_Secret and Refresh_Token
    data = {
	"grant_type":"refresh_token",
	"client_id": " ",
	"client_secret": " ",
	"refresh_token": " "
    }

    headers = {"Accept" : "application/json","Content-Type":"application/json"}
    response = requests.post(url_refresh, json=data, headers=headers)
    return response

while True:
    result = sendSparkGET(url_people)
    resBody = result.json()
    resHeaders = result.headers.get("trackingid")
    ## A 401 response will indicate that the access_token is no longer valid so this will cause it to generate a new one and store it in the dict.
    if result.status_code == 401:
        print('-----------------------------------------------------------------')
        print('HTTP Response: ',result.status_code)
        print('TrackingId: ',resHeaders)
        print('Token expired, generating new token...')
        newTokenCreate = refreshToken(url_refresh)
        res = json.loads(newTokenCreate.text)
        print('New Token: ', res['access_token'])
        print('-----------------------------------------------------------------')
        bearer['token'] = res['access_token']
    else:
        print('HTTP Response',result.status_code)
        print('TrackingId: ',resHeaders)
        print('Token still valid.')
        print('User Details: \n'+json.dumps(resBody, indent=4))
        print('-----------------------------------------------------------------')
        time.sleep(5)
