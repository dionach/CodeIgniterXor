#!/usr/bin/python2
import base64
import itertools
import re
import sys
import urllib

# Copyright (c) 2014 Robin Bailey @ Dionach Ltd.

# Usage: $ testkey.py encryptedcookie.txt

cookieurl = open(sys.argv[1]).read().rstrip()
cookieb64 = urllib.unquote(cookieurl)
cookie = base64.b64decode(cookieb64)

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

#
# Key goes here
#
key = ""

# Length of the target hash in characters
# Should normally be 40 (sha1), but could be 32(md5)
HASH_LENGTH = 40

session = decode(key)
print(session)
