A small python library for [idealista.com API](https://www.idealista.com/labs/)
```python
import idealista_api as iapi

APYKEY = 'YOUR_API_KEY'
secret = 'YOUR_API_SECRET'

client = iapi.Client(APYKEY, secret)
data = {'center': '41.394554,2.175153',
        'distance': 10000,
        'operation': 'sale',
        'propertyType': 'homes',
        'locale': 'en'}
r = client._post('es', data)
r_dict = client._parse_post(r)
```
