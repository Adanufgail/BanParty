#!/usr/bin/env python

import argparse
import csv
import sys
import time
import os
import twitter
from dateutil.parser import parse
import creds

__author__ = "Koen Rouwhorst"
__version__ = "0.1"

import creds
consumer_key = creds.apikeys['consumer_key']
consumer_secret = creds.apikeys['consumer_secret']
access_token_key = creds.apikeys['access_key']
access_token_secret = creds.apikeys['access_secret']

debug = False
WAIT = 30

def countdown(t):
    while t > 0:
        sys.stdout.write('\r{}     '.format(t))
        t -= 1
        sys.stdout.flush()
        time.sleep(1)

def delete(api):
    with open("like2.js") as file:
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

    delete(api)

if __name__ == "__main__":
    main()
