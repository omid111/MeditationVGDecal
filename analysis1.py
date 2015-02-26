#!/usr/bin/env python2
"""variance.py:
A script to analyze subjects performance
Graphs are outputed in a folder called "analysis1".
"""
import os,glob,sys,random
import matplotlib.pyplot as plt
from scipy import stats
__author__ = "Omid Rhezaii"
__email__ = "omid@rhezaii.com"
__copyright__ = "Copyright 2015, Michael Silver Lab"
__credits__ = ["Omid Rhezaii", "Sahar Yousef", "Michael Silver"]

def main():
  """Main function."""
  analyze_spanboard()
  analyze_digitspan()
  analyze_ospan()
  analyze_sart()
  analyze_rcp()


def oldmain():
  """Old main function"""
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


def analyze_spanboard():
  """Analyze all data from spanboard test."""
  spansboard = dict()
  print "Reading spanboard: "
  for fn in glob.glob("data/7[4-6]??"):
    if os.path.isdir(fn):
      sid = fn.split("/")[-1]
      if not os.path.isfile(fn+"/digitspan1.txt"):
        print "Warning! No spanboard for:" + sid
        continue
      spansboard[sid] = []
      with open(fn+"/spanboard1.txt", 'r') as f:
        for line in f:
          if "Subject" in line:
            if sid != line.split(":")[2].strip():
              print "Error invalid id number for spanboard " + sid
          elif "Max Span-Board Block" in line:
            spansboard[sid].append(int(line.split(":")[2].strip()))
            if spansboard[sid][-1] == 0:
              print "Error 0 spanboard found for ID#" + sid
    else:
      print "unknown file: " + f
  lineplot("All Data for Spanboard", "Max Spanboard", spansboard, 11, "spanboard")
  avgplot("Average of all Data for Spanboard", "Max Spanboard", spansboard, 11, "spanboard")

def analyze_ospan():
  """Analyze all data from ospan test."""
  ospans = dict()
  trueospans = dict()
  ms = dict()
  print "Reading ospan: "
  for fn in glob.glob("data/7[4-6]??"):
    if os.path.isdir(fn):
      sid = fn.split("/")[-1]
      if not os.path.isfile(fn+"/ospan1.txt"):
        print "Warning! No ospan for:" + sid
        continue
      ospans[sid] = []
      trueospans[sid] = []
      ms[sid] = []
      with open(fn+"/ospan1.txt", 'r') as f:
        tempms = []
        allms = []
        maxss = 0
        sectionbegan = False
        for line in f:
          if "Subject" in line:
            if sid != line.split(":")[2].strip():
              print "Error invalid id number for ospan " + sid
          elif "Max O-SPAN" in line:
            ospans[sid].append(int(line.split(":")[2].strip()))
            ms[sid].append(sum(allms)/float(len(allms)))
            allms = []
            trueospans[sid].append(maxss)
            maxss = 0
            if ospans[sid][-1] == 0:
              print "warning: 0 ospan found for ID#" + sid
          elif "Section 3" in line:
            sectionbegan = True
          elif "(" in line and sectionbegan:
            if "[" in line:
              if int(line.split("]")[3].split(",")[1]) != len(tempms):
                print "Error in data file ospan: " + sid
              if len(tempms) == 0:
                allms.append(100.0)
              else:
                allms.append(100*sum(tempms)/float(len(tempms)))
              if allms[-1] >=85 and "True"==line[line.index("(")+1:].split(",")[0]:
                maxss = len(tempms)
              tempms = []
            else:
              tempms.append(1 if "'True'" == (line[line.index("(")+1:].split(",")[0]) else 0)
          elif sectionbegan:
            #print "doesnt happen",line[:-1]
            tempms = []
            maxss = 0
    else:
      print "unknown file: " + f
  lineplot("Max O-SPAN", "Max O-SPAN", ospans, 11, "ospan")
  avgplot("Average Max O-SPAN", "Max O-SPAN", ospans, 11, "ospan")
  lineplot("Max O-SPAN with accurate math", "Max O-SPAN", trueospans, 11, "ospan")
  avgplot("Average Max O-SPAN with accurate math", "Max O-SPAN", trueospans, 11, "ospan")
  lineplot("Math Score", "Accuracy(%)", ms, 100, "ospan")
  avgplot("Average Math Score", "Accuracy(%)", ms, 100, "ospan")

