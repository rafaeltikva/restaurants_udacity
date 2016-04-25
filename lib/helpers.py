__author__ = 'rafaeltikva'
import re
import json

def is_api(url, api_format = 'qs_format'):
    if api_format == 'url_format':
        return True if re.match( r'/api((/(\w*)/?)*$)', url) else False

    return True if re.match( r'/api[/]?', url) else False

def get_api_match(url):
    return re.match( r'/api((/(\w*)/?)*$)', url)

def to_json(input):

    if type(input) == list:
        return json.dumps([obj.to_dict() for obj in input])
    else:
        return json.dumps(input)


def from_json(input):

    return json.loads(input)
