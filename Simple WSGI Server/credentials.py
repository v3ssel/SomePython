from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

species = {
           'Cyberman': 'John Lumic',
           'Dalek': 'Davros',
           'Judoon': 'Shadow Proclamation Convention 15 Enforcer',
           'Human': 'Leonardo da Vinci',
           'Ood': 'Klineman Halpen',
           'Silence': 'Tasha Lem',
           'Slitheen': 'Coca-Cola salesman',
           'Sontaran': 'General Staal',
           'Time Lord': 'Rassilon',
           'Weeping Angel': 'The Division Representative',
           'Zygon': 'Broton'
          }

def application(environ, start_response):
    d = parse_qs(environ['QUERY_STRING'])

    spec = species.get(d.get('species', [''])[0], 'Unknown')
    response_body = bytes(f'{{"credentials": "{spec}"}}\n', encoding='utf-8')

    status = '200 OK' if spec != 'Unknown' else '404 Not Found'
    response_headers = [
        ('Content-Type', 'application/json'),
        ('Content-Length', str(len(response_body)))
    ]

    start_response(status, response_headers)
    return [response_body]

httpd = make_server('localhost', 8888, application)
httpd.serve_forever()