def analyze_rcp():
  """Analyze all data from rcp test."""
  accuracies = dict()
  rcps = dict()
  caccuracies = dict()
  crcps = dict()
  for i in [1,2,3]:
    rcps[i] = dict()
    accuracies[i] = dict()
    crcps[i] = dict()
    caccuracies[i] = dict()
  print "Reading rcp: "
  for fn in glob.glob("data/7[4-6]??"):
    if os.path.isdir(fn):
      sid = fn.split("/")[-1]
      if not os.path.isfile(fn+"/rcp1.txt"):
        print "Warning! No rcp for:" + sid
        continue
      for i in [1,2,3]:
        rcps[i][sid] = []
        accuracies[i][sid] = []
        crcps[i][sid] = []
        caccuracies[i][sid] = []
      with open(fn+"/rcp1.txt", 'r') as f:
        last4rt = []
        lowload = []
        highload = []
        highrt = []
        lowrt = []
        clowload = []
        chighload = []
        chighrt = []
        clowrt = []
        section = 0
        for line in f:
          if "Subject" in line:
            if sid != line.split(":")[2].strip():
              print "Error invalid id number for sart " + sid
          elif "Section 1" in line and "Practice" not in line:
            section = 1
          elif "Section 2" in line and "Practice" not in line:
            section = 2
          elif "Section 3" in line and "Practice" not in line:
            section = 3
          elif "(" in line and section != 0:
            lines = line[line.index("(")+1:].split(";")
            if section == 3:
              if "[" not in line:
                continue
            if "True" in lines[3]:
              if lines[2].lower() in lines[1]:
                temp = clowload
                temprt = clowrt
              else:
                temp = lowload
                temprt = lowrt
            else:
              if lines[2].lower() in lines[1]:
                temp = chighload
                temprt = chighrt
              else:
                temp = highload
                temprt = highrt
            temp.append(1 if "True" in lines[0] else 0)
            temprt.append(float(lines[-1][:-2]))
          else:
            if section != 0:
              if len(lowrt) > 0:
                rcps[section][sid].append(1000*sum(lowrt)/float(len(lowrt)))
              if len(highrt) > 0:
                rcps[section][sid].append(1000*sum(highrt)/float(len(highrt)))
              if len(lowload) > 0:
                accuracies[section][sid].append(100*sum(lowload)/float(len(lowload)))
              if len(highload) > 0:
                accuracies[section][sid].append(100*sum(highload)/float(len(highload)))
              if len(clowrt) > 0:
                crcps[section][sid].append(1000*sum(clowrt)/float(len(clowrt)))
              if len(chighrt) > 0:
                crcps[section][sid].append(1000*sum(chighrt)/float(len(chighrt)))
              if len(clowload) > 0:
                caccuracies[section][sid].append(100*sum(clowload)/float(len(clowload)))
              if len(chighload) > 0:
                caccuracies[section][sid].append(100*sum(chighload)/float(len(chighload)))
              section = 0
              lowrt = []
              highrt = []
              lowload = []
              highload = []
              clowrt = []
              chighrt = []
              clowload = []
              chighload = []
    else:
      print "unknown file: " + f
  #plot
  dellist = ["7623","7601"]
  xaxes = ["","Perceptual Load","Perceptual Load","Working Memory Load"]
  for i in [1,2,3]:
    for s in dellist:
      del crcps[i][s]
      del rcps[i][s]
      del caccuracies[i][s]
      del accuracies[i][s]
    diglineplot("Compatible Visual Distractor Section "+str(i)+" RCP", ("Low","High"),xaxes[i],"Time(ms)", crcps[i], 1000, "rcp")
    digavgplot("Average Compatible Visual Distractor Section "+str(i)+" RCP", ("Low", "High"),xaxes[i], "Time(ms)", crcps[i], 1000, "rcp")
    diglineplot("Compatible Visual Distractor Section "+str(i)+" RCP", ("Low","High"),xaxes[i],"Accuracy(%)", caccuracies[i], 100, "rcp")
    digavgplot("Average Compatible Visual Distractor Section "+str(i)+" RCP", ("Low", "High"),xaxes[i], "Accuracy(%)", caccuracies[i], 100, "rcp")
    diglineplot("Incompatible Visual Distractor Section "+str(i)+" RCP", ("Low","High"),xaxes[i],"Time(ms)", rcps[i], 1000, "rcp")
    digavgplot("Average Incompatible Visual Distractor Section "+str(i)+" RCP", ("Low", "High"),xaxes[i], "Time(ms)", rcps[i], 1000, "rcp")
    diglineplot("Incompatible Visual Distractor Section "+str(i)+" RCP", ("Low","High"),xaxes[i],"Accuracy(%)", accuracies[i], 100, "rcp")
    digavgplot("Average Incompatible Visual Distractor Section "+str(i)+" RCP", ("Low", "High"),xaxes[i], "Accuracy(%)", accuracies[i], 100, "rcp")

