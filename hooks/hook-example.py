#!/usr/bin/env python 
# Created by Camio.com - Copyright 2017
# License MIT

from __future__ import print_function
from bottle import route, run, request, response, default_app
import pymongo
import sys
import base64
import json
import os
import StringIO
import requests
import time
import logging
import traceback
try:
    from PIL import Image
except ImportError:
    import Image

API_KEY = '123456789'

connection = pymongo.MongoClient()
db = connection['mydb']
tasks = db['tasks']

# a basic URL route to test whether Bottle is responding properly
@route('/')
def index():
    return "it works!"

@route('/tasks/<secret>',method='POST')
def post_task(secret):
    body = request.body.read()    
    logging.info('payload size %s' % len(body))
    if secret != API_KEY:
        response.status = 400
        return "Invalid API Key"
    if body:
        payload = json.loads(body.decode('utf8'))
        tasks.insert({'request': payload, 'status':'pending'})
        logging.info('done')
        images = payload.get('images')
    return 'ok'

@route('/tasks/<secret>',method='GET')
def get_tasks(secret):
    if secret != API_KEY:
        response.status = 400
        return "Invalid API Key"
    all_tasks = tasks.find({'status':'pending'})
    return repr([task['request']['user_id']+'/'+task['request']['camera'] for task in all_tasks])

###########################################################################
# This is the function that you modify to perform your particular labeling.
# The payload images is a list 
# [
#   {
#      type: "image/jpeg",
#      size: [640, 480],
#      timestamp: "2017-05-05T01:31:13.738647",
#      image_b64: "... base 64 binary data ..."
#   },
#   ...
# ]
#
# The custom code in compute_labels should loop and label each one of them and 
# return a dictionary of the form
#  
# {
# "labels: {
#   "2017-01-01T12:00:00.000": {
#      "cat": {"probability: 0.93, "polygon": []},
#      "dog": {"probability: 0.88, "polygon": []},
#   }
#  }
# }
#
# i.e. a dictionary of labels for each image timestamp
# each label is a dictionary key associated to a 
# probability and an optional polygon (as list of x,y 
# coordinates expressed in % of the original image
# with (0,0) being the bottom-left corner and (1,1)
# the top-right corner,
#
###########################################################################
def compute_labels(images):
    labels = {}
    for image in images:
        image_type = image['type'] # example 'image/jpeg'
        image_size = image['size'] # (width, height)
        image_timestamp = image['timestamp'] # in iso format string
        image_bytes = base64.b64decode(image['image_b64']) # the bytes
        image = Image.open(StringIO.StringIO(image_bytes)) # a PIL image
        labels[image_timestamp] = {
            "cat":{"probability":0.93, "polygon":[]}, 
            "dog":{"probability":0.88, "polygon":[]},
            }
    return labels

def runtasks():
    t = 0
    while True:
        task = tasks.find_one({'status':'pending'})
        sys.stdout.flush()
        sys.stderr.flush()
        if task:
            t = 0
            print('processing task')
            request = task['request']
            try:
                images = request['images']
                callback_url = request['callback_url']
                labels = compute_labels(images)
                payload = {'status':'success', 'labels':labels}
                print('    posting payload')
                requests.post(callback_url, json=payload)
                print('    done!')
                task['status'] = 'completed'
            except:
                task['status'] = 'error'
                task['traceback'] = traceback.format_exc()
            tasks.update({'_id':task['_id']}, task)
        else:
            print('... %i ...' % t)
            t += 10
            time.sleep(10)

# these two lines are only used for python app.py
if __name__ == '__main__':
    runtasks()
    
# this is the hook for Gunicorn to run Bottle
app = default_app()
