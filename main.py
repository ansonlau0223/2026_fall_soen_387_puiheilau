import json
from http.server import BaseHTTPRequestHandler, HTTPServer

events=[
    {"id": "ev_101", "title": "Jazz Ensemble: Fall Concert",
    "searsLeft": 42}, 
    {"id": "ev_102", "title": "Improv Night", 
    "seatsLeft": 0},
]

class Handler(BaseHTTPRequestHandler):

    def do_GET(self):

        #TODO 1
        if self.path =="/events":
            self.send(200, events)
        else:
            self.send(404, {"error": "not found"})

    def _send(self, status, body):
        payload = json.dumps(body).encode()

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()

        self.wfile.write(payload)

HTTPServer(("", 3000), Handler).serve_forever()