import sys # stdin
import re # regexp
import os
import json

qsize = 20;
chat_file = "chat.json"
users_file = "users.json"
DEBUG = False

server_msg = re.compile(r"\[(\d{2}:\d{2}:\d{2})\] \[Server thread/INFO\]: (.*)")
chat_message = re.compile(r"<([^ ]*)> (.*)")
achievement_message = re.compile(r"([^ ]*) has just earned the achievement_messageevement \[(.*)\]")
death_message = re.compile(r"([^ ]*) ((blew|burned|death_message|drowned|fell|got|hit|tried|starved|suffocated|walked|was|went|withered).*)")
join_message = re.compile(r"([^ ]*) joined the game")
leave_message = re.compile(r"([^ ]*) left the game");
online_message = re.compile(r"There are \d+/\d+ players online:");

storage = list()
users = set()

def put(action,timestamp,nick,message):
	if(len(storage) > qsize):
		storage.pop(0)
	storage.append({'action':action,'timestamp':timestamp,'nick':nick,'message':message})

def writeJSON():
	f = open(chat_file+".new", 'w+')
	js = json.dumps(storage)
	f.write(js)
	f.flush()
	f.close()
	# This way the webserver will always
	# serve "complete" json
	os.rename(chat_file+".new", chat_file)

writeJSON()

def writeUserJSON():
	f2 = open(users_file+".new", 'w+')
	js = json.dumps(list(users))
	print(js)
	f2.write(js)
	f2.flush()
	f2.close()
	# This way the webserver will always
	# serve "complete" json
	os.rename(users_file+".new", users_file)

writeUserJSON()

def dput(action, time, match):
	put(action, time, match.group(1), match.group(2))
	writeJSON()	

def D(msg):
	if(DEBUG):
		print(msg);

def DTM(msg, time, match):
	D(msg)

while True:
	line = sys.stdin.readline()
	line=line.strip()
	match = re.match(server_msg, line)
	if (match):
		time = match.group(1)
		data = match.group(2)
		match = re.match(chat_message, data);
		if(match):
			DTM("said ", time, match);
			dput("said", time, match)
			continue;
		match = re.match(achievement_message, data);
		if(match):
			DTM("gained", time, match)
			dput("gained", time, match)
			continue;
		match = re.match(death_message, data)
		if(match):
			DTM("died ", time, match)
			dput("died", time, match);
			writeJSON()
			continue;
		match = re.match(join_message, data)
		if(match):
			D("join " + match.group(1))
			users.add(match.group(1))
			writeUserJSON()
			continue
		match = re.match(leave_message, data)
		if(match):
			D("leave " + match.group(1))
			users.discard(match.group(1))
			writeUserJSON()
			continue
		match = re.match(online_message, data)
		if(match):
			data=sys.stdin.readline()
			data=data.strip()
			match = re.match(server_msg, data)
			if (match):
				li = match.group(2)
				users=set([x.strip() for x in li.split(',')])
				D("User_update " + str(users));
				writeUserJSON()
			continue
