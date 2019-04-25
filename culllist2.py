import argparse
import csv
import sys
import time
import os
from dateutil.parser import parse
from collections import OrderedDict
from shutil import copyfile


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
  
  with open("banids.csv.gold.cull","w") as makebanned:
    makebanned.write("")
  
  LINES=1000000    # MAX number of IDs to process at once
  PERCENTTICK = LINES/10
  IDLIST=[]
  sys.stdout.write("CullList.Py\nSTAGE 1 - SELF CULL\n")
  sys.stdout.write("CHUNK SIZE: "+str(LINES)+"\n")
  copyfile("banids.csv","banids.csv.raw.cull")
  RUNS=20
  RUN=0
  DEBUG=[]
  LASTWRITE=0
  while RUN < RUNS:
    RUN+=1
    sys.stdout.write("RUN "+str(RUN)+" of "+str(RUNS)+"\n")
    with open("banids.csv.raw.cull","r") as idfile:
      ISGOLD=True
      GOLDSET=1
      GOLD=[]
      ILINE=0
      TOTALGDD=0
      ISETS=0
      for idline in idfile:
        if ILINE < LINES:
          ILINE+=1
          IDLIST.append(idline)
        else:
          ILINE=0
          ISETS+=1
          ## PROCESS LINES ##
          IDSET=set(IDLIST)
          sys.stdout.write("SET "+str(ISETS)+": RAW "+str(len(IDLIST))+"\n")
          sys.stdout.write("SET "+str(ISETS)+": SDD "+str(len(IDSET))+"\n")
          IDLIST=[] # CLEAR RAM
          ## GOLD ##
          if ISETS == GOLDSET:
            GOLDSET=IDSET
            TOTALGDD+=len(GOLDSET)
            with open("banids.csv.gold.cull","a") as goldout:
              for ids in GOLDSET:
                goldout.write(ids+"\n")
          ## COMPARE OTHERS TO GOLD ##
          else:
            OSET=IDSET.difference(GOLDSET)
            with open("banids.csv.gold.cull","a") as goldout:
              for ids in GOLDSET:
                goldout.write(ids+"\n")
            sys.stdout.write("SET "+str(ISETS)+": GDD "+str(len(IDSET))+"\n")
            
          ##  END PROCESS  ##
      ## PROCESS FINAL LINES ##
      #if ISETS > GOLDSET:
      ##  END PROCESS FINAL  ##

    DEBUG.append("RUN "+str(RUN)+" ISETS " +str(ISETS)+" TOTALGDD "+str(TOTALGDD))
    copyfile("banids.csv.gold.cull","banids.csv.raw.cull")
  with open("debug.log","w") as debuglog:
    for line in DEBUG:
      debuglog.write(line+"\n")

def error(msg, exit_code=1):
    sys.stderr.write("Error: %s\n" % msg)
    exit(exit_code)

def main():

    cull()

if __name__ == "__main__":
    main()
