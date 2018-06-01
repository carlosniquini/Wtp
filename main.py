import argparse
import re
import operator
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np

_dict_ = {}
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required = True, help = "Path to the file")
ap.add_argument("-u", "--users", required = False, help = "# of users to show in graph")
args = vars(ap.parse_args())

total_msgs = 0
u = 0

def graf_v(l, n):
	x = np.arange(n)
	y = []
	label = []
	for i in range(0, n):
		label.append(l[i][0])
		y.append(l[i][1])
	fig, ax = plt.subplots()
	plt.bar(x, y)
	plt.xticks(x, label)
	plt.show()

def graf_h(l, n):
	x = np.arange(n)
	y = []
	label = []
	for i in range(0, n):
		label.append(l[i][0])
		y.append(l[i][1])
	fig, ax = plt.subplots()
	ax.barh(x, y)
	ax.set_yticks(x)
	ax.set_yticklabels(label)
	ax.invert_yaxis()
	ax.set_xlabel('# Mensagens')
	ax.annotate("# total de mensagens: %d\n# participantes: %d"%(total_msgs, len(_dict_)),
				xy=(0, 0), xycoords='data',
                xytext=(y[-1]+100, n-1), textcoords='data'
                )
	plt.show()
	
with open(args['file'], encoding="utf8") as file:
	for line in file:
		match = re.search(r'(?P<day>\d{1,2}\/\d{1,2}\/\d{2})\,\s(?P<hour>\d{2}:\d{2})\s-\s+(?:(?P<full_name>(?P<f_name>[A-Z][\w+]*)(\s*[A-Z][\w+]*)*)|.*(?P<number>(\+\d{1,3})\s(\d{1,4}\s\d{1,5}(\s|-)\d{1,4})))(:|.:)(?P<msg>.*)', line, re.UNICODE)
		if match:
			total_msgs+=1
			id = match.group('full_name') if match.group('full_name') else match.group('number')
			if id not in _dict_:
				_dict_[id] = 1
			else:
				_dict_[id] += 1
			
if args['users'] == None:
	u = len(_dict_)
else:
	u = int(args['users'])
			

sorted = sorted(_dict_.items(), key=operator.itemgetter(1), reverse=True)
graf_h(sorted, u)