#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  run.py
#  
#  Copyright 2013 [mad]Berry <madberry@hush.com>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 

### Please send donations to:
#btc: 1Q2QDC78uaGgkm4r3G5YzZSriPv7KMUuQU
#ltc: Lb5TUyhdUtqsExLmiyqCLAiBZUrs8mEYze
# Thanks.  

import urllib2,urllib,os,simplejson

# Variables used to run the script

user='' #userid from the site
password = '' #password from the site
less_than = 55000 #Bet less than "offset" 
'''
60000 = 91.6%    odds wins     1.081x
55000 = 83.9%    odds wins     1.179x
32768 = 50.0%    odds wins     1.98x
16384 = 25.0%    odds wins     3.96x
 7000 = 10.7%    odds wins     9.268x
 2400 = 3.66%    odds wins    27.03x
 1000 = 1.53%    odds wins    64.88x
    1 = 0.00153% odds wins 64880x
'''
#max_bet = 4000 # Maximum bet 4000=0.00004 || Not used yet
min_bet = 1000 # Minimum bet can't be lower then 1000=0.00001
max_loss = 2 # stop after X losses
rate_limit = 0 #Rate limit in seconds, currently 1 bet per 10 sec.

#-------Any changes below this line might break the script------

__prog__ = "coinroll.it automated gambling script"
__scriptname__ = "run.py"
__author__ = "[mad]Berry"
__date__ = "$May 07, 2013 17:10:45 PM$"
__version__ = "1.0.01"

class Error(Exception):
    pass

def pause(n, post=False):
	import time
	import sys
	if post:
		print "Start : %s" % time.ctime()
	while n != 0:
		time.sleep(1)
		sys.stdout.write("Sleeping for: %d   \r" % (n) )
		sys.stdout.flush()
		n = n -1
	print "                     "

def call(api_url, **kwargs):
	try:
		baseurl = 'https://coinroll.it/'
		api_url = baseurl + api_url
		data = urllib.urlencode(kwargs) #({'user': user, 'password': password})
		header = {
					"Content-type": "application/x-www-form-urlencoded",
					"User-Agent" : "Coinroll Martingale by "+__author__+" Version "+ __version__
				}
		req = urllib2.Request(api_url, data, header)
		response = urllib2.urlopen(req)
		result = response.read()
		result = simplejson.loads(result)
		if 'error' in result:
		# An error occurred; raise an exception
			raise Error({'message': result['error']})
			exit(1)
		return result
	except Exception, e:
		print e.args[0]['message']
		exit(1)
		
def firstrun():
	print 'Loading first run procedures'
	if os.path.isfile('cred.txt'): 
		print 'Success we already have credentials'
		file = open('cred.txt','r')
		address = file.read()
		file.close()
		print address
		pass
	else:
		result = call('deposit/', user=user, password=password)
		file = open('cred.txt','w')
		file.write(result['address'])
		print 'Send a deposit to:', result['address'], 'to create the new account'
		file.close() 

def main():
	#check balance
	#result = call('getbets', user=user, password=password, offset=60000)
	#result = call('querybet', id='515e8d110c88')
	resultloss = call('getbalance', user=user, password=password)  ##get balance from api
	initial_loss = resultloss['bets'] - resultloss['wins']
	initial_wins = resultloss['wins']
	while True:  #start bet loop
			resultloss = call('getbalance', user=user, password=password)
			losses = resultloss['bets'] - resultloss['wins']
			if (losses >= max_loss):
				max_lost = initial_loss+max_loss
			else:
				max_lost = max_loss
			if (losses == max_lost):
				print 'Lost to much exiting'
				break;
			else:
				print "Won! \nplacing another bet I will stop after {0} losses".format(max_loss)
				result = call('bet',user=user, password=password, lessthan=less_than,amount=min_bet)
			pause(rate_limit) 
	return 0

if __name__ == '__main__':
	import logging
	import optparse
	parser = optparse.OptionParser(version= __prog__ + " " + __version__ + "\nDeveloped by: " + __author__)
	parser.add_option("-n", "--new", action="store_true", dest="new",
			help=("Add a new account, your address will be added to cred.txt"))
	(options, args) = parser.parse_args()
	if options.new == True:
		firstrun()
	else:
		main()

