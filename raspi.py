#!/usr/bin/python3

import argparse
import base64
import httplib2
import sys
import time
import picamera

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

API_DISCOVERY_FILE = 'vision_discovery_v1alpha1.json'

def main():
  photo_file = 'target.jpg'
  with picamera.PiCamera() as camera:
    camera.resolution = (640, 480)
    camera.start_preview()
    time.sleep(2) # Adjust condition
    camera.capture(photo_file)
    camera.stop_preview()

  credentials = GoogleCredentials.get_application_default()
  with open(API_DISCOVERY_FILE, 'r') as f:
    doc = f.read()
  service = discovery.build_from_document(
    doc, credentials=credentials, http=httplib2.Http())

  with open(photo_file, 'rb') as image:
    image_content = base64.b64encode(image.read())
    service_request = service.images().annotate(
      body={
        'requests': [{
          'image': {
            'content': image_content
           },
          'features': [{
            'type': 'LABEL_DETECTION',
            'maxResults': 2,
           }]
         }]
      })
    response = service_request.execute()
    # print(response)
    labels = map(lambda x: x['description'], response['responses'][0]['labelAnnotations'])
    sys.stdout.write("There are " + ", ".join(labels))

if __name__ == '__main__':
  main()
