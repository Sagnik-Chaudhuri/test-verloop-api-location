'''
API endpoint which returns latitude and logitude related to
geolocation
'''

import urllib.parse
from flask import Flask, request
import requests
from dicttoxml import dicttoxml
from helpers import secret

app = Flask(__name__)
app.secret_key = secret.SESSION_SECRET_KEY


@app.route('/getAddressDetails', methods=['POST'])
def getAddressDetails():
    ''' Returns Co-ordinates either in json or xml'''
    request_body = request.json
    req_add = request_body.get('address')
    req_format = request_body.get('output_format')
    if(not req_add or not (req_format == "xml" or req_format == "json")):
        return 'bad request!', 400

    url = "https://maps.googleapis.com/maps/api/geocode/json?address="+urllib.parse.quote(req_add)+"&key="+app.secret_key

    payload = {}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    response = response.json()
    if len(response.get("results")) <= 0:
        return 'bad request!', 400

    latt = response.get("results")[0].get("geometry").get("location").get("lat")
    longg = response.get("results")[0].get("geometry").get("location").get("lng")

    result = {
        "coordinates": {
            "lat": latt,
            "lng": longg
        },
        "address": req_add
    }
    if req_format == "xml":
        return dicttoxml(result, attr_type=False), {'Content-Type': 'application/xml'}
    return result


if __name__ == "__main__":
    app.run()
