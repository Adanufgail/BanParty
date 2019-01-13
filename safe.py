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
WAIT=0
IDLIST=[]

def uniq(list):
  last = object()
  for item in list:
    if item == last:
      continue
    yield item
    last = item

def sorter(l):
  return list(uniq(sorted(l)))


def safe(api):
    #subtract safe.csv
    with open("safe.csv") as safes:
      if debug == True:
        print "Opened safe.csv\n"
      for row in csv.reader(safes):
        try:
          if debug == True:
            print ""+str(row[0])+"\n"
          safeuser=api.GetUser(screen_name=row[0])
          if debug == True:
            print ""+str(safeuser.id)+"\n"
          api.DestroyBlock(user_id=str(safeuser.id),include_entities=False,skip_status=True)
        except twitter.TwitterError, err:
          print "Exception: %s\n" % err.message
          

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():
  api = twitter.Api(consumer_key,
    consumer_secret,
    access_token_key,
    access_token_secret,
    sleep_on_rate_limit=True)
  FATAL=0
  while FATAL < 1:  
    try:
      safe(api)
    except:
      FATAL += 1

if __name__ == "__main__":
    main()
