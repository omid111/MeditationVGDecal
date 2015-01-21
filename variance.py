#!/usr/bin/env python2
"""variance.py:
A script to analyze the variance of subjects from block to block.
Graphs are outputed in a folder called "analysis".
"""
import os,glob,sys
import matplotlib.pyplot as plt
__author__ = "Omid Rhezaii"
__email__ = "omid@rhezaii.com"
__copyright__ = "Copyright 2015, Michael Silver Lab"
__credits__ = ["Omid Rhezaii", "Sahar Yousef", "Michael Silver"]

def main():
  """Main function."""
  for span in ["ospan","spanboard","digitspan"]:
    ospan = False
    if span == "ospan":
      ospan = True
      mathdata = dict()
    data = dict()
    identitydata = dict()
    positiondata = dict()
    accuracydata = dict()
    reduceddata = dict()
    for fn in glob.glob("data/*/"+span+"?.txt"):
      initials = fn.split("/")[1]
      if ospan:
        mathdata[initials] = []
        reduceddata[initials] = []
      data[initials] = []
      identitydata[initials] = []
      positiondata[initials] = []
      accuracydata[initials] = []
      with open(fn, 'r') as f:
        if ospan:
          mathlist = []
          tempmathlist = []
          tempospans = [0,]
        identitylist = []
        positionlist = []
        accuracylist = []
        while True:
          temp = f.readline()
          if "(" in temp:
            temp = temp.split("(")[1][:-2]
            if ospan and len(temp.split(",")) == 2:
              if temp.replace("'","").split(",")[0] == "True":
                mathlist.append(1)
                tempmathlist.append(1)
              else:
                mathlist.append(0)
                tempmathlist.append(0)
            else:
              regex = ",["
              if regex not in temp:
                regex = ", ["
              for t in temp.split(regex)[3].split("],")[0].replace(" ","").replace("'","").split(","):
                if t =="":
                  continue
                if t[0] == 'T':
                  positionlist.append(1)
                  accuracylist.append(1)
                else:
                  positionlist.append(0)
                  accuracylist.append(0)
                if t[1] == 'T':
                  identitylist.append(1)
                  accuracylist.append(1)
                else:
                  identitylist.append(0)
                  accuracylist.append(0)
              if ospan:
                if len(tempmathlist) > 0:
                  tempmathscore = (100.0*sum(tempmathlist))/len(tempmathlist)
                  a = len(tempmathlist)
                else:
                  tempmathscore = 0
                tempmathlist = []
                if tempmathscore >= 85:
                  if temp[:temp.index(",")].replace("'","") == "True":
                    j = temp.rindex(",")
                    tempospans.append(a)
          else:
            if ospan:
              tempmathlist = []
          if "Max " in temp or temp=="":
            if ospan and len(mathlist) > 0:
              reduceddata[initials].append(max(tempospans))
              tempospans = []
              mathdata[initials].append((100.0*sum(mathlist))/len(mathlist))
            if temp != "":
              data[initials].append(int(temp.split(":")[2]))
            if len(identitylist) > 0:
              identitydata[initials].append((100.0*sum(identitylist))/len(identitylist))
            if len(positionlist) > 0:
              positiondata[initials].append((100.0*sum(positionlist))/len(positionlist))
            if len(accuracylist) > 0:
              accuracydata[initials].append((100.0*sum(accuracylist))/len(accuracylist))
            if ospan:
              mathlist = []
            identitylist = []
            positionlist = []
            accuracylist = []
          if temp == "":
            break
    if span == "digitspan":
      i1 = data.copy()
      i2 = data.copy()
      id1 = identitydata.copy()
      pd1 = identitydata.copy()
      ad1 = identitydata.copy()
      id2 = identitydata.copy()
      pd2 = identitydata.copy()
      ad2 = identitydata.copy()
      for key in id1.keys():
        if len(id1[key]) > 0:
          splice = 3
          if len(i1[key]) == 2:
            splice = 1
          id1[key] = id1[key][:splice]
        else:
          del id1[key]
      for key in pd1.keys():
        if len(pd1[key])>0:
          splice = 3
          if len(pd1[key]) == 2:
            splice = 1
          pd1[key] = pd1[key][:splice]
        else:
          del pd1[key]
      for key in ad1.keys():
        if len(ad1[key])>0:
          splice = 3
          if len(ad1[key]) == 2:
            splice = 1
          ad1[key] = ad1[key][:splice]
        else:
          del ad1[key]
      for key in id2.keys():
        if len(id2[key])>0:
          splice = 3
          if len(id1[key]) == 2:
            splice = 1
          id2[key] = id2[key][splice:]
        else:
          del id2[key]
      for key in pd2.keys():
        if len(pd2[key]) > 0:
          splice = 3
          if len(pd2[key]) == 2:
            splice = 1
          pd2[key] = pd2[key][splice:]
        else:
          del pd2[key]
      for key in ad2.keys():
        if len(ad2[key])>0:
          splice = 3
          if len(ad2[key]) == 2:
            splice = 1
          ad2[key] = ad2[key][splice:]
        else:
          del ad2[key]
      for key in i1.keys():
        if len(i1[key])>0:
          splice = 3
          if len(i1[key]) == 2:
            splice = 1
          i1[key] = i1[key][:splice]
        else:
          del i1[key]
      for key in i2.keys():
        if len(i2[key])>0:
          splice = 3
          if len(i2[key]) == 2:
            splice = 1
          i2[key] = i2[key][splice:]
        else:
          del i2[key]
      plot("Max Forward "+span.upper(),"Performance",i1,10,"forward"+span)
      plot("Forward Identity Accuracy","Performance(%)",id1,100,"forward"+span)
      plot("Forward Position Accuracy","Performance(%)",pd1,100,"forward"+span)
      plot("Forward Overall Accuracy","Performance(%)",ad1,100,"forward"+span)
      plot("Max Reverse "+span.upper(),"Performance",i2,10,"reverse"+span)
      plot("Reverse Identity Accuracy","Performance(%)",id2,100,"reverse"+span)
      plot("Reverse Position Accuracy","Performance(%)",pd2,100,"reverse"+span)
      plot("Reverse Overall Accuracy","Performance(%)",ad2,100,"reverse"+span)
    else:
      plot("Max "+span.upper(),"Performance",data,10,span)
      if ospan:
        if len(reduceddata) > 0:
          plot("Accurate Math Max OSPAN","Performance",reduceddata,10,span)
        plot("Math Performance","Performance(%)",mathdata,100,span)
      plot("Identity Accuracy","Performance(%)",identitydata,100,span)
      plot("Position Accuracy","Performance(%)",positiondata,100,span)
      plot("Overall Accuracy","Performance(%)",accuracydata,100,span)

def plot(title, ylabel,data,toprange,span):
  """Make a simpe pyplot.

  Arguments:
  @param title - title of pyplot
  @param ylabel - y axis label text
  @param data - data for each block for each subject
  @param toprange - highest y value
  @param span - the type of span we are graphing
  """
  fig = plt.figure()
  ax = fig.add_subplot(111)
  x = [1,2,3]
  nodata = True
  for key in data.keys():
    if len(data[key]) > 0:
      nodata = False
      ax.plot(x[:len(data[key])],data[key],marker='o',label=key)
  if nodata:
    print data
    print "none"
    plt.close()
    return
  plt.xlabel("Block Number")
  plt.ylabel("Performance")
  plt.xticks(x)
  plt.legend()
  plt.axis([0,len(x)+1,0,0.1+toprange])
  plt.title(title)
  if not os.path.isdir("analysis"):
    os.mkdir("analysis")
  if not os.path.isdir("analysis/"+span):
    os.mkdir("analysis/"+span)
  plt.savefig("analysis/"+span+"/"+title.replace(" ","").lower()+".png")
  plt.close()

if __name__ == '__main__': main()
