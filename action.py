#!/usr/bin/env python
# -*- coding: utf8 -*- 

import sqlite3
import os.path
import datetime
import re
import yaml
import argparse
import sys

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

def initialize_log():
	create_log()
	create_todo()
	create_calendar()
	create_media()
	
# be careful using these! uncomment if you intend to erase the databases
def create_log():
	print "Creating tables for events, people, locations"
	query_db('CREATE TABLE IF NOT EXISTS events (category TEXT, time DATETIME, latitude DOUBLE, longitude DOUBLE, log TEXT)')
	query_db('CREATE TABLE IF NOT EXISTS people (name TEXT, alias TEXT)')
	query_db('CREATE TABLE IF NOT EXISTS locations (name TEXT, latitude DOUBLE, longitude DOUBLE)')

# be careful using these! uncomment if you intend to erase the databases
def create_todo():
	print "Creating tables for todo"
	query_db('CREATE TABLE IF NOT EXISTS todo (id INTEGER PRIMARY KEY, description TEXT, list_id INTEGER, parent_id INTEGER, status INTEGER, created DATETIME, completed DATETIME)')
	query_db('CREATE TABLE IF NOT EXISTS todo_archive (id INTEGER, description TEXT, list_id INTEGER, parent_id INTEGER, created DATETIME, completed DATETIME, archived DATETIME)')
	query_db('CREATE TABLE IF NOT EXISTS todo_lists (id INTEGER PRIMARY KEY, name TEXT, created DATETIME, archived DATETIME)')

def create_calendar():
	print "Creating calendar"
	query_db('CREATE TABLE IF NOT EXISTS calendar (id INTEGER PRIMARY KEY, name TEXT, description TEXT, start DATETIME, end DATETIME, created DATETIME)')

def create_media():
	query_db('CREATE TABLE IF NOT EXISTS  media (id INTEGER PRIMARY KEY, type TEXT, filepath TEXT, time DATETIME)')
	
def update_media():
	for root, dirs, files in os.walk(configuration['MEDIA_DIRECTORY']):
	    for name in files:
	        if name.lower().endswith((".png", ".jpg", ".jpeg")):
				actual_path = root + '/' + name
				local_path = 'images/' + root[21:] + '/' + name
				file_time = datetime.datetime.fromtimestamp(os.path.getmtime(actual_path))
				query = 'INSERT INTO media (type, filepath, time) VALUES ("image", "'+local_path+'", "'+str(file_time)+'")'
				query_db(query)
				
def format_time(ts):
	months = [ 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec' ]
	ts = ts.split(" ")
	dt = ts[0].split("-")
	tm = ts[1].split(":")
	timestring = "%s %s %s:%s" % (months[int(dt[1])-1], dt[2], tm[0], tm[1])
	return timestring
	
###COMMAND LINE PARSER CONFIGURATION###

def main(argv):
	args=parse_args(argv);

def init_parser():
        parser = argparse.ArgumentParser(description="A Tool to initialize the database for the Logger")
        parser.add_argument('-c','--config',help='Configuration File to Be Read; DEFAULT: config/default.yml')
        parser.add_argument('-m','--createmedia',help='Intialize Media MetaData into the database', action='store_false')
        parser.add_argument('-u','--updatemedia',help='Update Media MetaData into the database', action='store_false')
        parser.add_argument('-i','--initall',help='Initialize All Databases with Metadata', action='store_false')
        return parser

def parse_args(argv):
        parser=init_parser()
        args = parser.parse_args()
	if args.config:
		print "Setting new Configuration File"
		config_file = args.config
		configuration = yaml.load(config_file)
		DB_PATH = configuration["DB_FILE"]
        if args.initall == False:
		print "Initializing All Databases"
		initialize_log()
	if args.createmedia == False:
		print "Creating Meta Data Media Database Meta On DB_FILE"
		create_media()
	if args.updatemedia == False:
		print "Updating Media Database.."
		update_media()

main(sys.argv)
