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


def uniq(list):
  last = object()
  for item in list:
    if item == last:
      continue
    yield item
    last = item

def sorter(l):
  return list(uniq(sorted(l)))

def load(api):
    IDLIST=[]
    IDTEMP=[]
    if debug == True:
      print "loading banlist.csv\n"
    with open("banlist.csv") as file:
      for row in csv.reader(file):
        IDTEMP.append(row)
    shuffle(IDTEMP)
    with open("banlist.csv","w") as file:
      for row in IDTEMP:
        file.write(str(row)+"\n")
    with open("banlist.csv") as file:
      if debug == True:
        print "loaded. loading banids.csv\n"
      with open("banids.csv") as ids:
        with open("banids.csv.temp","w") as idst:
          count = 1
          if debug == True:
            print "loaded. reading lines.\n"
          for row in csv.reader(ids):
            IDLIST.append(str(row[0]))
          if debug == True:
            print "read.\n"
          skiplike = False
          for row in csv.reader(file):
            user_name = str(row[0])
            print "Finding followers of "+user_name
            cursorn = "-1"
            try:
              while cursorn != 0: 
                USERS=api.GetFollowerIDsPaged(screen_name=user_name,cursor=cursorn,count=5000)
                USER_ID=api.GetUser(screen_name=user_name,include_entities=False)
                IDLIST.append(USER_ID.id)
                cursorn=int(USERS[0])
                if debug == True:
                  print USER_ID.id
                  print "NEXT CURSOR: "+str(cursorn)+"\n"
                  print "PREV CURSOR: "+str(USERS[1])+"\n"
                for user in USERS[2]:
                  try:
                    if debug == True:
                      print str(count)+":"+str(user)
                    IDLIST.append(str(user))
                    idst.write(str(user)+"\n")
                    count += 1
                  except twitter.TwitterError, err:
                    print "Exception: %s\n" % err.message
            except twitter.TwitterError, err:
              print "Exception: %s\n" % err.message
    if debug == True:
      print "\nFinished loading all user IDs. Sorting them.\n"
    IDSET = sorter(IDLIST)
    if debug == True:
      print "\nSorting Complete. Opening banids.csv for writing.\n"
    shuffle(IDSET)

    with open("banids.csv","w") as ids:
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
    

    api = twitter.Api(consumer_key,
                      consumer_secret,
                      access_token_key,
                      access_token_secret,
                      sleep_on_rate_limit=True)

    load(api)

if __name__ == "__main__":
    main()
