import json
import urllib
# type = 'domain' # 'ip-address'
type = 'ip-address' # 'ip-address'
url = 'https://www.virustotal.com/vtapi/v2/'+ type +'/report'
apikey = '719fe935aacfd028abedbc0874a87a2f9c4b0186ef2d9ac98087bfa41c36ab8a'
# parameters = {'domain': 'bu.edu', 'apikey': apikey}
parameters = {'ip': '128.197.236.4', 'apikey': apikey }
response = urllib.urlopen('%s?%s' % (url, urllib.urlencode(parameters))).read()
print '%s?%s' % (url, urllib.urlencode(parameters))
response_dict = json.loads(response)
print response_dict
print response_dict["country"]
# print response_dict

with open('passiveDNS_Data.txt', 'w') as outfile:
  json.dump(response_dict, outfile,sort_keys=True, indent=4)