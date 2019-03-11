#!/usr/bin/python
from socket import *
import sys
import json

sSock = socket(AF_INET, SOCK_STREAM)
serverHost=sys.argv[1]
serverPort=int(sys.argv[2])
sSock.connect((serverHost, serverPort))
letters = sSock.recv(1024)

dt = {'S': 20,'T': 20,'R': 20, 'W': 50,'F': 50,'0':0,'1': 1,'2': 2,'3': 3,'4': 4,'5': 5,'6': 6,'7': 7,'8': 8,'9': 9}
while letters!="0\n":

#letters = "3||2||1||1:2,0,S,W||3:0,1,S||0||2||2:F,6||3:4,5,W,3,0||0||"
	data = letters.split("||") #split
	for temp in data:
	    #print temp,

	#print '\n'

		no_players = int(data[0])
	#print no_players 

	no_rounds = int(data[1])
	#print no_rounds

	df={}
	dr={}
	d={}
	j=len(data)

	summ1=0
	r=[]
	q=0
	w=0
	round_id=data[2]

	for v in range(2,j):
		if data[v]!="0" and len(data[v])>2:		
			x=len(data[v])
			for i in range(2,x,2):
				summ1=summ1+dt[data[v][i]]
			r.append(data[v][0])	
		elif data[v]=="0":
			#print summ1
			#print r
			for u in range(1,no_players+1):
				if str(u) not in r:
					q=u #winner
					#print q
			dr[round_id]=q		
			round_id=data[v+1]
		
			df[q]=summ1	
			summ1=0
			r=[]
	#print df
	#print dr

	for g in range(1,no_players+1):
		if g not in df.keys():
			w=g
			df[w]=0
	#print w
	
	for n, a in df.iteritems():
	    if a == max(df.values()):
		#print n
		d={"round_winners":dr,"overall_winner":n,"scores":df}
	#print d

	#if no_players!=len(df):
	j=json.dumps(d)
	sSock.sendall(j+"\n")
	letters = sSock.recv(1024)
sSock.close()
