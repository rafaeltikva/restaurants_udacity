__author__ = 'rafaeltikva'

from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
from urlparse import urlparse, parse_qs
from lib.helpers import is_api, get_api_match, to_json, from_json
import api_db_mapping
import database
import os
import codecs

restaurant_cfg = {
    'WEB_ROOT': './webapp'
}

mime_types = {'html': 'text/html', 'css': 'text/css', 'js': 'application/js', '': 'application/js',
              'json': 'application/json', 'jpg': 'image/jpg'}


class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):

        try:
            parsed_url = urlparse(self.path)

            self.path = parsed_url.path

            # initialize mime type to be text/html
            mime_type = mime_types.get('html')

            # initialize response to client
            response = ''

            # api request
            if is_api(self.path):
                api_regex_match = get_api_match(self.path)
                # extract api call from request
                api_call = api_regex_match.group(3)
                api_params = parse_qs(parsed_url.query)
                response = to_json(database.query(api_db_mapping.mapping[api_call]['object_type']))
                mime_type = mime_types.get('json')

            # file request/normal request
            else:
                self.path = restaurant_cfg['WEB_ROOT'] + self.path if self.path != '/' else restaurant_cfg['WEB_ROOT'] + '/html/restaurants.html'
                # check the file extension and set the correct mime type
                # filename = os.path.splitext(self.path)[0]
                file_extension = os.path.splitext(self.path)[1][1:]
                mime_type = mime_types.get(file_extension)

                with codecs.open(self.path, 'r', encoding='utf-8') as fp:
                    response = fp.read()
                    # print response

            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.end_headers()

            self.wfile.write(response)

            return

        except IOError:
            self.send_error(404, 'File not found: %s' % self.path)

    def do_POST(self):
        try:
            parsed_url = urlparse(self.path)

            self.path = parsed_url.path

            # initialize mime type to be application/json
            mime_type = mime_types.get('json')

            # initialize response to client
            response = ''

            # api request
            if is_api(self.path):

                api_regex_match = get_api_match(self.path)
                # extract api call from request
                api_call = api_regex_match.group(3)
                api_params = parse_qs(parsed_url.query)
                # load post data and convert to dict
                post_data = from_json(self.rfile.read(int(self.headers.getheader('Content-Length'))))

                if post_data['action'] == 'update':
                    response = to_json(database.update(api_db_mapping.mapping[api_call]['object_type'], from_json(post_data['store'])))
                elif post_data['action'] == 'delete':
                    response = to_json(database.delete(api_db_mapping.mapping[api_call]['object_type'], from_json(post_data['store'])))

            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.end_headers()

            self.wfile.write(response)

            print response

            return

        except IOError:
            self.send_error(404, 'File not found: %s' % self.path)

    def do_PUT(self):
        try:

            parsed_url = urlparse(self.path)

            self.path = parsed_url.path

            # initialize mime type to be application/json
            mime_type = mime_types.get('json')

            # initialize response to client
            response = ''

            # api request
            if is_api(self.path):

                api_regex_match = get_api_match(self.path)
                # extract api call from request
                api_call = api_regex_match.group(3)
                api_params = parse_qs(parsed_url.query)
                # load post data and convert to dict
                put_data = from_json(self.rfile.read(int(self.headers.getheader('Content-Length'))))

                if put_data['action'] == 'create':
                    response = to_json(database.create(api_db_mapping.mapping[api_call]['object_type'], from_json(put_data['store'])))

            self.send_response(200)
            self.send_header('Content-type', mime_type)
            self.end_headers()

            self.wfile.write(response)

            print response

            return

        except IOError:
            self.send_error(404, 'File not found: %s' % self.path)



def main(url='', port=8000):
    try:
        server_address = (url, port)
        httpd = HTTPServer(server_address, WebServerHandler)
        print ('Starting server, use <Ctrl-C> to stop')
        httpd.serve_forever()


    except KeyboardInterrupt:
        print ('Web server was stopped')


if __name__ == '__main__':
    main()