def analyze_sart():
  """Analyze all data from sart test."""
  accuracies = dict()
  rts = dict()
  print "Reading sart: "
  for fn in glob.glob("data/7[4-6]??"):
    if os.path.isdir(fn):
      sid = fn.split("/")[-1]
      if not os.path.isfile(fn+"/sart1.txt"):
        print "Warning! No ospan for:" + sid
        continue
      accuracies[sid] = []
      rts[sid] = []
      with open(fn+"/sart1.txt", 'r') as f:
        last4rt = []
        sarts = []
        correctrt = []
        incorrectrt = []
        sectionbegan = False
        target = -1
        for line in f:
          if "Subject" in line:
            if sid != line.split(":")[2].strip():
              print "Error invalid id number for sart " + sid
          elif "Section 2" in line:
            sectionbegan = True
          elif "TARGET" in line:
            target = line.split(":")[2].strip()
          elif "(" in line and sectionbegan:
            if line.split(",")[1] == target:
              sarts.append(1 if "True"==line[line.index("(")+1:].split(",")[0] else 0)
              if sarts[-1] == 1:
                temp = correctrt
              else:
                temp = incorrectrt
              if len(last4rt) > 0:
                temp.append(sum(last4rt)/len(last4rt))
            else:
              if len(last4rt) == 4:
                last4rt = last4rt[1:]
              last4rt.append(float(line.split(",")[2][:-2]))
        rts[sid].append(1000*sum(correctrt)/len(correctrt))
        rts[sid].append(1000*sum(incorrectrt)/len(incorrectrt))
        accuracies[sid].append(100*sum(sarts)/len(sarts))
        accuracies[sid].append(min(100.0,accuracies[sid][-1]+(20*random.random())))
    else:
      print "unknown file: " + f
  diglineplot("Sart Accuracy with expected results", ("Before","Expected After"),"Cognitive Training","Accuracy(%)", accuracies, 100, "sart")
  digavgplot("Average Sart Accuracy with expected results", ("Before","Expected After"),"Cognitive Training","Accuracy(%)", accuracies, 100, "sart")
  diglineplot("Last 4 Response Times before target", ("Correct","Incorrect"),"Target Accuracy","Time(ms)", rts, 1000, "sart")
  digavgplot("Average of Last 4 Response Times before target", ("Correct", "Incorrect"),"Target Accuracy", "Time(ms)", rts, 1000, "sart")

def analyze_digitspan():
  """Analyze all data from digitspan test."""
  digitspans = dict()
  print "Reading digitspan: "
  for fn in glob.glob("data/7[4-6]??"):
    if os.path.isdir(fn):
      sid = fn.split("/")[-1]
      if not os.path.isfile(fn+"/digitspan1.txt"):
        print "Warning! No digitspan for:" + sid
        continue
      digitspans[sid] = []
      with open(fn+"/digitspan1.txt", 'r') as f:
        for line in f:
          if "Subject" in line:
            if sid != line.split(":")[2].strip():
              print "Error invalid id number for digitspan " + sid
          elif "Max Forward Digit Span BLOCK" in line:
            digitspans[sid].append(int(line.split(":")[2].strip()))
            if digitspans[sid][-1] == 0:
              print "Error 0 span found for ID#" + sid
          elif "Max Reverse Digit Span BLOCK" in line:
            digitspans[sid].append(int(line.split(":")[2].strip()))
            if digitspans[sid][-1] == 0:
              print "Error 0 digitspan found for ID#" + sid
    else:
      print "unknown file: " + f
  diglineplot("All Data for DigitSpan",("Forward","Reverse"),"Block Type", "Max Digit Span", digitspans, 11, "digitspan")
  digavgplot("Average of all Data for DigitSpan", ("Forward","Reverse"),"Block Type","Max Digit Span", digitspans, 11, "digitspan")

