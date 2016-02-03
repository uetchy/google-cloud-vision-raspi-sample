import argparse
import base64
import httplib2
import sys

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

API_DISCOVERY_FILE = 'vision_discovery_v1alpha1.json'


def main(photo_file):
    '''Run a label request on a single image'''

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
                        'maxResults': 5,
                    }]
                }]
            })
        response = service_request.execute()
        # print(response)
        labels = map(lambda x: x['description'], response[
                     'responses'][0]['labelAnnotations'])
        sys.stdout.write("There are " + ", ".join(labels))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'image_file', help='The image you\'d like to label.')
    args = parser.parse_args()
    main(args.image_file)
