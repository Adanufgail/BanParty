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


def block(api):
  with open("banids.csv") as ids:
    if debug == True:
      print "loaded. reading lines.\n"
    for row in csv.reader(ids):
        try:
            IDLIST.append(str(row[0]))
        except:
            print "O"
    if debug == True:
        print "read.\n"
    if debug == True:
      print "Finished loading all user IDs. Sorting them.\n"
      print ""+str(len(IDLIST))+" USERS\n"
    IDSET=sorter(IDLIST)


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
          try:
            api.DestroyBlock(user_id=str(safeuser.id),include_entities=False,skip_status=True)
            IDSET.remove(str(safeuser.id))
          except:
            print ""
          api.DestroyBlock(user_id=safeuser.id,include_entities=False,skip_status=True)
        except twitter.TwitterError, err:
          print "Exception: %s\n" % err.message
          
    #subtract friends
    if debug == True:
      print ""+str(len(IDSET))+" after cleanup\n"
      print "Done. Loading Your Followers.\n"
    cursorn = -1
    try:
      while cursorn != 0:
        if debug == True:
          print "IN TRY\n"
        #FRIENDS=api.GetFollowerIDsPaged(cursor=cursorn)
        FRIENDS=api.GetFriendsPaged(cursor=cursorn)
        if debug == True:
          print "API DONE\n"
        cursorn=int(FRIENDS[0])
        if debug == True:
          print "next cursor "+str(cursorn)+"\n"
          print "prev cursor "+str(FRIENDS[1])+"\n"
        for user in FRIENDS[2]:
          if debug == True:
            print ""+str(user.id)+"\n"
          try:
            IDSET.remove(str(user.id))
          except:
            print ""+str(user.id)+" is not in blocklist\n"
    except twitter.TwitterError, err:
      print "Exception: %s\n" % err.message

    # shuffle list
    if debug == True:
      print ""+str(len(IDSET))+" after removing people you follow\n"
    shuffle(IDSET)
    count = 0

    #DO THE BANNING!
    with open("alreadybanned.csv","a") as addban:
      for row in IDSET:
        user_id = int(row)
        try:
          if debug is True:
            print user_id
          print "Blocking user"
          api.CreateBlock(user_id=user_id,include_entities=False,skip_status=True)
          count += 1
          addban.write(str(user_id)+"\n")
          print count

        except twitter.TwitterError, err:
          print "Exception: %s\n" % err.message
          print "Attempting to block"
          try:
            api.CreateBlock(user_id=user_id,include_entities=False,skip_status=True)
            count += 1
            addban.write(str(user_id)+"\n")
            print count
          except twitter.TwitterError, err:
            print "Exception: %s\n" % err.message

  print "Number of blocked users: %s\n" % count

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
      block(api)
    except:
      FATAL += 1

if __name__ == "__main__":
    main()
