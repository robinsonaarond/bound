#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc

http_client = pyjsonrpc.HttpClient(
	url = "http://localhost:8080"
)

#print http_client.call("update", 1, 2)
# Result: 3

# It is also possible to use the *method* name as *attribute* name.
http_client.update("www.mytest.com", "5.6.7.8")
# Result: 3
