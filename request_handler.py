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
        (resource, id, query_params) = self.parse_url(self.path)
        if id is not None:
            response = retrieve(resource, id)
            if resource == "orders":
                if query_params[0] == 'metal':
                    print(query_params)
                    matching_metal = retrieve("metals", response["metalId"])
                    response["metal"] = matching_metal
                if response is not None:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
                    response = "not found"
            else:
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
        (resource, id, query_params) = self.parse_url(self.path)
        new_asset = None
        new_asset = create(resource, post_body)
        target_table = all(resource)
        length = len(target_table)
        last_index = length - 1
        required_attr = retrieve(resource, last_index).keys()
        if resource == "orders":
            if new_asset.keys() == required_attr:
                self._set_headers(201)
                response = new_asset
                print(response)
            else:
                self._set_headers(400)
                print(required_attr)
                response = f"not able. these attributes required {list(required_attr)}"
        else:
            self._set_headers(400)
            response = {
                "message": "customers cannot create these items"
            }
        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self):
        """Handles PUT requests to the server """
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)
        (resource, id, query_params) = self.parse_url(self.path)
        response = None
        target_table = all(resource)
        length = len(target_table)
        last_index = length - 1
        required_attr = retrieve(resource, last_index).keys()
        target_for_update = retrieve(resource, id)
        if post_body.keys() == required_attr:
            if resource == "metals" and target_for_update["metal"] == post_body["metal"]:
                self._set_headers(204)
                update(resource, id, post_body)
                self.wfile.write("".encode())
            else:
                self._set_headers(400)
                response = {
                    "message": "unable to update this item"
                }
                self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers(400)
            response = {
                "message": f"not a valid replacement object. must have {list(required_attr)}"
            }
            self.wfile.write(json.dumps(response).encode())

    def do_DELETE(self):
        """function for handling delete request"""
        (resource, id, query_params) = self.parse_url(self.path)
        if resource == "styles" or "sizes" or "orders" or "metals":
            self._set_headers(400)
            response = {
                "message": "customers cannot delete these items"
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self._set_headers(204)
            delete(resource, id)
            self.wfile.write("".encode())

    # def get_last_table_item(self, resource):
    #     """function for getting last item in table to match attributes"""
    #     target_table = all(resource)
    #     length = len(target_table)
    #     last_index = length - 1
    #     return retrieve(resource, last_index)

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

    # def parse_url(self, path):
    #     """turns url for requested animal into tuple"""
    #     path_params = path.split("/")
    #     resource = path_params[1]
    #     id = None
    #     try:
    #         id = int(path_params[2])
    #     except IndexError:
    #         pass
    #     except ValueError:
    #         pass
    #     return (resource, id)
    # Replace existing function with this

    def parse_url(self, path):
        """function for url parse with query params"""
        url_components = urlparse(path)
        path_params = url_components.path.strip("/").split("/")
        query_params = url_components.query.split("&")
        # query_params = url_components.query
        resource = path_params[0]
        id = None
        print(query_params)
        try:
            id = int(path_params[1])
        except IndexError:
            pass
        except ValueError:
            pass
        print(url_components)
        return (resource, id, query_params)

# point of this application.


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
