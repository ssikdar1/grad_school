from xlrd import open_workbook
import re
import codecs
from urlparse import urlparse, parse_qs
outfile = codecs.open('output.csv', encoding='utf-8', mode='w+')
import math
wb = open_workbook('MALWARE_TRAFFIC_PATTERNS.xls')


def get_path_depth(path):
	""" Given a path calculate the the depth of the path
		input: '/bin/src/tmp/index.html'
		output: 3?
	"""
	try:
		parse = urlparse(path)
		tokens = parse.path.split('/')
		tokens.remove("")
		return len(tokens)-1
	except:
		print("ERROR IN PATH DEPTH")
		print path
		return 0
		
def get_path_entropy(path):
	""" Given a path calculate the the depth of the path
		input: '/bin/src/tmp/index.html'
		output: 3?
	"""
	try:
		e = entropy(path)
		return e
	except:
		print("ERROR IN PATH Entropy")
		print path
		return 0

def avg_entropy_of_param(path):
	try:
		parse = urlparse(path)
		if(len(parse.query) > 0):
			total = 0.0
			params = parse_qs(parse.query)
			if(len(params) > 0):
				# in this case
				#/ld/queenfun/vl /login.php?cd2hpdGU&uU11TVEV&s&pMTkyLjE2OC4wljYS&hi2wsdf35l
				#give it a zero
				for p in params:
					total += entropy(params[p][0])
				return total/len(params)
			else:
				return 0
		else:
			return 0
	except:
		print("ERROR IN param entropy")
		print path
		return 0
		
def get_resource_ext(path):
	pattern = '\.(.+)$'
	m = re.search(pattern, path)
	return m.group(1)

def contains_get_put(path):
	if(re.match('GET',path)):
		return 0
	elif(re.match('POST',path)):
		return 1
	else:
		return 2
		
def process_path(path):
	""" to process GET/POST paths 
		examples of paths I've been seeing:
		POST /new/gate.php HTTP/1.1
		GET /news.jpg HTTP/1.1
		"NICK USA|94576 USER vtptdwd 0 0 :USA|94576"
	"""
	depth = -1
	extension = ""
	
	# first remove the HTTP/1.1 or HTTP/1.0
	path = re.sub(r'HTTP\s*\/\d\.\d','',path)
	
	#Check to see if there is a GET or POST, for now throw an error if there isn't anything
	if(re.match('GET|POST',path)):
		path =  re.sub(r'GET|POST','',path)
		path =  path.lstrip()
		depth = get_path_depth(path)
		entrop = get_path_entropy(path)
		avg_param_entrop = avg_entropy_of_param(path)
		# extension = get_resource_ext(path)
		return avg_param_entrop
	else:
		print 'Path contains no GET OR POST ignoring for now'
		return 0

def run_data():
	for s in wb.sheets():
		if(s.name == 'Malware'):
			print 'Sheet:',s.name
			for row in range(s.nrows):
				for col in range(s.ncols):
					if(col == 3):
						#POST/GET Pattern
						data = s.cell(row,col).value
						data = data.replace('\n',' ')
						data = s.cell(row,col).value.encode('ascii', errors='backslashreplace')
						# val = contains_get_put(data)
						# outfile.write(str(val) + "\n")
						entrop = process_path(data)
						outfile.write(str(entrop) + "\n")
						
# http://stackoverflow.com/questions/2979174/how-do-i-compute-the-approximate-entropy-of-a-bit-string
def entropy(string):
        "Calculates the Shannon entropy of a string"

        # get probability of chars in string
        prob = [ float(string.count(c)) / len(string) for c in dict.fromkeys(list(string)) ]

        # calculate the entropy
        entropy = - sum([ p * math.log(p) / math.log(2.0) for p in prob ])

        return entropy


def entropy_ideal(length):
        "Calculates the ideal Shannon entropy of a string with given length"

        prob = 1.0 / length

        return -1.0 * length * prob * math.log(prob) / math.log(2.0)
						
						
def main():
	# p = 'POST /new/gate.php HTTP/1.1'
	# q = 'GET /news.jpg HTTP/1.1'
	# r = "NICK USA|94576 USER vtptdwd 0 0 :USA|94576"
	# process_path(p)
	# process_path(q)
	# t = "GET /1js/handle. php?addr=http%3A//thaingo.org/web/category/daylinews/enqnews/&ck =PHPSESSI D%3 Dn3fj1rfatdpgvpp7lucn0g44 c5%3B%20_utma%3D202272852. 2144388183.1340808890.1340808890.1340877171.2%3B%20_utmb%3D202272852. 2.10.1340877171%3B%20_utmc%3D202272852%3B%20_utmz%3D202272852.1340808890.1.1. utmcsr%3D%28direct%29%7Cutmccn%3D%28direct%29%7Cutmcmd%3D%28none%29&soft=Windows%20Explorer&browser=Mozilla/4. 0%20(compatible;%20MSIE%208. 0;%20windows%20NT%205.1;%20Trident/4.0;%20.NET%2OCLR%202.0.50727;%20.NET%2OCLR%203.0.04506.648;%20.NET%20CLR%203.5.21022;%20.NET%2OCLR%203.O.4506.2152;%20.NET%20CLR%203.5. 30729;%20. NET4. 0c;%20. NET4. 0E)&flashver=WIN%206%2c0%2c88%2c0 HTTP/1.1"
	# o = urlparse('/dns/dnslookup?la=en&host=picture.ucparlnet.com&type=A&submit=Resolve')
	
	run_data()
main()