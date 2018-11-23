#!/usr/bin/env python

import argparse
import csv
import sys
import time
import os
import twitter
from dateutil.parser import parse
import creds
from collections import OrderedDict

__author__ = "Michael Lubert"
__version__ = "0.1"

import creds
consumer_key = creds.apikeys['consumer_key']
consumer_secret = creds.apikeys['consumer_secret']
access_token_key = creds.apikeys['access_key']
access_token_secret = creds.apikeys['access_secret']

debug = True
WAIT=120

def countdown(t):
    while t > 0:
        sys.stdout.write('\r{}     '.format(t))
        t -= 1
        sys.stdout.flush()
        time.sleep(1)
    sys.stdout.write('\r{}     ')

def uniq(list):
  last = object()
  for item in list:
    if item == last:
      continue
    yield item
    last = item

def sorter(l):
  return list(uniq(sorted(l)))

def count(api):
  LENGTH=0
  cursorn=-1
  try:
    while cursorn != 0: 
      USERS=api.GetBlocksIDsPaged(cursor=cursorn)
      print "LENGTH: "+str(len(USERS[2]))+"\n"
      print "CURRENT TOTAL: "+str(LENGTH)+"\n"
      LENGTH=LENGTH+len(USERS[2])
      cursorn=int(USERS[0])
      countdown(WAIT)
  except twitter.TwitterError, err:
    print "Exception: %s\n" % err.message
  print "TOTAL LENGTH: "+str(LENGTH)+"\n"    

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():

    print "Sleeping %i to be safe" % WAIT
    countdown(WAIT)
    

    api = twitter.Api(consumer_key,
                      consumer_secret,
                      access_token_key,
                      access_token_secret,
                      sleep_on_rate_limit=True)

    count(api)

if __name__ == "__main__":
    main()
