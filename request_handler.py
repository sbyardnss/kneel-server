"""main module"""
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from repository import all, retrieve, create, delete, update


class HandleRequests(BaseHTTPRequestHandler):
    """Controls the functionality of any GET, PUT, POST, DELETE requests to the server"""

    def do_GET(self):
        """Handles GET requests to the server """
        response = None
        (resource, id) = self.parse_url(self.path)
        if id is not None:
            response = retrieve(resource, id)
            if response is not None:
                self._set_headers(200)
            else:
                self._set_headers(404)
                response = "not found"
        else:
            if resource is not None:
                self._set_headers(200)
                response = all(resource)
            else:
                self._set_headers(404)
                response = {
                    "message": "table not found"
                }
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        """Handles POST requests to the server """

        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        # response = {"payload": post_body}
        post_body = json.loads(post_body)
        response = {}
        (resource, id) = self.parse_url(self.path)
        new_asset = None
        new_asset = create(resource, post_body)
        response = new_asset
        required_attr = retrieve(resource, 1).keys()
        if new_asset.keys() == required_attr:
            self._set_headers(201)
            response = new_asset
            print(response)
        else:
            self._set_headers(400)
            print(required_attr)
            response = f"not able. these attributes required {list(required_attr)}"
        # new_order = None
        # if resource == "orders":
        #     if "metalId" in post_body and "styleId" in post_body and "sizeId" in post_body:
        #         new_order = create_order(post_body)
        #         self._set_headers(201)
        #         response = new_order
        #     else:
        #         self._set_headers(400)
        #         response = {
        #             "message": f'{"metalId is required" if "metalId" not in post_body else ""} {"styleId is required" if "styleId" not in post_body else ""} {"sizeId is required" if "sizeId" not in post_body else ""}'
        #         }
        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self):
        """Handles PUT requests to the server """
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id) = self.parse_url(self.path)
        if resource == "orders":
            update_order(id, post_body)
            self.wfile.write("".encode())

    def do_DELETE(self):
        """function for handling delete request"""
        (resource, id) = self.parse_url(self.path)
        if resource == "orders":
            self._set_headers(405)
            # delete_order(id)
            response = {
                "message": "Cannot delete this order as it has already been fulfilled"
            }
            self.wfile.write(json.dumps(response).encode())

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the options headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def parse_url(self, path):
        """turns url for requested animal into tuple"""
        path_params = path.split("/")
        resource = path_params[1]
        id = None
        try:
            id = int(path_params[2])
        except IndexError:
            pass
        except ValueError:
            pass
        return (resource, id)

# point of this application.


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
