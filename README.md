# Logger

[Logger](http://genekogan.com/writing/intro-to-logger.html) is a mostly personal project to create a quick and simple dashboard to log notes, ideas, commentary, and todo lists into an electronic journal to keep an ongoing record of my own personal activities. Entries are placed into a database along with a timestamp and geolocation (when connected to internet), with various twitter-style reserved characters used to track entities over time. There is also functionality for making simple, locally-served to-do lists.

In the note-taking component, the following conventions apply:

	@   locations (e.g. @NewYork)
	~   people (e.g. ~AbrahamLincoln)
	#   project, thing, tag
	!() idea
	%() comment
	?() question
	^() web link

The logging utility is written in python and the database is maintained using [SQLite](http://www.sqlite.org/).  Alfred is used to make a convenient shortcut for adding entries.

Viewing and interacting with the database is done through a browser, entirely through the localhost machine via lightweight local webserver setup by [CherryPy](http://www.cherrypy.org/). In the future, analytical tools will be developed to query the database and pull out meaningful statistics and generate summaries.

## Configuration File

You may choose to override some or more features of the Personal Logger by Using a Config File. The default location of the configuration file can be found at config directory in the default program location. The default location of the file is "config/default.yml". Include the following lines in the config file to start.

	DB_FILE: /home/saurajeet/.logger/universe.db
	MEDIA_DIRECTORY: /home/saurajeet/Pictures


## Usage

The file actions.py has a bunch of utilities for managing databases, including one important one for initializing the events table.

	$ python action.py -h
	usage: action.py [-h] [-c CONFIG] [-m] [-u] [-i]
	
	A Tool to initialize the database for the Logger
	
	optional arguments:
	  -h, --help            show this help message and exit
	  -c CONFIG, --config CONFIG
	                        Configuration File to Be Read; DEFAULT:
	                        config/default.yml
	  -m, --createmedia     Intialize Media MetaData into the database
	  -u, --updatemedia     Update Media MetaData into the database
	  -i, --initall         Initialize All Databases with Metadata
		
	$ python action.py --initall
	Initializing All Databases
	Creating tables for events, people, locations
	Creating tables for todo
	Creating calendar

	$ python action.py --createmedia
	Creating Meta Data Media Database Meta On DB_FILE
 
	$ python action.py --updatemedia
	Updating Media Database..
	

Once Meta of all Tables have been generated, we are good to start logging our personal events

	python /path/to/Logger/log.py log "this is the text i want to log"

Optionally, the timestamp can be overridden if say the entry is being made later than the time of the event being logged. Must be in format MM/DD/YYYY HH:MM (or just HH:MM if date stays same) in 24-hour time.

	python log.py log "this event will have a different timestamp %(8/14/2012 19:22)"

If you have an internet connection, it will automatically log the gps coordinates with the post. You can also override the location stamp with a link to a lookup in a locations table. To add locations to the table, use the following example.

	python log.py location "StatueOfLiberty" 40.689249 -74.0445

You can then override the location in a log post using the following notation,

	python log.py log "this event will have a different location @(StatueOfLiberty)"

Another useful function is the ability to create replacement strings, useful if you want to use a nickname or shorthand for a longer tag. The following example converts all instances of ~john to ~JohnSmith in the database.

	python log.py name JohnSmith john


## Viewing

The data can be interacted with through a browser. First download and install [CherryPy](http://www.cherrypy.org/).  The following command will launch a local server on which you can see your log data.

	python view.py

After launching, open a browser and navigate to localhost:8080. The basic interface currently supports viewing entries on specific days and by specific keyword searches. In the future this will be extended with data visualization techniques.


## Todo

A simple todo utility can be found at localhost:8080/todo. The interface is similar to Google Tasks with infinitely nestable lists. More documentation later.


## Calendar

A simple calendar utility can be found at localhost:8080/calendar. The interface is similar to Google Calendar. More documentation later.


## Extending with Alfred

[Alfred](http://www.alfredapp.com/) is an OSX app which is an alternative to Spotlight.  A handy functionality is extensions which lets you add your own keywords for launching scripts from the search bar. By adding the following script to the extensions and assigning it keyword "log", entries can be added quickly via Alfred, e.g. "log add this to my database"

	python /path/to/Logger/log.py "{query}"

