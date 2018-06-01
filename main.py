import argparse
import re
import operator
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter
import numpy as np
import json

"""
_dict_=	{'users':{'name|number':{'n_msg':0, 'n_words':0, 'n_charac':0, 'n_by_time': { '00':0, '01':0, ...,'23':0}}}
		'_chat_info_':{"n_msg":0, "n_words":0, "n_charac":0,"n_by_time":{'00':0, '01':0, ...,'23':0}}}
"""
_dict_ = {"users":{},"_chat_info_":{"n_msg":0, "n_words":0, "n_charac":0, "n_by_time":{}}}
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--file", required = True, help = "Path to the file")
ap.add_argument("-u", "--users", required = False, help = "# of users to show in graph")
args = vars(ap.parse_args())

u = 0

def plot_msgs_by_users(_d_, _u_):
	users_n_msg = sorted([(item[0], item[1]["n_msg"]) for item in _dict_['users'].items()],key=operator.itemgetter(1), reverse=True)
	graf_h(users_n_msg, _u_, "Mensagens enviadas por usuario")

def plot_words_by_users(_d_, _u_):
	users_n_words = sorted([(item[0], item[1]["n_words"]) for item in _dict_['users'].items()],key=operator.itemgetter(1), reverse=True)
	graf_h(users_n_words, _u_, "Palavras enviadas por usuario")

def plot_charac_by_users(_d_, _u_):
	users_n_charac = sorted([(item[0], item[1]["n_charac"]) for item in _dict_['users'].items()],key=operator.itemgetter(1), reverse=True)
	graf_h(users_n_charac, _u_, "Caracteres enviados por usuario")
	
def plot_chat_msgs_by_time(_d_):
	chat_n_by_time = sorted([(item[0], item[1]) for item in _dict_['_chat_info_']['n_by_time'].items()])
	graf_v(chat_n_by_time, len(chat_n_by_time), "Total de mensagens enviadas por hora")

def export(_d_):
	with open('data.json', 'w') as fp:
		json.dump(_d_, fp)

def import_data():
	file = open('data.json')
	_str_ = file.read()
	data = json.loads(_str_)
	return data

def graf_v(l, n, t):
	x = np.arange(n)
	y = []
	label = []
	for i in range(0, n):
		label.append(l[i][0])
		y.append(l[i][1])
	fig, ax = plt.subplots()
	ax.set_title(t)
	ax.set_xlabel('Hora')
	#plt.bar(x, y, color=(0, 0, 1))
	plt.bar(x, y, color=(0, 0, 1))
	plt.xticks(x, label)
	plt.show()

def graf_h(l, n, t):
	x = np.arange(n)
	y = []
	label = []
	for i in range(0, n):
		label.append(l[i][0])
		y.append(l[i][1])
	fig, ax = plt.subplots()
	ax.set_title(t)
	ax.barh(x, y)
	ax.set_yticks(x)
	ax.set_yticklabels(label)
	ax.invert_yaxis()
	ax.set_xlabel('# Mensagens')
	ax.annotate("# total de mensagens: %d\n# total de palavras: %d\n# total de caracteres: %d\n# participantes: %d"
				 %(_dict_["_chat_info_"]["n_msg"],_dict_["_chat_info_"]["n_words"],_dict_["_chat_info_"]["n_charac"], len(_dict_['users'])),
				xy=(0, 0), xycoords='data',
                xytext=(y[-1]+(y[0]-y[-1])/2, n-1), textcoords='data'
                )
	plt.show()
	
with open(args['file'], encoding="utf8") as file:
	for line in file:
		match = re.search(r'(?P<day>\d{1,2}\/\d{1,2}\/\d{2})\,\s(?P<hour>\d{2}:\d{2})\s-\s+(?:(?P<full_name>(?P<f_name>[A-Z][\w+]*)(\s*[A-Z][\w+]*)*)|.*(?P<number>(\+\d{1,3})\s(\d{1,4}\s\d{1,5}(\s|-)\d{1,4})))(:|.:)\s(\<Media.omitted\>)*(?P<msg>.*)', line, re.UNICODE)
		if match:
			h, _ = match.group('hour').split(":")
			# Informacoes gerais do grupo/chat
			_dict_["_chat_info_"]["n_msg"]+=1
			_dict_["_chat_info_"]["n_words"]+=len(match.group('msg').split())
			_dict_["_chat_info_"]["n_charac"]+=len(match.group('msg'))
			if h not in _dict_['_chat_info_']['n_by_time']:
				_dict_['_chat_info_']["n_by_time"][h] = 1
			else:
				_dict_['_chat_info_']["n_by_time"][h] += 1
			
			# Informacoes de usuario
			id = match.group('full_name') if match.group('full_name') else (match.group('number').replace(" ", "")).replace("-", "")
			if id not in _dict_['users']:
				#_dict_['users'][id] = 1
				_dict_['users'][id] = {"n_msg": 1, "n_words": len(match.group('msg').split()), "n_charac": len(match.group('msg')),"n_by_time":{h:1}}
			else:
				#_dict_['users'][id] += 1
				_dict_['users'][id]["n_msg"] += 1
				_dict_['users'][id]["n_words"] += len(match.group('msg').split())
				_dict_['users'][id]["n_charac"] += len(match.group('msg'))
				if h not in _dict_['users'][id]['n_by_time']:
					_dict_['users'][id]["n_by_time"][h] = 1
				else:
					_dict_['users'][id]["n_by_time"][h] += 1

if args['users'] == None:
	u = len(_dict_['users'])
else:
	u = int(args['users']) if int(args['users'])<=len(_dict_['users']) else len(_dict_['users'])

#import_data()
#export(_dict_)	
plot_msgs_by_users(_dict_, u)
plot_words_by_users(_dict_, u)
plot_charac_by_users(_dict_, u)
plot_chat_msgs_by_time(_dict_)
#sorted = sorted(_dict_['users'].items(), key=operator.itemgetter(1), reverse=True)