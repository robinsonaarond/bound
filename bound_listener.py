#! /usr/bin/env python

import sqlite3
import pyjsonrpc

def update_domain(url, ip):
	conn = sqlite3.connect(r"bound.db")
	cur = conn.cursor()
	cur.execute('CREATE TABLE IF NOT EXISTS A ( URL TEXT PRIMARY KEY NOT NULL, IP text NOT NULL )')
	try:
		cur.execute('INSERT or REPLACE into A values ("'+url+'", "'+ip+'")')
		print "Insert/Replace of %s, %s successful." % (url, ip)
		#data = cur.fetchone()[0]
	except Exception, e:
		print "Insert/Replace of %s, %s unsuccessful." % (url, ip), e
	#return "URL was: %s, IP was: %s" % (url, ip)
	conn.commit()
	return 0

class RequestHandler(pyjsonrpc.HttpRequestHandler):
	# Register public JSON-RPC methods
	methods = {
		"update": update_domain
	}

# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
	server_address = ('localhost', 8080),
	RequestHandlerClass = RequestHandler
	)
print "Starting HTTP server ..."
print "URL: http://localhost:8080"
#http_server.serve_forever()
http_server.serve_forever()