def lineplot(title, ylabel, data, toprange, span):
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
  for key in data.keys():
    if len(data[key]) == 3:
      ax.plot(x,data[key],marker='o',label=key)
    else:
      print "Error. Not enough data for: ID#" + key,data[key]
      plt.close()
      return
  plt.xlabel("Block Number")
  plt.ylabel(ylabel)
  plt.xticks(x)
  plt.axis([0,len(x)+1,0,0.1+toprange])
  plt.title(title)
  if not os.path.isdir("analysis1"):
    os.mkdir("analysis1")
  if not os.path.isdir("analysis1/"+span):
    os.mkdir("analysis1/"+span)
  plt.savefig("analysis1/"+span+"/"+title.replace(" ","").lower()+".png")
  plt.close()

def avgplot(title, ylabel, data, toprange, span):
  """Make a simpe average bar graph pyplot.

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
  width = 0.35
  for key in data.keys():
    if len(data[key]) != 3:
      print "Error. Not enough data for: ID#" + key,data[key]
      plt.close()
      return
  avgs = [0,0,0]
  err = [0,0,0]
  for i in range(len((x))):
    temp = [data[key][i] for key in data.keys()]
    avgs[i] = sum(temp)/float(len(temp))
    err[i] = stats.sem(temp)

  ax.bar([i-width/2 for i in x],avgs,width, yerr=err, color='y',error_kw=dict(linewidth=2,ecolor='black',capsize=5,mew=2))
  plt.xticks(x)
  plt.xlabel("Block Number")
  plt.ylabel(ylabel)
  plt.axis([0,len(x)+1,0,0.1+toprange])
  plt.title(title)
  if not os.path.isdir("analysis1"):
    os.mkdir("analysis1")
  if not os.path.isdir("analysis1/"+span):
    os.mkdir("analysis1/"+span)
  plt.savefig("analysis1/"+span+"/"+title.replace(" ","").lower()+".png")
  plt.close()

def diglineplot(title, xlabels, xlabel, ylabel, data, toprange, span):
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
  x = [1,2]
  for key in data.keys():
    if len(data[key]) == 2:
      ax.plot(x,data[key],marker='o',label=key)
    else:
      print "Error. Not enough data for: ID#" + key,data[key]
      plt.close()
      return
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.xticks(x,xlabels)
  plt.axis([0,len(x)+1,0,0.1+toprange])
  plt.title(title)
  if not os.path.isdir("analysis1"):
    os.mkdir("analysis1")
  if not os.path.isdir("analysis1/"+span):
    os.mkdir("analysis1/"+span)
  plt.savefig("analysis1/"+span+"/"+title.replace(" ","").lower()+".png")
  plt.close()

def digavgplot(title, xlabels, xlabel, ylabel, data, toprange, span):
  """Make a simpe average bar graph pyplot.

  Arguments:
  @param title - title of pyplot
  @param xlabels - x axis labels text
  @param xlabel - x axis label text
  @param ylabel - y axis label text
  @param data - data for each block for each subject
  @param toprange - highest y value
  @param span - the type of span we are graphing
  """
  fig = plt.figure()
  ax = fig.add_subplot(111)
  x = [1,2]
  width = 0.35
  for key in data.keys():
    if len(data[key]) != 2:
      print "Error. Not enough data for: ID#" + key,data[key]
      plt.close()
      return
  avgs = [0,0]
  err = [0,0]
  for i in range(len((x))):
    temp = [data[key][i] for key in data.keys()]
    avgs[i] = sum(temp)/float(len(temp))
    err[i] = stats.sem(temp)

  ax.bar([i-width/2 for i in x],avgs,width, yerr=err, color='y',error_kw=dict(linewidth=2,ecolor='black',capsize=5,mew=2))
  plt.xticks(x)
  ax.set_xticklabels(xlabels)
  plt.xlabel(xlabel)
  plt.ylabel(ylabel)
  plt.axis([0,len(x)+1,0,0.1+toprange])
  plt.title(title)
  if not os.path.isdir("analysis1"):
    os.mkdir("analysis1")
  if not os.path.isdir("analysis1/"+span):
    os.mkdir("analysis1/"+span)
  plt.savefig("analysis1/"+span+"/"+title.replace(" ","").lower()+".png")
  plt.close()

if __name__ == '__main__': main()
