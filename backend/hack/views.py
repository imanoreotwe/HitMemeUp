from twilio.twiml.messaging_response import MessagingResponse
from imgurpython import ImgurClient
from flask import Flask, request, jsonify, session, send_file
from werkzeug.utils import secure_filename
from datetime import date
import random
import configparser
import json
import os
import requests

from hack import app
from twilio.rest import Client
import urllib
from urllib import parse

#app = Flask(__name__)
#config = configparser.ConfigParser()
#config.read(os.path.join(os.getcwd(),'auth.ini'))

#client_id = config.get('credentials', 'client_id')
#client_secret = config.get('credentials', 'client_secret')

client_id = "741a70c559947a2"
client_secret = "c97cf173d6c7bfd71f7486cbd23d8f98a9e578b9"

client = ImgurClient(client_id, client_secret)

twi_account_sid = 'ACd5b96657935efd3a8d35495e2a9b1ea0'
twi_auth_token = '798eecacd63248f6e604a51a274fb916'
twi_client = Client(twi_account_sid, twi_auth_token)

@app.route("/sms", methods=['GET', 'POST'])
def sms_ahoy_reply():
    resp = MessagingResponse()
    fields = request.values['Body'].split(' ')

    # if there is a message
    if len(fields) > 0:
        if fields[0].lower() == 'meme':
            try:
                command = fields[0]

                # do something with imgur
                req = request.values['Body'].replace("meme", "", 1)
                items = client.gallery_search(request.values['Body'], advanced=None, sort='time', window='all', page=0)
                print(len(items))
                if len(items) > 0:
                    item_index = random.randint(0, len(items)-1)
                    image_link = items[item_index].link

                    album_id = items[item_index].link.split('/')[-1]
                    if '.' not in album_id:
                        album_items = client.get_album_images(album_id)
                        image_link = album_items[0].link
                    print(image_link)
                    message = twi_client.messages \
                            .create(
                                    from_='+17205130277',
                                    to=request.values['From'],
                                    media_url=image_link
                            )
            except:
                message = twi_client.messages.create(
                                    from_='+17205130277',
                                    to=request.values['From'],
                                    body='An unexpected error occured.'
                )
        elif fields[0] == 'gif':
            # return a gif related to the keyword
            req = request.values['Body'].replace("meme", "", 1)
            query = {'q': req, 'apikey': 'dc6zaTOxFJmzC'}
            headers = {'X-RapidAPI-Key': '0b7e7db0dfmshddfdc1e9523edf6p1c40d5jsn42179db7b62e'}
            r = requests.get('https://giphy.p.rapidapi.com/v1/gifs/search?' + urllib.parse.urlencode(query), headers=headers)
            print(type(r))
            print(r)
            print(type(r.text))
            items = r['data']
            item_index = random.randint(0, len(items)-1)
            message = twi_client.messages.create(
                                from_='+17205130277',
                                to=request.values['From'],
                                media_url=r.text['data'][item_index]['images']['original']['url']
            )

        elif fields[0] == 'insult':
            # return a random spotify song
            query = {'mode': 'random'}
            headers = {'X-RapidAPI-Key': '0b7e7db0dfmshddfdc1e9523edf6p1c40d5jsn42179db7b62e'}
            r = requests.get('https://lakerolmaker-insult-generator-v1.p.rapidapi.com/?' + urllib.parse.urlencode(query), headers=headers)
            message = twi_client.messages.create(
                                from_='+17205130277',
                                to=request.values['From'],
                                body=r.text
            )

    else:
        message = twi_client.messages.create(
                            from_='+17205130277',
                            to=request.values['From'],
                            body='No results found.'
                            )

    print(request.values['Body'])

    # Add a message

    return str(resp)
