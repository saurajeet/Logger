#!/usr/bin/env python
# -*- coding: utf8 -*- 

import sqlite3
import os.path
import datetime
import re
import yaml

# name of your database
config_file = open(os.path.join(os.path.dirname(__file__), 'config/default.yml'), "r")
configuration = yaml.load(config_file)
DB_PATH = configuration["DB_FILE"]

# wrapper function for interacting with the sqlite database
def query_db(query, db=None):
	if db is None:	db = DB_PATH
	conn = sqlite3.connect(db)
	c = conn.cursor()
	c.execute(query)
	results = c.fetchall()
	conn.commit()
	conn.close()
	return results
				
def format_time(ts):
	months = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]
	ts = ts.split(" ")
	dt = ts[0].split("-")
	tm = ts[1].split(":")
	timestring = "%s %s %s:%s" % (months[int(dt[1])-1], dt[2], tm[0], tm[1])
	return timestring
