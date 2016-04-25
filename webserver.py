from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi

class WebServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith('/hello'):
                self.send_response(200, 'Hello was successful')
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = '<html><body><h1>Hello there!</h1>'

                output += '<form method="POST" enctype="multipart/form-data" action="/hello">' \
                          '<h2>What would you like me to say?</h2>' \
                          '<input name="message" type="text" />' \
                          '<input type="submit" />' \
                          '</form>'
                output += '</body></html>'
                self.wfile.write(output)
                print output
                return
            elif self.path.endswith('/hola'):
                self.send_response(200)
                self.send_header('Content-Type', 'text/html')
                self.end_headers()

                output = '<html><body><h1>Hello there!</h1>'

                output += '<form method="POST" enctype="multipart/form-data" action="/hello">' \
                          '<h2>What would you like me to say?</h2>' \
                          '<input name="message" type="text" />' \
                          '<input type="submit" />' \
                          '</form>'
                output += '</body></html>'

                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File not found %s' % self.path)
    def do_POST(self):
        try:
            print 'self.rfile: \n'
            print self.rfile.__dict__
            self.send_response(301)
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')

                output = ''
                output += '<html><body>'
                output += '<h2>Ok, how about this: </h2>'
                output += '<h1> %s </h1>' % messagecontent[0]

                output += '<form method="POST" enctype="multipart/form-data" action="/hello">' \
                          '<h2>What would you like me to say?</h2>' \
                          '<input name="message" type="text" />' \
                          '<input type="submit" />' \
                          '</form>'
                output += '</body></html>'

                self.wfile.write(output)
                print output
                return


        except IOError:
            self.send_error(404, 'File not found %s' % self.path)

def main():
    try:
        port = 8000
        server_url = 'localhost'
        server_address = (server_url, port)
        httpd = HTTPServer(server_address, WebServerHandler)
        print ("Web server running on %s port %d" % server_address)
        httpd.serve_forever()

    except KeyboardInterrupt:
        print ("Web server was stopped")


if __name__ == '__main__':
    main()