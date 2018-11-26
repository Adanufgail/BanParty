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
from random import shuffle

__author__ = "Michael Lubert"
__version__ = "0.1"

import creds
consumer_key = creds.apikeys['consumer_key']
consumer_secret = creds.apikeys['consumer_secret']
access_token_key = creds.apikeys['access_key']
access_token_secret = creds.apikeys['access_secret']

debug = True
WAIT=1

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
  return shuffle(list(uniq(sorted(l))))

def load(api):
    IDLIST=[]
    if debug == True:
      print "loading banlist.csv\n"
    with open("banlist.csv") as file:
      if debug == True:
        print "loaded. loading banids.csv\n"
      with open("banids.csv") as ids:
        if debug == True:
          print "loaded. reading lines.\n"
        for row in csv.reader(ids):
          IDLIST.append(str(row[0]))
        if debug == True:
          print "read.\n"
    if debug == True:
      print "\nFinished loading all user IDs. Sorting them.\n"
    IDSET = sorter(IDLIST)

def block(api):
    with open("banids.csv") as file:
        count = 0

        for row in csv.reader(file):
            user_id = int(row[0])
            try:
                 if debug is True:
                   print user_id
                   print "Blocking user"
                 api.CreateBlock(user_id=user_id,include_entities=False,skip_status=True)
                 countdown(WAIT)
                 count += 1
                 print count
                 countdown(WAIT)

            except twitter.TwitterError, err:
                 print "Exception: %s\n" % err.message
                 print "Attempting to block"
                 try:
                   countdown(WAIT)
                   api.CreateBlock(user_id=user_id,include_entities=False,skip_status=True)
                   count += 1
                   print count
                 except twitter.TwitterError, err:
                    print "Exception: %s\n" % err.message

        print "Number of blocked users: %s\n" % count

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

    load(api)
    block(api)

if __name__ == "__main__":
    main()
