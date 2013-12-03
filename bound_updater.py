#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc
import sys

http_client = pyjsonrpc.HttpClient(
	url = "http://localhost:8080"
)

#print http_client.call("update", 1, 2)
# Result: 3

# It is also possible to use the *method* name as *attribute* name.
http_client.update(sys.argv[1], sys.argv[2])
# Result: 3
