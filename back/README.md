Install:
	python setup.py install

Create config file:
	HOST = "irc.twitch.tv"
	PORT = 6667
	USERNAME = USERNAME
	PASSWORD = PASSWORD
	CHANNEL = CHANNEL
	UNLIMITED = False

Run:
	parabot <config>

API routes:
	/run_parabot : run parabot and/or connect to channel
	/stop_parabot : disconnect parabot from channel
	/summary : get current status as json data
