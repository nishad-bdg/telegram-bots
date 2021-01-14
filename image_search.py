import requests

headers = { 
  "apikey": "87cce380-5671-11eb-aa89-0d67d0cb24a0"}

params = (
   ("q","Pied Piper"),
   ("tbm","isch"),
);

response = requests.get('https://app.zenserp.com/api/v2/search', headers=headers, params=params);

data = response.json()

first_image = data['image_results'][0]['thumbnail']
print(first_image)