import requests

server_url = 'http://127.0.0.1:5000/image'
response = requests.get(server_url, allow_redirects=True)
full_path = '/home/cmb22/Desktop/temp_test.jpg'
open(full_path, 'wb').write(response.content)