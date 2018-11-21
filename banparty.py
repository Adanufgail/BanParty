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
WAIT = 15

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
        count = 0
        skiplike = False
        for row in csv.reader(file):
          user_name = str(row[0])
          print "Finding followers of "+user_name
          cursorn = "-1"
          try:
            while cursorn != 0: 
              USERS=api.GetFollowerIDsPaged(screen_name=user_name,cursor=cursorn,count=5000)
              cursorn=int(USERS[0])
              if debug == True:
                print "NEXT CURSOR: "+str(cursorn)+"\n"
                print "PREV CURSOR: "+str(USERS[1])+"\n"
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
      print "\nSorting Complete. Opening banids.csv for writing.\n"

    with open("banids.csv","w") as ids:
      if debug == True:
        print "\nFile open.\n"
      for X in IDSET:
        ids.write(str(X)+"\n")
        if debug == True:
          print(str(X))
    if debug == True:
      print "\writing complete.\n"
      


def delete(api):
    with open("banids.csv") as file:
        count = 0
        skiplike = False

        for row in csv.reader(file):
            tweet_id = int(row[0])
            try:
                 print tweet_id
                 if debug is True:
                   print api.GetStatus(status_id=tweet_id)
                   time.sleep(WAIT)
                 print "Recreating like"
                 print api.CreateFavorite(status_id=tweet_id)
                 countdown(WAIT)
                 #time.sleep(WAIT)
                 print "Deleting like"
                 print api.DestroyFavorite(status_id=tweet_id)
                 print count
                 count += 1
                 #time.sleep(WAIT)
                 countdown(WAIT)

            except twitter.TwitterError, err:
                 print "Exception: %s\n" % err.message
                 print "Attempting to delete like"
                 try:
                   countdown(WAIT)
                   #time.sleep(WAIT)
                   api.DestroyFavorite(status_id=tweet_id)
                   print count
                   count += 1
                 except twitter.TwitterError, err:
                    print "Exception: %s\n" % err.message

        print "Number of unliked tweets: %s\n" % count

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():

    print "Sleeping %i to be safe" % WAIT
    #time.sleep(WAIT)
    countdown(WAIT)
    parser = argparse.ArgumentParser(description="Delete old likes.")

    args = parser.parse_args()

    api = twitter.Api(consumer_key,
                      consumer_secret,
                      access_token_key,
                      access_token_secret,
                      sleep_on_rate_limit=True)

    load(api)
    #delete(api)

if __name__ == "__main__":
    main()
