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
from shutil import copyfile

__author__ = "Michael Lubert"
__version__ = "0.1"

import creds
consumer_key = creds.apikeys['consumer_key']
consumer_secret = creds.apikeys['consumer_secret']
access_token_key = creds.apikeys['access_key']
access_token_secret = creds.apikeys['access_secret']

debug = True
WAIT=0

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
  counter = 1
  cursorn = "-1"
  with open("allbanids.csv.tmp","w",0) as ids:
    try:
      while cursorn != 0: 
        USERS=api.GetBlocksIDsPaged(cursor=cursorn)
        cursorn=int(USERS[0])
        for user in USERS[2]:
          try:
            if debug == True:
              print str(counter)+": "+str(user)
            ids.write(str(user)+"\n")
            counter += 1
          except twitter.TwitterError, err:
            print "Exception: %s\n" % err.message
        countdown(WAIT)
    except twitter.TwitterError, err:
      print "Exception: %s\n" % err.message
    if debug == True:
        print "\nFinished loading all user IDs.\n"
    copyfile("allbanids.csv.tmp","allbanids.csv")
      

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():


    api = twitter.Api(consumer_key,
                      consumer_secret,
                      access_token_key,
                      access_token_secret,
                      sleep_on_rate_limit=True)

    count(api)

if __name__ == "__main__":
    main()
