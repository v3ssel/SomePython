import sys
import os
import filetype
import requests

if __name__ == '__main__':
    dst = os.path.join(os.path.dirname(__file__), 'app/audio/')
    if len(sys.argv) == 2 and sys.argv[1] == 'list':
        req = requests.get('http://localhost:8888/files_list')
        print(req.text)
    elif len(sys.argv) == 3 and sys.argv[1] == 'upload':
        if os.path.isfile(sys.argv[2]) and 'audio' in filetype.guess(sys.argv[2]).mime:
            req = requests.post('http://localhost:8888/', files={'file': open(sys.argv[2], 'rb')})
            print('Uploaded!')
