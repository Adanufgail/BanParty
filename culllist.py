import argparse
import csv
import sys
import time
import os
from dateutil.parser import parse
from collections import OrderedDict
from shutil import copyfile

def uniq(list):
  last = object()
  for item in list:
    if item == last:
      continue
    yield item
    last = item

def sorter(l):
  return list(uniq(sorted(l)))

def cullout(DONE,TOTALCOUNT):
  COUNT=0
  with open("banids.csv.cull","a") as ids:
    for ID in DONE:
      COUNT += 1
      ids.write(ID)
  sys.stdout.write(" WROTE "+str(COUNT)+" LINES TO banids.csv.cull. CURRENT TOTAL LINES: "+str(TOTALCOUNT+COUNT)+"\n")
  return COUNT
  

def cull():
  if not os.path.isfile("alreadybanned.csv"):
    with open("alreadybanned.csv") as makebanned:
      makebanned.write("")
    print ""

  if not os.path.isfile("banids.csv"):
    with open("banids.csv") as makebanned:
      makebanned.write("")
    print ""

  if not os.path.isfile("allbanids.csv"):
    with open("allbanids.csv") as makebanned:
      makebanned.write("")

  with open("banids.csv.cull","w") as makebanned:
    makebanned.write("")
  
  IDLIST=[]
  ALLIDLIST=[]
  ALRIDLIST=[]
  DONE=[]
  COUNTI=0        # Current Count of IDs from BANIDS
  COUNTA=0        # Current Count of IDs from OTHER FILES
  LINES=1000000    # MAX number of IDs to process at once
  PERCENTTICK = LINES/10
  LINES = LINES - 1
  TOTALDUPE=0
  TOTALCOUNT=0
  with open("banids.csv") as ids:
    for ID in ids:
      COUNTI += 1
      IDLIST.append(ID)
      if COUNTI%PERCENTTICK == 0:
        sys.stdout.write("X")
      if COUNTI > LINES:
        LENB=len(IDLIST)
        IDLISTSET=set(IDLIST)
        LENA=len(IDLISTSET)
        DIFF=LENB-LENA
        IDLIST=[]
        TOTALDUPE += DIFF
        sys.stdout.write(" LOADED "+str(COUNTI)+" LINES FROM banids.csv. REMOVED "+str(DIFF)+" DUPLICATES ("+str(TOTALDUPE)+" TOTAL).\n")
        COUNTA=0
        COUNTI=0
        with open("allbanids.csv") as ida:
      	  for IDA in ida:
            COUNTA += 1
            ALLIDLIST.append(IDA)
            if COUNTA%PERCENTTICK == 0:
              sys.stdout.write("Y")
            if COUNTA > LINES:
              ALLIDLISTSET=set(ALLIDLIST)
              ALLIDLIST=[]
              DONE=IDLISTSET.difference(ALLIDLISTSET)
              DIFF=len(IDLISTSET)-len(DONE)
              IDLISTSET=DONE
              TOTALDUPE += DIFF
              sys.stdout.write(" LOADED "+str(COUNTA)+" LINES FROM allbanids.csv. REMOVED "+str(DIFF)+" DUPLICATES\n")
              COUNTA=0
            #ONCE MORE
          ALLIDLISTSET=set(ALLIDLIST)
          ALLIDLIST=[]
          DONE=IDLISTSET.difference(ALLIDLISTSET)
          DIFF=len(IDLISTSET)-len(DONE)
          IDLISTSET=DONE
          TOTALDUPE += DIFF
          sys.stdout.write(" LOADED "+str(COUNTA)+" LINES FROM allbanids.csv. REMOVED "+str(DIFF)+" DUPLICATES ("+str(TOTALDUPE)+" TOTAL).\n")
          COUNTA=0
        with open("alreadybanned.csv") as ida:
      	  for IDA in ida:
            COUNTA += 1
            ALLIDLIST.append(IDA)
            if COUNTA%PERCENTTICK == 0:
              sys.stdout.write("Z")
            if COUNTA > LINES:
              ALLIDLISTSET=set(ALLIDLIST)
              DONE=IDLISTSET.difference(ALLIDLISTSET)
              IDLISTSET=DONE
              DIFF=len(IDLISTSET)-len(DONE)
              TOTALDUPE += DIFF
              sys.stdout.write(" LOADED "+str(COUNTA)+" LINES FROM alreadybanids.csv. REMOVED "+str(DIFF)+" DUPLICATES ("+str(TOTALDUPE)+" TOTAL).")
              TOTALCOUNT += cullout(DONE,TOTALCOUNT) 
              COUNTA=0
          ALLIDLISTSET=set(ALLIDLIST)
          DONE=IDLISTSET.difference(ALLIDLISTSET)
          DIFF=len(IDLISTSET)-len(DONE)
          IDLISTSET=DONE
          TOTALDUPE += DIFF
          sys.stdout.write(" LOADED "+str(COUNTA)+" LINES FROM alreadybanids.csv. REMOVED "+str(DIFF)+" DUPLICATES ("+str(TOTALDUPE)+" TOTAL).")
          TOTALCOUNT += cullout(DONE,TOTALCOUNT) 
          COUNTA=0

  

  
  sys.stdout.write("TOTAL DUPES: "+str(TOTALDUPE)+"\n")
  sys.stdout.write("TOTAL COUNT: "+str(TOTALCOUNT)+"\n")
  sys.stdout.write("COPYING TO BANIDS.CSV\n")
  copyfile("banids.csv.cull","banids.csv")
      
    
  #IDSET=sorter(IDLIST)
  #print len(IDSET)

  #with open("banids.csv","w") as ids:
    #for ID in IDSET:
      #ids.write(ID)

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():

    cull()

if __name__ == "__main__":
    main()
