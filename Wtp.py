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

class Wtp():
	
	def __init__(self, path_chat=None, i=False, path_import="data.json"):
		self.__dict__ = {"users":{},"_chat_info_":{"n_msg":0, "n_words":0, "n_charac":0, "n_by_time":{}}}
		self.u = 0
		if path_chat:
			self.__load_from_chat__(path_chat)
		elif i:
			self.import_data(path_import)

	def plot_msgs_by_users(self, _u_=None, hide=True):
		if _u_:
			_u_ = _u_ if _u_ <= self.u else self.u
		else:
			_u_ = self.u
		users_n_msg = sorted([(item[0], item[1]["n_msg"]) for item in self.__dict__['users'].items()],key=operator.itemgetter(1), reverse=True)
		self.graf_h(users_n_msg, _u_, "Mensagens enviadas por usuario", hide)

	def plot_words_by_users(self, _u_=None, hide=True):
		if _u_:
			_u_ = _u_ if _u_ <= self.u else self.u
		else:
			_u_ = self.u
		users_n_words = sorted([(item[0], item[1]["n_words"]) for item in self.__dict__['users'].items()],key=operator.itemgetter(1), reverse=True)
		self.graf_h(users_n_words, _u_, "Palavras enviadas por usuario", hide)
	
	def plot_charac_by_users(self, _u_=None, hide=True):
		if _u_:
			_u_ = _u_ if _u_ <= self.u else self.u
		else:
			_u_ = self.u
		users_n_charac = sorted([(item[0], item[1]["n_charac"]) for item in self.__dict__['users'].items()],key=operator.itemgetter(1), reverse=True)
		self.graf_h(users_n_charac, _u_, "Caracteres enviados por usuario", hide)
	
	def plot_chat_msgs_by_time(self):
		chat_n_by_time = sorted([(item[0], item[1]) for item in self.__dict__['_chat_info_']['n_by_time'].items()])
		self.graf_v(chat_n_by_time, len(chat_n_by_time), "Total de mensagens enviadas por hora")
	
	def export(self, name = "data.json"):
		with open('data.json', 'w') as fp:
			json.dump(self.__dict__, fp)
	
	def import_data(self, name = "data.json"):
		file = open(name)
		_str_ = file.read()
		data = json.loads(_str_)
		self.__dict__ = data
		self.u = len(self.__dict__['users'])
	
	def graf_v(self, l, n, t):
		x = np.arange(n)
		y = []
		label = []
		for i in range(0, n):
			label.append(l[i][0])
			y.append(l[i][1])
		fig, ax = plt.subplots()
		ax.set_title(t)
		ax.set_xlabel('Hora')
		plt.bar(x, y, color=(0, 0, 1))
		plt.xticks(x, label)
		plt.show()
	
	def graf_h(self, l, n, t, h):
		x = np.arange(n)
		y = []
		label = []
		for i in range(0, n):
			label.append(l[i][0] if not h else "u: "+str(i+1))
			y.append(l[i][1])
		fig, ax = plt.subplots()
		ax.set_title(t)
		ax.barh(x, y, color=(0, 0, 1))
		ax.set_yticks(x)
		ax.set_yticklabels(label)
		ax.invert_yaxis()
		ax.set_xlabel('# Mensagens')
		ax.annotate("# total de mensagens: %d\n# total de palavras: %d\n# total de caracteres: %d\n# participantes: %d"
					 %(self.__dict__["_chat_info_"]["n_msg"],self.__dict__["_chat_info_"]["n_words"],self.__dict__["_chat_info_"]["n_charac"], self.u),
					xy=(0, 0), xycoords='data',
					xytext=(y[-1]+(y[0]-y[-1])/2, n-1), textcoords='data'
					)
		plt.show()
	
	def __load_from_chat__(self, path):
		with open(path, encoding="utf8") as file:
			for line in file:
				match = re.search(r'(?P<day>\d{1,2}\/\d{1,2}\/\d{2})\,\s(?P<hour>\d{2}:\d{2})\s-\s+(?:(?P<full_name>(?P<f_name>[A-Z][\w+]*)(\s*[A-Z][\w+]*)*)|.*(?P<number>(\+\d{1,3})\s(\d{1,4}\s\d{1,5}(\s|-)\d{1,4})))(:|.:)\s(\<Media.omitted\>)*(?P<msg>.*)', line, re.UNICODE)
				if match:
					h, _ = match.group('hour').split(":")
					# Informacoes gerais do grupo/chat
					self.__dict__["_chat_info_"]["n_msg"]+=1
					self.__dict__["_chat_info_"]["n_words"]+=len(match.group('msg').split())
					self.__dict__["_chat_info_"]["n_charac"]+=len(match.group('msg'))
					if h not in self.__dict__['_chat_info_']['n_by_time']:
						self.__dict__['_chat_info_']["n_by_time"][h] = 1
					else:
						self.__dict__['_chat_info_']["n_by_time"][h] += 1
					
					# Informacoes de usuario
					id = match.group('full_name') if match.group('full_name') else (match.group('number').replace(" ", "")).replace("-", "")
					if id not in self.__dict__['users']:
						#self.__dict__['users'][id] = 1
						self.__dict__['users'][id] = {"n_msg": 1, "n_words": len(match.group('msg').split()), "n_charac": len(match.group('msg')),"n_by_time":{h:1}}
					else:
						#self.__dict__['users'][id] += 1
						self.__dict__['users'][id]["n_msg"] += 1
						self.__dict__['users'][id]["n_words"] += len(match.group('msg').split())
						self.__dict__['users'][id]["n_charac"] += len(match.group('msg'))
						if h not in self.__dict__['users'][id]['n_by_time']:
							self.__dict__['users'][id]["n_by_time"][h] = 1
						else:
							self.__dict__['users'][id]["n_by_time"][h] += 1
			
			self.u = len(self.__dict__['users'])

def str2bool(v):
	if v.lower() in ('no', 'false', 'f', 'n', '0'):
		return False
	else:
		return True
			
if __name__=="__main__":
	ap = argparse.ArgumentParser()
	ap.add_argument("-f", "--file", required = True, help = "Path to the file")
	ap.add_argument("-u", "--users", required = False, help = "# of users to show in graph", default=0)
	ap.add_argument("-r", "--hide", required = False, help = "Hide name/numer in graph. Default=True",type=str2bool, default=True)
	args = vars(ap.parse_args())
	u = int(args['users'])
	h = args['hide']
	wtp = Wtp(args['file'])
	wtp.plot_msgs_by_users(u, h)
