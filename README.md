# BanParty
BanParty is a follow on project to my Unliked script. It's a series of scripts using the Python Twitter library and written in Python 2.7. The scripts are as follows:

auth.py: Used to generate auth ID tokens to add to your creds.py file.

count.py: Create a csv called allbanids.csv containing the User ID of every Twitter user you block. This is subject to rate limiting and so you'll see it working in batches and then pausing for a while until the rate limit block ends.

load.py: Add the User ID of every Twitter handle in banlist.csv, as well as the User ID of every one of their followers, to banids.csv.

block.py: Go through banids.csv and block every single entry. Now includes protection to prevent it from blocking someone you follow. Stores already blocked ids in alreadyblocked.csv to prevent duplicating work.

culllist.py: This removes every entry from allbanids.csv and alreadyblocked.csv from the banids.csv file, as well as removing dupliactes. It also removes the user ids of any handle in safe.csv (used to prevent blocking accounts you don't follow).

These scripts use a LOT of memory (hundreds of MB or even GB). 

As GitHub has a 100MB file limit, I've put my copies of the CSV files here: https://banparty.circlelinego.com
