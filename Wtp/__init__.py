import argparse
import re
import operator
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.ticker import FuncFormatter
import numpy as np
import json
import datetime
import pprint
import statistics

"""
_dict_=	{'users':{'name|number':{'n_msg':0, 'n_words':0, 'n_charac':0, 'n_by_time': { '00':0, '01':0, ...,'23':0}}}
		'_chat_info_':{"n_msg":0, "n_words":0, "n_charac":0,"n_by_time":{'00':0, '01':0, ...,'23':0}}}
"""

class Wtp():

	__id_to_weekday__ = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
	
	def __init__(self, path_chat=None, i=False, path_import="data.json"):
		self.__dict__ = {"users":{},"_chat_info_":{"n_msg":0, "n_words":0, "n_charac":0, "n_by_time":self.__init_dict_by_hour__(), "n_by_day":self.__init_dict_by_weekday__()}}
		self.u = 0
		
		if path_chat:
			self.__load_from_chat__(path_chat)
		elif i:
			self.import_data(path_import)
		
		self.users_n_msg = sorted([(item[0], item[1]["n_msg"]) for item in self.__dict__['users'].items()],key=operator.itemgetter(1), reverse=True)
		self.users_n_words = sorted([(item[0], item[1]["n_words"]) for item in self.__dict__['users'].items()],key=operator.itemgetter(1), reverse=True)
		self.users_n_charac = sorted([(item[0], item[1]["n_charac"]) for item in self.__dict__['users'].items()],key=operator.itemgetter(1), reverse=True)
		self.chat_n_by_time = sorted([(item[0], item[1]) for item in self.__dict__['_chat_info_']['n_by_time'].items()])

	def __init_dict_by_weekday__(self):
		return {i:self.__init_dict_by_hour__() for i in range(7)} 
	
	def __init_dict_by_hour__(self):
		return {format(i,'02d'):0 for i in range(24)}

	def __validate_u__(self, _u_):
		if _u_:
			_u_ = _u_ if _u_ <= self.u else self.u
		else:
			_u_ = self.u
		return _u_

	def plot_msgs_by_users(self, _u_=None, hide=True):
		_u_ = self.__validate_u__(_u_)
		self.__graf_h__(self.users_n_msg, _u_, "Total messages sent per user", hide)

	def plot_words_by_users(self, _u_=None, hide=True):
		_u_ = self.__validate_u__(_u_)
		self.__graf_h__(self.users_n_words, _u_, "Total words sent per user", hide)
	
	def plot_charac_by_users(self, _u_=None, hide=True):
		_u_ = self.__validate_u__(_u_)
		self.__graf_h__(self.users_n_charac, _u_, "Total characters sent per user", hide)
	
	def plot_user_msgs_by_weekday(self, id, hide=True, t="u: 1"):
		l = [sorted([(item[0], item[1]) for item in self.__dict__['users'][id]["n_by_day"][i].items()]) for i in range(0, 7)]
		self.__subplots_graf_v__(l, t if hide else id)

	def plot_users_msgs_by_weekday(self, _u_=None, hide=True):
		_u_ = self.__validate_u__(_u_)
		for i in range(0, _u_):
			self.plot_user_msgs_by_weekday(self.users_n_msg[i][0], hide=hide, t="u: "+str(i+1) if hide else None)

	def plot_chat_msgs_by_weekday(self):
		l = [sorted([(item[0], item[1]) for item in self.__dict__['_chat_info_']["n_by_day"][i].items()]) for i in range(0, 7)]
		self.__subplots_graf_v__(l, "Chat")

	def plot_chat_msgs_by_hour(self):
		self.__graf_v__(self.chat_n_by_time, len(self.chat_n_by_time), "Messages sent per hour")
	
	def export(self, name = "data.json", use_pprint = False):
		with open('data.json', 'w') as fp:
			if(use_pprint):
				pprint.pprint(self.__dict__, fp)
			else:
				json.dump(self.__dict__, fp)
	
	def import_data(self, name = "data.json"):
		file = open(name)
		_str_ = file.read()
		data = json.loads(_str_)
		self.__dict__ = data
		self.u = len(self.__dict__['users'])
	
	def __subplots_graf_v__(self, l, t, save=False):
		x = np.arange(24)
		plt.figure(1)
		for i in range(1, 8):
			ax = plt.subplot(330+i)
			y = []
			label = []
			for j in range(0, 24):
				label.append(l[i-1][j][0])
				y.append(l[i-1][j][1])
			plt.title(self.__id_to_weekday__[i-1])
			plt.plot(x, y, color=(0, 0, 1))
			plt.axhline(statistics.mean(y),color=(0,1,0,0.5), linewidth=1, label="Mean")
			plt.axhline(statistics.stdev(y),color=(1,0,0,0.5), linewidth=1, label="Standard deviation")
			ax.set_ylim(-0.5, max(y)+1)
			ax.set_xlim(0,23)
		plt.subplots_adjust(top=0.87, bottom=0.08, left=0.10, right=0.95, hspace=0.42,wspace=0.35)
		plt.suptitle(t + "\n(hour X # of msgs)")
		plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)		
		if save:
			plt.savefig(t+".png", bbox_inches='tight')
		plt.show()
		plt.close()

	def __graf_v__(self, l, n, t):
		x = np.arange(n)
		y = []
		label = []
		for i in range(0, n):
			label.append(l[i][0])
			y.append(l[i][1])
		_, ax = plt.subplots()
		ax.set_xlabel('Hour')
		#plt.bar(x, y, color=(0, 0, 1))
		plt.plot(x, y, color=(0, 0, 1))
		plt.axhline(statistics.mean(y),color=(0,1,0,0.5), linewidth=1, label="Mean")
		plt.axhline(statistics.stdev(y),color=(1,0,0,0.5), linewidth=1, label="Standard deviation")
		plt.legend()
		ax.set_title(t)
		ax.set_xlim(0,23)
		plt.xticks(x, label)
		plt.show()
	
	def __graf_h__(self, l, n, t, h):
		x = np.arange(n)
		y = []
		label = []
		for i in range(0, n):
			label.append(l[i][0] if not h else "u: "+str(i+1))
			y.append(l[i][1])
		_, ax = plt.subplots()
		ax.set_title(t)
		ax.barh(x, y, color=(0, 0, 1))
		ax.set_yticks(x)
		ax.set_yticklabels(label)
		ax.invert_yaxis()
		ax.set_xlabel('# Messages')
		ax.annotate("# messages: %d\n# words: %d\n# characters: %d\n# members: %d"
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
					mm, dd, yy = match.group('day').split("/")
					weekday = datetime.datetime(int(yy), int(mm), int(dd)).weekday()
					
					# Informacoes gerais do grupo/chat
					self.__dict__["_chat_info_"]["n_msg"]+=1
					self.__dict__["_chat_info_"]["n_words"]+=len(match.group('msg').split())
					self.__dict__["_chat_info_"]["n_charac"]+=len(match.group('msg'))
					self.__dict__['_chat_info_']["n_by_time"][h] += 1
					self.__dict__['_chat_info_']["n_by_day"][weekday][h] += 1
					
					# Informacoes de usuario
					id = match.group('full_name') if match.group('full_name') else (match.group('number').replace(" ", "")).replace("-", "")
					self.__dict__['users'].setdefault(id, {"n_msg": 0, "n_words": 0, "n_charac": 0,"n_by_time":self.__init_dict_by_hour__(), "n_by_day":self.__init_dict_by_weekday__()})
					self.__dict__['users'][id]["n_msg"] += 1
					self.__dict__['users'][id]["n_words"] += len(match.group('msg').split())
					self.__dict__['users'][id]["n_charac"] += len(match.group('msg'))
					self.__dict__['users'][id]['n_by_day'][weekday][h] += 1
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
	ap.add_argument("-i", "--import", required = False, help = "Import data from JSON file.", action='store_true')
	ap.add_argument("-e", "--export", required = False, help = "Export into a JSON file.", action='store_true')
	ap.add_argument("-u", "--users", required = False, help = "# of users to show in graph", default=0)
	ap.add_argument("-r", "--hide", required = False, help = "Hide name/numer in graph. Default=True",type=str2bool, default=True)
	ap.add_argument("-m_users", "--msgs_users", required = False, help = "Plot # of msgs by each user.", action='store_true')
	ap.add_argument("-w_users", "--words_users", required = False, help = "Plot # of words by each user.", action='store_true')
	ap.add_argument("-c_users", "--charac_users", required = False, help = "Plot # of characters by each user.", action='store_true')
	ap.add_argument("-m_user_w", "--msgs_user_w", required = False, help = "Plot # of msgs by name/number by weekday.")
	ap.add_argument("-m_users_w", "--msgs_users_w", required = False, help = "Plot # of msgs by each user by weekday.", action='store_true')
	ap.add_argument("-m_chat", "--msgs_chat", required = False, help = "Plot # of msgs by time.", action='store_true')
	ap.add_argument("-m_chat_w", "--msgs_chat_w", required = False, help = "Plot # of msgs by weekday.", action='store_true')
	args = vars(ap.parse_args())
	
	# Functions params
	f = args['file']
	i = args['import']
	e = args['export']
	u = int(args['users'])
	h = args['hide']
	
	# Functions
	m_users = args['msgs_users']
	w_users = args['words_users']
	c_users = args['charac_users']
	m_user_w = args['msgs_user_w']
	m_users_w = args['msgs_users_w']
	m_chat = args['msgs_chat']
	m_chat_w = args['msgs_chat_w']

	wtp = Wtp()
	if(i):
		wtp = Wtp(i=i, path_import=f)
	else:
		wtp = Wtp(f)
	
	if(m_users):
		wtp.plot_msgs_by_users(u, h)
	if(w_users):
		wtp.plot_words_by_users(u, h)
	if(c_users):
		wtp.plot_charac_by_users(u, h)
	if(m_user_w):
		wtp.plot_user_msgs_by_weekday(m_user_w, h)
	if(m_users_w):
		wtp.plot_users_msgs_by_weekday(u, h)
	if(m_chat):
		wtp.plot_chat_msgs_by_hour()
	if(m_chat_w):
		wtp.plot_chat_msgs_by_weekday()
	if(not i and e):
		wtp.export()
