A small python library for [idealista.com API](https://www.idealista.com/labs/)
```python
# import the module
import idealista_api as iapi

APYKEY = 'YOUR_API_KEY'
secret = 'YOUR_API_SECRET'

# client object to use the api
client = iapi.Client(APYKEY, secret)
# set up your data
data = {'center': '41.394554,2.175153',
        'distance': 10000,
        'operation': 'sale',
        'propertyType': 'homes',
        'locale': 'en',
        'maxItems': 50,
        'order': 'publicationDate',
        'numPage': 0} # change this number for each request

# request the data and parse the data as dictionary
r = client.api_search('es', data)
```
