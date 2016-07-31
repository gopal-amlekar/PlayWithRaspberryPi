# This file just updates a channel in thingspeak.
# The channel key should be noted from thingspeak website

import requests

r = requests.post('https://api.thingspeak.com/update', {'api_key':'2YP3AFWJ90WSF4N8','field1':125})
print r

r = requests.post('https://api.thingspeak.com/apps/thingtweet/1/statuses/update',{'api_key':'20MPULCN4J2BN70B', 'status':'Tweet an example from thingspeak-pi'})
print r
