from http.server import BaseHTTPRequestHandler
import os
from io import BytesIO
import urllib


class MyHTTPRequestHandler(BaseHTTPRequestHandler):

    root = "htdocs"
    url = urllib.parse.ParseResult(0, 0, 0, 0, 0, 0)

    def _set_headers(self, mimetype=""):
        if mimetype == "":
            mimetype = "text/html"

        print(mimetype)
        self.send_response(200)
        self.send_header('Content-type', mimetype)
        self.end_headers()

    def _debug_self(self):
        parsed_path = self.url

        message = '\n'.join([
            'CLIENT VALUES:',
            'client_address=%s (%s)' % (self.client_address,
                                        self.address_string()),
            'command=%s' % self.command,
            'path=%s' % self.path,
            'real path=%s' % parsed_path.path,
            'query=%s' % parsed_path.query,
            'request_version=%s' % self.request_version,
            '',
            'SERVER VALUES:',
            'server_version=%s' % self.server_version,
            'sys_version=%s' % self.sys_version,
            'protocol_version=%s' % self.protocol_version,
            '',
        ])
        print(message)

    def do_HEAD(self):
        self._set_headers()

    def do_GET(self):
        self.url = urllib.parse.urlparse(self.path)

        self._debug_self()

        print(self.__handleURL())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)

        self._set_headers()

        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())


    # url = ParseResult(scheme='', netloc='', path='/', params='', query='index=2', fragment='')
    def __handleURL(self):

        url_ = self.url.path

        text = url_

        if url_ == '/api':
            text += self.__api_call()
        else:
            text += self.__standard_call()

        return text

    def __standard_call(self):
        text = 'standard call'
        text += self.url.path

        filename = self.url.path

        # work around for empty GET
        if filename == '/':
            filename = '/index.html'

        # build the fullname
        fullname = self.root + filename

        # try to load the file
        text += self.__load_file(fullname)

        return text


    def __api_call(self):

        text = 'api call'

        text += self.url.path
        byte_str = text.encode('utf-8')

        self._set_headers()
        self.wfile.write(byte_str)

        return text

    def __load_file(self, fullname):
        text = ""
        if os.path.exists(fullname):
            f = open(fullname, mode="rb")

            mimetype = self.__get_mimetype(fullname)
            self._set_headers(mimetype)
            self.wfile.write(f.read())
            text += "file loaded " + fullname
        else:
            self._set_headers()
            data = self.__magic404()
            self.wfile.write(data.encode('utf-8'))
            text += 'file not found ' + fullname

        return text

    def __get_mimetype(self, fullname):

        ext = os.path.splitext(fullname)[1]
        ext = ext.upper()

        types = {
            '.PNG': 'image/png'
        }

        mimetype = types.get(ext, 'text/html')

        return mimetype


    def __magic404(self):

        data = ""
        data += "<h1>ooops 404</h1>"

        return data


