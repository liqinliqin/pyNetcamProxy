#!/usr/bin/python

""" Dump raw JPG images from a multipart JPEG stream """

import requests
import sys
import time

req = requests.get('http://hostname/videostream.cgi', auth=('user', 'password'), stream=True)

print req.headers

# Get our boundary marker
if req.headers['content-type'].startswith('multipart/'):
    print "Got a multipart stream!"
    boundary = req.headers['content-type'].rsplit(';boundary=')[1]
    print "[%s]" % boundary
else:
    print "Looks like we're not being fed multipart data?"
    sys.exit(1)

while True:
    # Snarf the beginning of the request, to find our headers
    chunk_split = req.raw.read(1024).split("\r\n\r\n", 1)
    for head in chunk_split[0].splitlines():
        if head.startswith("Content-Length:"):
            clen = head.split(": ", 1)[1]
            print "Content len is %d" % int(clen)
    
    #print "%d bytes remaining..." % len(chunk_split[1])
    remaining = int(clen) - len(chunk_split[1])
    #print "Need to read %d bytes more" % remaining
    
    img = chunk_split[1] + req.raw.read(remaining)
    print "Image is %d bytes long" % len(img)
    
    f = open('img-%s.jpg' % time.time(), 'wb')
    f.write(img)
    f.close()
