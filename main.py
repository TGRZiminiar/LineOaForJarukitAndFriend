# -*- coding: utf-8 -*-

from flask import Flask,request
import os
import json
import requests
from dotenv import load_dotenv

#------------ end import zone -----------
load_dotenv()
token = os.getenv('CHANNELACCESSTOKEN')

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

#------------insert new code below --------
@app.route('/webhook' , methods = ['POST']) 
# for checking that the request 
def webhook():
    req = request.json
    print(req)
    if len(req["events"]) == 0:
        return '',200

    # replyToken = req['events'][0]['replyToken']

    handleRequest(req)
    return "", 200
    
# handle text incoming text
# the req of the events can be array but now we handle only 1 message at a time
def handleRequest(req):
    reply_url = 'https://api.line.me/v2/bot/message/reply'
    Authorization = 'Bearer {}'.format(token)

    headers = {'Content-Type':'application/json; charset=UTF-8','Authorization':Authorization}
    
    # now handle only 1 message that is sending from a user for now
    response = handleEvents(req["events"][0])
    replyToken = req['events'][0]['replyToken']
    
    data = json.dumps(
        {
            "replyToken":replyToken,
            "messages":[
                {
                    "type":"text",
                    "text":response,
                }
            ]
        }
    )
    r = requests.post(reply_url, headers=headers, data=data)


def handleEvents(event):
    if event['message']['type'] == 'text':
        return handleMessage(event['message'])
    elif event['message']['type'] == 'image':
        return handleImage(event['message'])
    else:
        print(f"Unknown event type: {event['type']}")
        return "sorry unknown type format we still can't handle this type of message"


# handle input type message
# return out the string that we want to send the user 
# out of the function to send a message
def handleMessage(event):
    print(event)
    textFromUser = event['text']
    return "receiving this from handle message" + textFromUser


# handle input type image
# return out the string that we want to send the user 
# out of the function to send a message
def handleImage(event):
    
    # line doesn't allow to get the image data directly but need to call an api instead
    messageId = event["id"]
    getImageDataUrl = f"https://api-data.line.me/v2/bot/message/{messageId}/content"
    
    Authorization = 'Bearer {}'.format(token)

    headers = {'Content-Type':'application/json; charset=UTF-8','Authorization':Authorization}
    # Returns status code 200 and the content in binary
    response = requests.request("GET", getImageDataUrl, headers=headers)
    content_type = response.headers['Content-Type']

    if response.status_code == 200:
        image_data = response.content
        responseFromCarnet = recognize_file(messageId, image_data, content_type)
        if 'error' in responseFromCarnet:
            return "can't process your image cause of " + responseFromCarnet['error']
        
        car_info = responseFromCarnet["car"]

        return "what ever NUT what to send to user" + str(car_info)
    else:
        return "get the image error"


# version to use with a lineOa
# change at imageFile directly send the file_type to the files
def recognize_file(file_name, file_binary, file_type):
    url = "https://carnet.ai/recognize-file"
    headers = {
        "accept": "*/*",
        "accept-language": "en-US,en;q=0.9,th;q=0.8",
        "sec-ch-ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"macOS\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
        "Referer": "https://carnet.ai/",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }

    files = {
        "imageFile": (file_name, file_binary, file_type)
    }
    

    response = requests.post(url, headers=headers, files=files)
    return response.json()

#------------ end edit zone  --------
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=int(os.environ.get('PORT','5000')))