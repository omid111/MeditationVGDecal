#!/usr/bin/env python2
"""runthemall.py
Runs all of the psychopy tests after each other.
"""
from psychopy import gui
import sys,sart,ospan,spanboard,digitspan,rcp,os
__author__ = "Omid Rhezaii"
__email__ = "omid@rhezaii.com"
__copyright__ = "Copyright 2015, Michael Silver Lab"
__credits__ = ["Omid Rhezaii", "Sahar Yousef", "Michael Silver"]

def main(argv):
  """Master runner main file"""
  #do only if we werent given initials from the command line
  if len(argv) == 1:
    while True:
      dlg = gui.DlgFromDict(dictionary={'Class ID':'','Test Number':'1'},title="SART Task")
      if(dlg.OK):
        initials = dlg.data[0]
        testNo = int(dlg.data[1])
      else:
        sys.exit(1)
      if os.path.isfile("data/"+initials+"/spanboard"+str(testNo)+".txt") or os.path.isfile("data/"+initials+"/ospan"+str(testNo)+".txt") or os.path.isfile("data/"+initials+"/digitspan"+str(testNo)+".txt") or os.path.isfile("data/"+initials+"/sart"+str(testNo)+".txt") or os.path.isfile("data/"+initials+"/rcp"+str(testNo)+".txt"):
        error = gui.Dlg(title="Existing Log File",labelButtonOK=u'Yes',labelButtonCancel=u'No')
        error.addText("A log file with initials " + initials+ " already exists. Are you sure you want to overwrite? If not, answer no and change your initials." )
        error.show()
        if error.OK:
          for temp in ["ospan","spanboard","digitspan","sart","rcp"]:
            if os.path.isfile("data/"+initials+"/"+temp+str(testNo)+".txt"):
              os.remove("data/"+initials+"/"+temp+str(testNo)+".txt")
          break
        else:
          continue
      else:
        break
  elif(len(argv)==3):
    initials = argv[1]
    testNo = int(argv[2])
  else:
    print "Too many command line arguments. Please read documentation."
    sys.exit(1)
  initials = initials.upper()

  args = ['',initials,testNo]
  spanboard.main(args)
  digitspan.main(args)
  ospan.main(args)
  sart.main(args)
  rcp.main(args)

if __name__ == '__main__': main(sys.argv)
