from twilio.twiml.messaging_response import MessagingResponse
from imgurpython import ImgurClient
from flask import Flask, request, jsonify, session, send_file
from werkzeug.utils import secure_filename
from datetime import date
import random
import configparser
import json
import os

from hack import app
import hack.db
from hack.db import db_session, init_db
from twilio.rest import Client

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
    fields = request.values['Body'].split(',')

    # if there is a message
    if len(fields) > 0:
        command = fields[0]

        if "meme" in request.values['Body'].lower():
            # do something with imgur
            req = request.values['Body'].replace("meme", "", 1)
            items = client.gallery_search(request.values['Body'], advanced=None, sort='time', window='all', page=0)
            print(len(items))
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
                            #to=request.values['From'],
                            to='+17033099847',
                            media_url=image_link
                    )
            #resp.message(items[0])
        elif command == 'gif':
            # do something with giphy
            print()



    print(request.values['Body'])

    # Add a message

    return str(resp)
