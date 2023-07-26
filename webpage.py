from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

def read_file(filename):
    with open(filename, 'r') as file:
        return file.read()
    
html_form = read_file('template/index.html')
css_style = read_file('template/styles.css')
logged_page = read_file('template/selection.html')

class SimpleServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(html_form.encode())
        elif self.path.startswith('/submitted'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            parsed_params = parse_qs(urlparse(self.path).query)
            service_name = parsed_params.get('service_name', [''])[0]
            service_type = parsed_params.get('service_type', [''])[0]
            # self.wfile.write(f'Starting {service_type} service: {service_name}'.encode())
            self.wfile.write(logged_page.encode())
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode()
        parsed_params = parse_qs(post_data)
        service_name = parsed_params.get('service_name', [''])[0]
        service_type = parsed_params.get('service_type', [''])[0]

        # Perform any necessary processing with the form data here.
        # For now, we'll just redirect to the second page.
        if 'felipe' in service_name:
            self.send_response(303)  # 303 See Other (POST-REDIRECT-GET)
            self.send_header('Location', '/submitted?service_name={}&service_type={}'.format(service_name, service_type))
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b'404 Not Found')

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, SimpleServer)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()