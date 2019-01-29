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


def block(api):
  BATCH=1000000
  BATCHCOUNT=0
  IDLIST=[]
  TOTAL=0
  COUNT=0
  with open("banids.csv") as ids:
    if debug == True:
      print "loaded. reading lines.\n"
    for row in csv.reader(ids):
        try:
            IDLIST.append(str(row[0]))
            COUNT += 1
        except Exception, err:
            print "Exception: %s\n" % err.message
        if COUNT > BATCH:
          COUNT=0
          BATCHCOUNT += 1
          print "batch count of "+str(BATCH)+" reached. current batch: "+str(BATCHCOUNT)+"\n"
          #subtract friends
          cursorn = -1
          try:
            while cursorn != 0:
              FRIENDS=api.GetFriendsPaged(cursor=cursorn)
              if debug == True:
                print "API DONE\n"
              cursorn=int(FRIENDS[0])
              for user in FRIENDS[2]:
                if debug == True:
                  print ""+str(user.id)+""
                try:
                  IDLIST.remove(str(user.id))
                except:
                  print " "+str(user.id)+" is not in blocklist\n"
          except twitter.TwitterError, err:
            print "Exception: %s\n" % err.message
          TOTAL += banem(IDLIST,api,BATCHCOUNT)
          IDLIST=[]
    if debug == True:
        print "read.\n"
    if debug == True:
      print "Finished loading all user IDs.\n"
      print ""+str(len(IDLIST))+" USERS\n"

  print "Number of blocked users: %s\n" % TOTAL


    ## shuffle list
    #if debug == True:
    #  print ""+str(len(IDLIST))+" after removing people you follow\n Sorting list\n"
    #IDSET=sorter(IDLIST)
    #if debug == True:
    #  print ""+str(len(IDLIST))+" after sorting \n"
    #shuffle(IDSET)

def banem(IDSET, api,BATCHCOUNT):
    count = 0

    #DO THE BANNING!
    with open("alreadybanned.csv","a") as addban:
      for row in IDSET:
        user_id = int(row)
        try:
          if debug is True:
            sys.stdout.write(str(user_id))
          sys.stdout.write(' blocking user.')
          api.CreateBlock(user_id=user_id,include_entities=False,skip_status=True)
          count += 1
          addban.write(str(user_id)+"\n")
          sys.stdout.write(' total: '+str(count)+"\n")
          

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

      return count


def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():
  api = twitter.Api(consumer_key,
    consumer_secret,
    access_token_key,
    access_token_secret,
    sleep_on_rate_limit=True)
  block(api)

if __name__ == "__main__":
    main()
