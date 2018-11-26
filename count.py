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
  return list(uniq(sorted(l)))

def count(api):
  IDLIST=[]
  cursorn = "-1"
  try:
    while cursorn != 0: 
      USERS=api.GetBlocksIDsPaged(cursor=cursorn)
      cursorn=int(USERS[0])
      for user in USERS[2]:
        try:
          if debug == True:
            print str(user)
          IDLIST.append(str(user))
        except twitter.TwitterError, err:
          print "Exception: %s\n" % err.message
      countdown(WAIT)
  except twitter.TwitterError, err:
    print "Exception: %s\n" % err.message
  if debug == True:
      print "\nFinished loading all user IDs. Sorting them.\n"
  IDSET = sorter(IDLIST)
  if debug == True:
    print "\nSorting Complete. Opening allbanids.csv for writing.\n"

  with open("allbanids.csv","w") as ids:
    if debug == True:
      print "\nFile open.\n"
    for X in IDSET:
      ids.write(str(X)+"\n")
      if debug == True:
        print(str(X))
  if debug == True:
    print "\writing complete.\n"
      

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
