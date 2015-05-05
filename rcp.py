#!/usr/bin/env python2
"""rcp.py
Response-Competition Paradigm - Below are the different sections of the task:
  1. First a fixation dot appears on the screen for FIXATION_TIME, then the 
    target letter is displayed for DISPLAY_TIME. The target letter is 
    either an x or a z, and it appears randomly in one of six positions 
    equdistant from each other in a circle, located at the center of the 
    display. The other five positions are either empty in the low perceptual 
    load of the experiment or occupied by five neutral letters, in the high 
    perceptual load of the experiment. In the beginning, this is repeated 
    NUM_PRACTICE_TRIALS times for NUM_PRACTICE_BLOCKS times. Then, this is 
    repeated NUM_TRIALS_PER_BLOCK times per block for NUM_BLOCK times.
  2. Go - NoGo Task
  3. Work Memory High Load task

Command-Line Execution: Instead of entering the subject initials through the
psychopy gui, you can provide them as command line arguments when running 
with the terminal.

Log files:
  All log files are placed in the directory data/X/rcp.txt, where X is 
  the initials of the participant. Each line of the log file describes 
  different actions occuring in the program. Here are the different possible 
  formats of each line in the log file:
    * Note: 'TIMESTAMP' indicates how many seconds have passed since the 
      initialization of the program
    * "MM/DD/YYYY HH:MM:SS" - at the beginning of the data file, indicates the 
      current date and time that the program began its execution.
    * "TIMESTAMP: SUBJECT: X" - indicates the subjects initials who this data 
      file belongs to.
    * "TIMESTAMP: Test Number: X" - indicates which iteration of the test the
      subject is on. X must be an integer >= 1.
    * "TIMESTAMP: TARGET: X" - indicates what the target number was
    * "TIMESTAMP: Section [1-2]" - indicates that section data follows until 
      the next "Section X".
    * "TIMESTAMP: ([true/false/timeout], N, reaction time)" - for each showing
      of a number, the subject will get true if it was a non-target number and 
      they pressed the key, otherwise if it is the target and they press a 
      digit, then they get false, otherwise they get a true. A timeout occurs
      when they don't respond within the MASK_TIME to a non-target digit. The
      reaction time is measured from the beginning of when the digit is 
      displayed.
    * "TIMESTAMP: Accuracy: Y" - overall accuracy including non-targets and
      targets.
    * "TIMESTAMP: END SUCCESS" - test has successfully completed
    * "TIMESTAMP: ERROR! QUIT OUT OF SYSTEM" - test has been quit by user, by
      pressing the 'q' or 'Esc' keys.
After imports, there is a list of global variables that change various aspects
of the program, modifiable to the administrators content.
"""
from psychopy import visual,core,event,gui,sound
import random,numpy,sys,os,numpy
from datetime import datetime
__author__ = "Omid Rhezaii"
__email__ = "omid@rhezaii.com"
__copyright__ = "Copyright 2015, Michael Silver Lab"
__credits__ = ["Omid Rhezaii", "Sahar Yousef", "Michael Silver"]
__version__ = "2.0"
__status__ = "Final"

# GLOBAL VARIABLE DECLARATIONS
DIGIT_RANGE = (0,9)
DIGIT_SIZES = [1.8,2.7,3.5,3.8,4.5] # display sizes in cm
FIXATION_SIZE = 0.3
FIXATION_TIME = 1.000
# Experiment Practice
NUM_PRACTICE_TRIALS = 12 #10   # per block
NUM_PRACTICE_BLOCKS = 2
# Experiment 1
NUM_TRIALS_PER_BLOCK = 72  # 72
NUM_BLOCKS = 2             # 10
DISPLAY_TIME = 0.050 # time stimuli is displayed
# Experiment 2
NUM_TRIALS_PER_BLOCK2 = 48 # 48
NUM_BLOCKS2 = 4            # 2
DISPLAY_TIME2 = 0.100 # time stimuli is displayed
TIMEOUT = 3
# Experiment 3
NUM_TRIALS_PER_BLOCK3 = 48 # 50
NUM_BLOCKS3 = 4
DISPLAY_TIME3 = 0.050 # time stimuli is displayed
NUMBER_DISPLAY_TIME = 0.500 # time numbers are displayed
MASK_TIME = 1.000
# sound settings
MAX_FAILS = 3
CORRECT_FREQ = 440
INCORRECT_FREQ = 330
TONE_LENGTH = 0.5

# Keep master time for whole program
programTime = core.Clock()
# log file location
logFile = "rcp"
dataPath = "rcp"
def main(argv):
  """Main method to be runned at beginning"""
  global logFile, programTime, dataPath

  #do only if we werent given initials from the command line
  if len(argv) == 1:
    while True:
      dlg = gui.DlgFromDict(dictionary={'Class ID':'','Test Number':'1'},title="RCP Task")
      if(dlg.OK):
        initials = dlg.data[0]
        testNo = int(dlg.data[1])
      else:
        sys.exit(1)
      if(os.path.isfile("data/"+initials+"/"+logFile+str(testNo)+".txt")):
        error = gui.Dlg(title="Existing Log File",labelButtonOK=u'Yes',labelButtonCancel=u'No')
        error.addText("A log file with initials " + initials+ " already exists. Are you sure you want to overwrite? If not, answer no and change your initials." )
        error.show()
        if error.OK:
          os.remove("data/"+initials+"/"+logFile+str(testNo)+".txt")
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
  dataPath = "data/"+initials+"/" + dataPath

  if not os.path.isdir("data"):
    os.mkdir("data")
  if not os.path.isdir("data/"+initials):
    os.mkdir("data/"+initials)
  logFile = open("data/"+initials+"/"+logFile+str(testNo)+".txt","w+")
  log(datetime.now().strftime("%d/%m/%y %H:%M"))
  log("Subject: " + initials)
  log("Test Number: " + str(testNo))
  win = visual.Window([800,600],monitor="testMonitor",units="deg",color="Black",fullscr=True)
  winsound = sound.SoundPygame(value=CORRECT_FREQ, secs=TONE_LENGTH)
  losesound = sound.SoundPygame(value=INCORRECT_FREQ, secs=TONE_LENGTH)
  fixation = visual.Circle(win,radius=FIXATION_SIZE,fillColor="LightGray")
  go_color = "DarkMagenta"
  nogo_color = "DarkOrange"
  timer = core.Clock()
  #place text in circle
  stims = []
  eccen = 4 # distance to fixation point
  for theta in numpy.linspace(0,numpy.pi*2,7)[:-1]:
      current_x = eccen * numpy.cos(theta)
      current_y = eccen * numpy.sin(theta)
      stims.append(visual.TextStim(win,text="0", pos = (current_x,current_y)))
      stims[-1].height=2

  ###SECTION 1 PRACTICE BEGIN
  log("Section 1 Practice")
  instructions = visual.TextStim(win,text="Part 1 Practice\n\nIn this task, you will see letters arranged in a circle near the center of the screen. "+
                                          "One of these letters will be either an \'x\' or a \'z\'. If there was an \'x\', press 2 with your index finger, "+
                                          "or if there was a \'z\', press 0 with your thumb. There will also be a large letter (either Z, X, or P) "+
                                          "outside of this circle that you should ignore.\n\nPress spacebar key to continue.",wrapWidth=40,color="LightGray")
  instructions.draw()
  win.flip()
  event.waitKeys(keyList=['space','q','escape'])
  visual.TextStim(win,text="This is the sound of a correct response.",color="LightGray").draw()
  win.flip()
  winsound.play()
  core.wait(2)
  visual.TextStim(win,text="This is the sound of an incorrect response.",color="LightGray").draw()
  win.flip()
  losesound.play()
  core.wait(2)
  condition_s1 = True
  #begin drawing
  for block in range(1,NUM_PRACTICE_BLOCKS+1):
    visual.TextStim(win,text="To start practice block "+str(block)+" of " + str(NUM_PRACTICE_BLOCKS)+", press the spacebar.").draw()
    win.flip()
    event.waitKeys(keyList=['space','q','escape'])
    condition_s1 = not condition_s1
    for trial in range(NUM_PRACTICE_TRIALS):
      fixation.draw()
      win.flip()
      core.wait(FIXATION_TIME)
      criticaldistractor = visual.TextStim(win,text=random.choice(["P","Z","X"]),pos=random.choice([(7,0),(-7,0),(0,-7),(0,7)]))
      criticaldistractor.height=2.5
      criticaldistractor.draw()
      letters = ['z' if random.random() < 0.5 else 'x']
      if condition_s1:
        letters += ['o']*5
      else:
        letters += ['k','s','m','v','n']
      random.shuffle(letters)
      for i,stim in enumerate(stims):
        stim.setText(letters[i])
        stim.draw()
      win.flip()
      core.wait(DISPLAY_TIME)
      win.flip()
      timer.reset()
      event.clearEvents()
      while True:
        if event.getKeys(keyList=['num_0','0','[0]']):
          if 'z' in letters:
            tempLog = "(True"
            winsound.play()
          else:
            tempLog = "(False"
            losesound.play()
          break
        elif event.getKeys(keyList=['num_2','2','[2]']):
          if 'x' in letters:
            tempLog = "(True"
            winsound.play()
          else:
            tempLog = "(False"
            losesound.play()
          break
        elif event.getKeys(keyList=['q','escape']):
          quit()
      log(tempLog+";"+str(letters)+";"+str(criticaldistractor.text)+";"+str(condition_s1)+";"+str(timer.getTime()))
  core.wait(TONE_LENGTH)
  ### SECTION 1 PRACTICE END

  ### SECTION 1 BEGIN
  log("Section 1")
  instructions = visual.TextStim(win,text="Part 1\n\nIn this task, you will see letters arranged in a circle near the center of the screen. "+
                                          "One of these letters will be either an \'x\' or a \'z\'. If there was an \'x\', press 2 with your index finger, "+
                                          "or if there was a \'z\', press 0 with your thumb. There will also be a large letter (either Z, X, or P) "+
                                          "outside of this circle that you should ignore.\n\nPress spacebar to continue.",wrapWidth=40,color="LightGray")
  instructions.draw()
  win.flip()
  event.waitKeys(keyList=['space','q','escape'])

  condition_s1 = random.random() < 0.5
  log_s1 = []
  log_s6 = []
  #begin drawing
  for block in range(1,NUM_BLOCKS+1):
    visual.TextStim(win,text="To start block "+str(block)+" of " + str(NUM_BLOCKS)+", press the spacebar.").draw()
    win.flip()
    event.waitKeys(keyList=['space','q','escape'])
    condition_s1 = not condition_s1
    for trial in range(NUM_TRIALS_PER_BLOCK):
      fixation.draw()
      win.flip()
      core.wait(FIXATION_TIME)
      criticaldistractor = visual.TextStim(win,text=random.choice(["P","Z","X"]),pos=random.choice([(7,0),(-7,0),(0,-7),(0,7)]))
      criticaldistractor.height=2.5
      criticaldistractor.draw()
      letters = ['z' if random.random() < 0.5 else 'x']
      if condition_s1:
        letters += ['o']*5
      else:
        letters += ['k','s','m','v','n']
      random.shuffle(letters)
      for i,stim in enumerate(stims):
        stim.setText(letters[i])
        stim.draw()
      win.flip()
      core.wait(DISPLAY_TIME)
      win.flip()
      timer.reset()
      event.clearEvents()
      while True:
        if event.getKeys(keyList=['num_0','0','[0]']):
          if 'z' in letters:
            tempLog = "(True, "
            winsound.play()
            (log_s1 if condition_s1 else log_s6).append(1)
          else:
            tempLog = "(False, "
            losesound.play()
            (log_s1 if condition_s1 else log_s6).append(0)
          break
        elif event.getKeys(keyList=['num_2','2','[2]']):
          if 'x' in letters:
            tempLog = "(True"
            winsound.play()
            (log_s1 if condition_s1 else log_s6).append(1)
          else:
            tempLog = "(False"
            losesound.play()
            (log_s1 if condition_s1 else log_s6).append(0)
          break
        elif event.getKeys(keyList=['q','escape']):
          quit()
      log(tempLog+";"+str(letters)+";"+str(criticaldistractor.text)+";"+str(condition_s1)+";"+str(timer.getTime()))
  core.wait(TONE_LENGTH)
  s1accuracy1= (1.0*sum(log_s1))/len(log_s1)
  s6accuracy1= (1.0*sum(log_s6))/len(log_s6)
  #feedback = visual.TextStim(win, text=("You had an accuracy of: %.0f%% for easy part\n\nYou had an accuracy of: %.0f%% for the hard part" % (s1accuracy1*100,s6accuracy1*100)) )
  #feedback.draw()
  log("S1 Accuracy: "+str(s1accuracy1))
  log("S6 Accuracy: "+str(s6accuracy1))
  #win.flip()
  #core.wait(5)
  ### SECTION 1 END

  ### SECTION 2 PRACTICE START
  log("Section 2 Practice")
  condition_s2 = random.random() < 0.5

  #begin drawing
  while True:
    log2_s1 = []
    log2_s6 = []
    for block in range(1,NUM_PRACTICE_BLOCKS+1):
      if condition_s2:
        instructions = visual.TextStim(win,text="Part 2a Practice\n\nYou will now see letters in the center of the screen, along with an orange or purple shape. "+
                                                "Like before, press 2 if you see an \'x\' or press 0 if you see a \'z\', BUT only do so if the shape is purple. "+
                                                "If the shape is orange, don't press anything at all. \n\nPress spacebar to continue.",wrapWidth=40,color="LightGray")
      else:
        instructions = visual.TextStim(win,text="Part 2b Practice\n\nYou will now see letters in the center of the screen, along with an orange or purple shape. "+
                                                "Like before, press 2 if you see an \'x\' or press 0 if you see a \'z\', BUT only do so if the shape is a purple square OR an orange circle.\n"+
                                                "If the object is a purple circle OR an orange square, don't type anything at all. "+
                                                "See below for summary:\n\nPress spacebar to continue.",pos=(0,2),wrapWidth=40,color="LightGray")
        visual.Rect(win,fillColor=go_color,pos=(-5,-5),height=1,width=1,lineWidth=0).draw()
        visual.Circle(win,fillColor=nogo_color,pos=(-4,-5),lineWidth=0).draw()
        visual.Rect(win,fillColor=nogo_color,pos=(5,-5),height=1,width=1,lineWidth=0).draw()
        visual.Circle(win,fillColor=go_color,pos=(4,-5),lineWidth=0).draw()
        visual.TextStim(win,text="Press",pos=(-5,-6)).draw()
        visual.TextStim(win,text="Do Not Press",pos=(5,-6)).draw()
      instructions.draw()
      win.flip()
      event.waitKeys(keyList=['space','q','escape'])
      #visual.TextStim(win,text="To start block "+str(block)+" of " + str(NUM_PRACTICE_BLOCKS)+", press the spacebar.").draw()
      #event.waitKeys(keyList=['space','q','escape'])
      for trial in range(NUM_PRACTICE_TRIALS):
        fixation.draw()
        win.flip()
        core.wait(FIXATION_TIME)
        criticaldistractor = visual.TextStim(win,text=random.choice(["P","Z","X"]),pos=random.choice([(7,0),(-7,0),(0,-7),(0,7)]))
        criticaldistractor.height=2
        tempLog = "(timeout,"
        pressed = False
        letter = visual.TextStim(win, text=('z' if random.random() < 0.5 else 'x'),pos=(-1,0),height=2)
        nogo = random.random() < 0.25
        if condition_s2:
          if random.random() < 0.5:
            shape = visual.Rect(win,fillColor=(nogo_color if nogo else go_color),height=2,width=2,lineWidth=0)
          else:
            shape = visual.Circle(win,fillColor=(nogo_color if nogo else go_color),radius=1,lineWidth=0)
        else:
          if nogo:
            if random.random() < 0.5:
              shape = visual.Rect(win,fillColor=nogo_color,height=2,width=2,lineWidth=0)
            else:
              shape = visual.Circle(win,fillColor=go_color,radius=1,lineWidth=0)
          else:
            if random.random() < 0.5:
              shape = visual.Rect(win,fillColor=go_color,height=2,width=2,lineWidth=0)
            else:
              shape = visual.Circle(win,fillColor=nogo_color,radius=1,lineWidth=0)
        shape.setPos((1,0))
        shape.draw()
        letter.draw()
        criticaldistractor.draw()
        win.flip()
        core.wait(DISPLAY_TIME2)
        win.flip()
        timer.reset()
        event.clearEvents()
        while timer.getTime()<TIMEOUT:
          if event.getKeys(keyList=['num_0','0','[0]']) and not pressed:
            if 'z' == letter.text:
              if not nogo:
                tempLog = "(True,go"
                winsound.play()
                (log2_s1 if condition_s2 else log2_s6).append(1)
              else:
                tempLog = "(False,nogo"
                losesound.play()
                (log2_s1 if condition_s2 else log2_s6).append(0)
            else:
              tempLog = "(False," + ("nogo" if nogo else "go")
              losesound.play()
              (log2_s1 if condition_s2 else log2_s6).append(0)
            pressed = True
            break
          elif event.getKeys(keyList=['num_2','2','[2]']) and not pressed:
            if 'x' == letter.text:
              if not nogo:
                tempLog = "(True,go"
                winsound.play()
                (log2_s1 if condition_s2 else log2_s6).append(1)
              else:
                tempLog = "(False,nogo"
                losesound.play()
                (log2_s1 if condition_s2 else log2_s6).append(0)
            else:
              tempLog = "(False,"+ ("nogo" if nogo else "go")
              losesound.play()
              (log2_s1 if condition_s2 else log2_s6).append(0)
            pressed = True
            break
          elif event.getKeys(keyList=['q','escape']):
            quit()
        if nogo and not pressed:
          tempLog = "(True," + ("nogo" if nogo else "go")
          (log2_s1 if condition_s2 else log2_s6).append(1)
          winsound.play()
        elif not pressed:
          losesound.play()
          (log2_s1 if condition_s2 else log2_s6).append(0)
        log(tempLog+";"+str(letter.text)+";"+str(criticaldistractor.text)+";"+str(condition_s2)+";"+str(timer.getTime()))
    core.wait(TONE_LENGTH)
    if len(log2_s1) > 0:
      s1accuracy2 = (1.0*sum(log2_s1))/len(log2_s1)
    else:
      s1accuracy2 = 0
    if len(log2_s6) > 0:
      s6accuracy2 = (1.0*sum(log2_s6))/len(log2_s6)
    else:
      s6accuracy2 = 0
    #feedback = visual.TextStim(win, text=("You had an accuracy of: %.0f%% for the easy part\n\nYou had an accuracy of: %.0f%% for the hard part" % (s1accuracy2*100,s6accuracy2*100)) )
    #feedback.draw()
    log("S1 Accuracy: "+str(s1accuracy2))
    log("S6 Accuracy: "+str(s6accuracy2))
    #win.flip()
    #core.wait(5)
    if s6accuracy2 < 0.65 and s1accuracy2 <0.65:
      visual.TextStim(win,text="Please read over the instructions very carefully one more time\n\nPress the spacebar to continue.").draw()
      win.flip()
      event.waitKeys(keyList=['space','q','escape'])
    else:
      break
  ###SECTION 2 PRACTICE END

  ###SECTION 2 BEGIN
  log("Section 2")
  log2_s1 = []
  log2_s6 = []

  #begin drawing
  for block in range(1,NUM_BLOCKS2+1):
    if condition_s2:
      instructions = visual.TextStim(win,text="Part 2a\n\nYou will now see letters in the center of the screen, along with an orange or purple shape. "+
                                              "Like before, press 2 if you see an \'x\' or press 0 if you see a \'z\', BUT only do so if the shape is purple. "+
                                              "If the shape is orange, don't press anything at all. \n\nPress spacebar to continue.",wrapWidth=40,color="LightGray")
    else:
      instructions = visual.TextStim(win,text="Part 2b\n\nYou will now see letters in the center of the screen, along with an orange or purple shape. "+
                                              "Like before, press 2 if you see an \'x\' or press 0 if you see a \'z\', BUT only do so if the shape is a purple square OR an orange circle.\n"+
                                              "If the object is a purple circle OR an orange square, don't type anything at all. "+
                                              "See below for summary:\n\nPress spacebar to continue.",pos=(0,2),wrapWidth=40,color="LightGray")
      visual.Rect(win,fillColor=go_color,pos=(-5,-5),height=1,width=1,lineWidth=0).draw()
      visual.Circle(win,fillColor=nogo_color,pos=(-4,-5),lineWidth=0).draw()
      visual.Rect(win,fillColor=nogo_color,pos=(5,-5),height=1,width=1,lineWidth=0).draw()
      visual.Circle(win,fillColor=go_color,pos=(4,-5),lineWidth=0).draw()
      visual.TextStim(win,text="Press",pos=(-5,-6)).draw()
      visual.TextStim(win,text="Do Not Press",pos=(5,-6)).draw()
    instructions.draw()
    win.flip()
    event.waitKeys(keyList=['space','q','escape'])
    #visual.TextStim(win,text="To start block "+str(block)+" of " + str(NUM_PRACTICE_BLOCKS)+", press the spacebar.").draw()
    #event.waitKeys(keyList=['space','q','escape'])
    for trial in range(NUM_TRIALS_PER_BLOCK2):
      fixation.draw()
      win.flip()
      core.wait(FIXATION_TIME)
      criticaldistractor = visual.TextStim(win,text=random.choice(["P","Z","X"]),pos=random.choice([(7,0),(-7,0),(0,-7),(0,7)]))
      criticaldistractor.height=2
      tempLog = "(timeout,"
      pressed = False
      letter = visual.TextStim(win, text=('z' if random.random() < 0.5 else 'x'),pos=(-1,0),height=2)
      nogo = random.random() < 0.25
      if condition_s2:
        if random.random() < 0.5:
          shape = visual.Rect(win,fillColor=(nogo_color if nogo else go_color),height=2,width=2,lineWidth=0)
        else:
          shape = visual.Circle(win,fillColor=(nogo_color if nogo else go_color),radius=1,lineWidth=0)
      else:
        if nogo:
          if random.random() < 0.5:
            shape = visual.Rect(win,fillColor=nogo_color,height=2,width=2,lineWidth=0)
          else:
            shape = visual.Circle(win,fillColor=go_color,radius=1,lineWidth=0)
        else:
          if random.random() < 0.5:
            shape = visual.Rect(win,fillColor=go_color,height=2,width=2,lineWidth=0)
          else:
            shape = visual.Circle(win,fillColor=nogo_color,radius=1,lineWidth=0)
      shape.setPos((1,0))
      shape.draw()
      letter.draw()
      criticaldistractor.draw()
      win.flip()
      core.wait(DISPLAY_TIME2)
      win.flip()
      timer.reset()
      event.clearEvents()
      while timer.getTime()<TIMEOUT:
        if event.getKeys(keyList=['num_0','0','[0]']) and not pressed:
          if 'z' == letter.text:
            if not nogo:
              tempLog = "(True,go"
              winsound.play()
              (log2_s1 if condition_s2 else log2_s6).append(1)
            else:
              tempLog = "(False,nogo"
              losesound.play()
              (log2_s1 if condition_s2 else log2_s6).append(0)
          else:
            tempLog = "(False," + ("nogo" if nogo else "go")
            losesound.play()
            (log2_s1 if condition_s2 else log2_s6).append(0)
          pressed = True
          break
        elif event.getKeys(keyList=['num_2','2','[2]']) and not pressed:
          if 'x' == letter.text:
            if not nogo:
              tempLog = "(True,go"
              winsound.play()
              (log2_s1 if condition_s2 else log2_s6).append(1)
            else:
              tempLog = "(False,nogo"
              losesound.play()
              (log2_s1 if condition_s2 else log2_s6).append(0)
          else:
            tempLog = "(False,"+ ("nogo" if nogo else "go")
            losesound.play()
            (log2_s1 if condition_s2 else log2_s6).append(0)
          pressed = True
          break
        elif event.getKeys(keyList=['q','escape']):
          quit()
      if nogo and not pressed:
        tempLog = "(True," + ("nogo" if nogo else "go")
        (log2_s1 if condition_s2 else log2_s6).append(1)
        winsound.play()
      elif not pressed:
        losesound.play()
        (log2_s1 if condition_s2 else log2_s6).append(0)
      log(tempLog+";"+str(letter.text)+";"+str(criticaldistractor.text)+";"+str(condition_s2)+";"+str(timer.getTime()))
  core.wait(TONE_LENGTH)
  if len(log2_s1) > 0:
    s1accuracy2 = (1.0*sum(log2_s1))/len(log2_s1)
  else:
    s1accuracy2 = 0
  if len(log2_s6) > 0:
    s6accuracy2 = (1.0*sum(log2_s6))/len(log2_s6)
  else:
    s6accuracy2 = 0
  #feedback = visual.TextStim(win, text=("You had an accuracy of: %.0f%% for the easy part\n\nYou had an accuracy of: %.0f%% for the hard part" % (s1accuracy2*100,s6accuracy2*100)) )
  #feedback.draw()
  log("S1 Accuracy: "+str(s1accuracy2))
  log("S6 Accuracy: "+str(s6accuracy2))
  #win.flip()
  #core.wait(5)

  #SECTION 2 PRACTICE 2 START
  log("Section 2 Practice")
  condition_s2 = not condition_s2

  #begin drawing
  while True:
    log2_s1 = []
    log2_s6 = []
    for block in range(1,NUM_PRACTICE_BLOCKS+1):
      if condition_s2:
        instructions = visual.TextStim(win,text="Part 2a Practice\n\nYou will now see letters in the center of the screen, along with an orange or purple shape. "+
                                                "Like before, press 2 if you see an \'x\' or press 0 if you see a \'z\', BUT only do so if the shape is purple. "+
                                                "If the shape is orange, don't press anything at all. \n\nPress spacebar to continue.",wrapWidth=40,color="LightGray")
      else:
        instructions = visual.TextStim(win,text="Part 2b Practice\n\nYou will now see letters in the center of the screen, along with an orange or purple shape. "+
                                                "Like before, press 2 if you see an \'x\' or press 0 if you see a \'z\', BUT only do so if the shape is a purple square OR an orange circle.\n"+
                                                "If the object is a purple circle OR an orange square, don't type anything at all. "+
                                                "See below for summary:\n\nPress spacebar to continue.",pos=(0,2),wrapWidth=40,color="LightGray")
        visual.Rect(win,fillColor=go_color,pos=(-5,-5),height=1,width=1,lineWidth=0).draw()
        visual.Circle(win,fillColor=nogo_color,pos=(-4,-5),lineWidth=0).draw()
        visual.Rect(win,fillColor=nogo_color,pos=(5,-5),height=1,width=1,lineWidth=0).draw()
        visual.Circle(win,fillColor=go_color,pos=(4,-5),lineWidth=0).draw()
        visual.TextStim(win,text="Press",pos=(-5,-6)).draw()
        visual.TextStim(win,text="Do Not Press",pos=(5,-6)).draw()
      instructions.draw()
      win.flip()
      event.waitKeys(keyList=['space','q','escape'])
      #visual.TextStim(win,text="To start block "+str(block)+" of " + str(NUM_PRACTICE_BLOCKS)+", press the spacebar.").draw()
      #event.waitKeys(keyList=['space','q','escape'])
      for trial in range(NUM_PRACTICE_TRIALS):
        fixation.draw()
        win.flip()
        core.wait(FIXATION_TIME)
        criticaldistractor = visual.TextStim(win,text=random.choice(["P","Z","X"]),pos=random.choice([(7,0),(-7,0),(0,-7),(0,7)]))
        criticaldistractor.height=2
        tempLog = "(timeout,"
        pressed = False
        letter = visual.TextStim(win, text=('z' if random.random() < 0.5 else 'x'),pos=(-1,0),height=2)
        nogo = random.random() < 0.25
        if condition_s2:
          if random.random() < 0.5:
            shape = visual.Rect(win,fillColor=(nogo_color if nogo else go_color),height=2,width=2,lineWidth=0)
          else:
            shape = visual.Circle(win,fillColor=(nogo_color if nogo else go_color),radius=1,lineWidth=0)
        else:
          if nogo:
            if random.random() < 0.5:
              shape = visual.Rect(win,fillColor=nogo_color,height=2,width=2,lineWidth=0)
            else:
              shape = visual.Circle(win,fillColor=go_color,radius=1,lineWidth=0)
          else:
            if random.random() < 0.5:
              shape = visual.Rect(win,fillColor=go_color,height=2,width=2,lineWidth=0)
            else:
              shape = visual.Circle(win,fillColor=nogo_color,radius=1,lineWidth=0)
        shape.setPos((1,0))
        shape.draw()
        letter.draw()
        criticaldistractor.draw()
        win.flip()
        core.wait(DISPLAY_TIME2)
        win.flip()
        timer.reset()
        event.clearEvents()
        while timer.getTime()<TIMEOUT:
          if event.getKeys(keyList=['num_0','0','[0]']) and not pressed:
            if 'z' == letter.text:
              if not nogo:
                tempLog = "(True,go"
                winsound.play()
                (log2_s1 if condition_s2 else log2_s6).append(1)
              else:
                tempLog = "(False,nogo"
                losesound.play()
                (log2_s1 if condition_s2 else log2_s6).append(0)
            else:
              tempLog = "(False," + ("nogo" if nogo else "go")
              losesound.play()
              (log2_s1 if condition_s2 else log2_s6).append(0)
            pressed = True
            break
          elif event.getKeys(keyList=['num_2','2','[2]']) and not pressed:
            if 'x' == letter.text:
              if not nogo:
                tempLog = "(True,go"
                winsound.play()
                (log2_s1 if condition_s2 else log2_s6).append(1)
              else:
                tempLog = "(False,nogo"
                losesound.play()
                (log2_s1 if condition_s2 else log2_s6).append(0)
            else:
              tempLog = "(False,"+ ("nogo" if nogo else "go")
              losesound.play()
              (log2_s1 if condition_s2 else log2_s6).append(0)
            pressed = True
            break
          elif event.getKeys(keyList=['q','escape']):
            quit()
        if nogo and not pressed:
          tempLog = "(True," + ("nogo" if nogo else "go")
          (log2_s1 if condition_s2 else log2_s6).append(1)
          winsound.play()
        elif not pressed:
          losesound.play()
          (log2_s1 if condition_s2 else log2_s6).append(0)
        log(tempLog+";"+str(letter.text)+";"+str(criticaldistractor.text)+";"+str(condition_s2)+";"+str(timer.getTime()))
    core.wait(TONE_LENGTH)
    if len(log2_s1) > 0:
      s1accuracy2 = (1.0*sum(log2_s1))/len(log2_s1)
    else:
      s1accuracy2 = 0
    if len(log2_s6) > 0:
      s6accuracy2 = (1.0*sum(log2_s6))/len(log2_s6)
    else:
      s6accuracy2 = 0
    #feedback = visual.TextStim(win, text=("You had an accuracy of: %.0f%% for the easy part\n\nYou had an accuracy of: %.0f%% for the hard part" % (s1accuracy2*100,s6accuracy2*100)) )
    #feedback.draw()
    log("S1 Accuracy: "+str(s1accuracy2))
    log("S6 Accuracy: "+str(s6accuracy2))
    #win.flip()
    #core.wait(5)
    if s6accuracy2 < 0.65 and s1accuracy2 <0.65:
      visual.TextStim(win,text="Please read over the instructions very carefully one more time\n\nPress the spacebar to continue.").draw()
      win.flip()
      event.waitKeys(keyList=['space','q','escape'])
    else:
      break
  ###SECTION 2 PRACTICE END

  ###SECTION 2 BEGIN
  log("Section 2")
  log2_s1 = []
  log2_s6 = []

  #begin drawing
  for block in range(1,NUM_BLOCKS2+1):
    if condition_s2:
      instructions = visual.TextStim(win,text="Part 2a\n\nYou will now see letters in the center of the screen, along with an orange or purple shape. "+
                                              "Like before, press 2 if you see an \'x\' or press 0 if you see a \'z\', BUT only do so if the shape is purple. "+
                                              "If the shape is orange, don't press anything at all. \n\nPress spacebar to continue.",wrapWidth=40,color="LightGray")
    else:
      instructions = visual.TextStim(win,text="Part 2b\n\nYou will now see letters in the center of the screen, along with an orange or purple shape. "+
                                              "Like before, press 2 if you see an \'x\' or press 0 if you see a \'z\', BUT only do so if the shape is a purple square OR an orange circle.\n"+
                                              "If the object is a purple circle OR an orange square, don't type anything at all. "+
                                              "See below for summary:\n\nPress spacebar to continue.",pos=(0,2),wrapWidth=40,color="LightGray")
      visual.Rect(win,fillColor=go_color,pos=(-5,-5),height=1,width=1,lineWidth=0).draw()
      visual.Circle(win,fillColor=nogo_color,pos=(-4,-5),lineWidth=0).draw()
      visual.Rect(win,fillColor=nogo_color,pos=(5,-5),height=1,width=1,lineWidth=0).draw()
      visual.Circle(win,fillColor=go_color,pos=(4,-5),lineWidth=0).draw()
      visual.TextStim(win,text="Press",pos=(-5,-6)).draw()
      visual.TextStim(win,text="Do Not Press",pos=(5,-6)).draw()
    instructions.draw()
    win.flip()
    event.waitKeys(keyList=['space','q','escape'])
    #visual.TextStim(win,text="To start block "+str(block)+" of " + str(NUM_PRACTICE_BLOCKS)+", press the spacebar.").draw()
    #event.waitKeys(keyList=['space','q','escape'])
    for trial in range(NUM_TRIALS_PER_BLOCK2):
      fixation.draw()
      win.flip()
      core.wait(FIXATION_TIME)
      criticaldistractor = visual.TextStim(win,text=random.choice(["P","Z","X"]),pos=random.choice([(7,0),(-7,0),(0,-7),(0,7)]))
      criticaldistractor.height=2
      tempLog = "(timeout,"
      pressed = False
      letter = visual.TextStim(win, text=('z' if random.random() < 0.5 else 'x'),pos=(-1,0),height=2)
      nogo = random.random() < 0.25
      if condition_s2:
        if random.random() < 0.5:
          shape = visual.Rect(win,fillColor=(nogo_color if nogo else go_color),height=2,width=2,lineWidth=0)
        else:
          shape = visual.Circle(win,fillColor=(nogo_color if nogo else go_color),radius=1,lineWidth=0)
      else:
        if nogo:
          if random.random() < 0.5:
            shape = visual.Rect(win,fillColor=nogo_color,height=2,width=2,lineWidth=0)
          else:
            shape = visual.Circle(win,fillColor=go_color,radius=1,lineWidth=0)
        else:
          if random.random() < 0.5:
            shape = visual.Rect(win,fillColor=go_color,height=2,width=2,lineWidth=0)
          else:
            shape = visual.Circle(win,fillColor=nogo_color,radius=1,lineWidth=0)
      shape.setPos((1,0))
      shape.draw()
      letter.draw()
      criticaldistractor.draw()
      win.flip()
      core.wait(DISPLAY_TIME2)
      win.flip()
      timer.reset()
      event.clearEvents()
      while timer.getTime()<TIMEOUT:
        if event.getKeys(keyList=['num_0','0','[0]']) and not pressed:
          if 'z' == letter.text:
            if not nogo:
              tempLog = "(True,go"
              winsound.play()
              (log2_s1 if condition_s2 else log2_s6).append(1)
            else:
              tempLog = "(False,nogo"
              losesound.play()
              (log2_s1 if condition_s2 else log2_s6).append(0)
          else:
            tempLog = "(False," + ("nogo" if nogo else "go")
            losesound.play()
            (log2_s1 if condition_s2 else log2_s6).append(0)
          pressed = True
          break
        elif event.getKeys(keyList=['num_2','2','[2]']) and not pressed:
          if 'x' == letter.text:
            if not nogo:
              tempLog = "(True,go"
              winsound.play()
              (log2_s1 if condition_s2 else log2_s6).append(1)
            else:
              tempLog = "(False,nogo"
              losesound.play()
              (log2_s1 if condition_s2 else log2_s6).append(0)
          else:
            tempLog = "(False,"+ ("nogo" if nogo else "go")
            losesound.play()
            (log2_s1 if condition_s2 else log2_s6).append(0)
          pressed = True
          break
        elif event.getKeys(keyList=['q','escape']):
          quit()
      if nogo and not pressed:
        tempLog = "(True," + ("nogo" if nogo else "go")
        (log2_s1 if condition_s2 else log2_s6).append(1)
        winsound.play()
      elif not pressed:
        losesound.play()
        (log2_s1 if condition_s2 else log2_s6).append(0)
      log(tempLog+";"+str(letter.text)+";"+str(criticaldistractor.text)+";"+str(condition_s2)+";"+str(timer.getTime()))
  core.wait(TONE_LENGTH)
  if len(log2_s1) > 0:
    s1accuracy2 = (1.0*sum(log2_s1))/len(log2_s1)
  else:
    s1accuracy2 = 0
  if len(log2_s6) > 0:
    s6accuracy2 = (1.0*sum(log2_s6))/len(log2_s6)
  else:
    s6accuracy2 = 0
  #feedback = visual.TextStim(win, text=("You had an accuracy of: %.0f%% for the easy part\n\nYou had an accuracy of: %.0f%% for the hard part" % (s1accuracy2*100,s6accuracy2*100)) )
  #feedback.draw()
  log("S1 Accuracy: "+str(s1accuracy2))
  log("S6 Accuracy: "+str(s6accuracy2))
  #win.flip()
  #core.wait(5)
  ### SECTION 2 END


  ###SECTION 3 PRACTICE START
  log("Section 3 Practice")
  condition_s3 = random.random() < 0.5
  condition_s1 = True

  #begin drawing
  while True:
    log3_s1 = []
    log3_s6 = []
    instructions = visual.TextStim(win,text="Last Part Practice\n\nThis time you will be doing 2 memory related tasks. \n"+
                                            "1. First, you will see some numbers.\n2. Then, you will see letters arranged in a circle near the center of the screen. "+
                                            "Similar to before, if you see an \'x\' you press 2, or if you see a \'z\' press 0. \n"+
                                            "3. Afterwards, a number will be presented on screen. "+
                                            "If you saw this number in the original set (before the letters), press 2. Otherwise, press 0. "+
                                            "\n\nPress spacebar to continue.",wrapWidth=40,color="LightGray")
    instructions.draw()
    win.flip()
    event.waitKeys(keyList=['space','q','escape'])
    for block in range(1,NUM_PRACTICE_BLOCKS+1):
      visual.TextStim(win,text="To start block "+str(block)+" of " + str(NUM_BLOCKS3)+", press the spacebar.").draw()
      win.flip()
      event.waitKeys(keyList=['space','q','escape'])
      for trial in range(NUM_PRACTICE_TRIALS):
        criticaldistractor = visual.TextStim(win,text=random.choice(["P","Z","X"]),pos=random.choice([(7,0),(-7,0),(0,-7),(0,7)]))
        criticaldistractor.height=2.5
        letter = visual.TextStim(win, text=('z' if random.random() < 0.5 else 'x'),pos=(-0.5,0),height=2)
        numbers = []
        if condition_s3:
          numbers.append(random.choice(range(10)))
        else:
          for i in range(6):
            a = range(10)
            random.shuffle(a)
            numbers = a[:6]
        #display number
        number = visual.TextStim(win,text=''.join([str(n) for n in numbers]),height=2)
        number.draw()
        win.flip()
        core.wait(NUMBER_DISPLAY_TIME)
        #display mask
        number.text = '.........'
        number.draw()
        win.flip()
        core.wait(MASK_TIME)
        #display letter
        fixation.draw()
        win.flip()
        core.wait(FIXATION_TIME)
        criticaldistractor = visual.TextStim(win,text=random.choice(["P","Z","X"]),pos=random.choice([(7,0),(-7,0),(0,-7),(0,7)]))
        criticaldistractor.height=2.5
        criticaldistractor.draw()
        letters = ['z' if random.random() < 0.5 else 'x']
        if condition_s1:
          letters += ['o']*5
        else:
          letters += ['k','s','m','v','n']
        random.shuffle(letters)
        for i,stim in enumerate(stims):
          stim.setText(letters[i])
          stim.draw()
        win.flip()
        core.wait(DISPLAY_TIME)
        win.flip()
        timer.reset()
        event.clearEvents()
        while True:
          if event.getKeys(keyList=['num_0','0','[0]']):
            if 'z' in letters:
              tempLog = "(True, "
              winsound.play()
              (log3_s1 if condition_s1 else log3_s6).append(1)
            else:
              tempLog = "(False, "
              losesound.play()
              (log3_s1 if condition_s1 else log3_s6).append(0)
            break
          elif event.getKeys(keyList=['num_2','2','[2]']):
            if 'x' in letters:
              tempLog = "(True"
              winsound.play()
              (log3_s1 if condition_s1 else log3_s6).append(1)
            else:
              tempLog = "(False"
              losesound.play()
              (log3_s1 if condition_s1 else log3_s6).append(0)
            break
          elif event.getKeys(keyList=['q','escape']):
            quit()
        log(tempLog+";"+str(letters)+";"+str(criticaldistractor.text)+";"+str(condition_s3)+";"+str(numbers)+";"+str(timer.getTime()))
        #number probe working memory
        core.wait(TONE_LENGTH)
        ans_true = random.random() < 0.5
        if ans_true:
          letter.text = random.choice(numbers)
        else:
          if condition_s3:
            temp = range(10)
            temp.remove(numbers[0])
            letter.text = random.choice(temp)
          else:
            letter.text = random.choice(a[6:])
        letter.draw()
        win.flip()
        timer.reset()
        event.clearEvents()
        while True:
          if event.getKeys(keyList=['num_0','0','[0]']):
            if ans_true:
              tempLog = "(False"
              losesound.play()
              (log3_s1 if condition_s3 else log3_s6).append(0)
            else:
              tempLog = "(True"
              winsound.play()
              (log3_s1 if condition_s3 else log3_s6).append(1)
            break
          elif event.getKeys(keyList=['num_2','2','[2]']):
            if not ans_true:
              tempLog = "(False"
              losesound.play()
              (log3_s1 if condition_s3 else log3_s6).append(0)
            else:
              tempLog = "(True"
              winsound.play()
              (log3_s1 if condition_s3 else log3_s6).append(1)
            break
          elif event.getKeys(keyList=['q','escape']):
            quit()
        log(tempLog+";"+str(letter.text)+";"+str(ans_true)+";"+str(timer.getTime()))
        core.wait(TONE_LENGTH)
      condition_s3 = not condition_s3
    s1accuracy3 = (1.0*sum(log3_s1))/len(log3_s1)
    s6accuracy3 = (1.0*sum(log3_s6))/len(log3_s6)
    #feedback = visual.TextStim(win, text=("You had an accuracy of: %.0f%% for the easy part\n\nYou had an accuracy of: %.0f%% for the hard part" % (s1accuracy3*100,s6accuracy3*100)) )
    #feedback.draw()
    log("S1 Accuracy: "+str(s1accuracy3))
    log("S6 Accuracy: "+str(s6accuracy3))
    #win.flip()
    #core.wait(5)
    if s6accuracy3 < 0.65 and s1accuracy3 <0.65:
      visual.TextStim(win,text="Please read over the instructions very carefully one more time\n\nPress the spacebar to continue.").draw()
      win.flip()
      event.waitKeys(keyList=['space','q','escape'])
    else:
      break
  ###SECTION 3 PRACTICE END

  ###SECTION 3 BEGIN
  log("Section 3")
  instructions = visual.TextStim(win,text="Last Part \n\nThis time you will be doing 2 memory related tasks. \n"+
                                          "1. First, you will see some numbers.\n2. Then, you will see letters arranged in a circle near the center of the screen. "+
                                          "Similar to before, if you see an \'x\' you press 2, or if you see a \'z\' press 0. \n"+
                                          "3. Afterwards, a number will be presented on screen. "+
                                          "If you saw this number in the original set (before the letters), press 2. Otherwise, press 0. "+
                                          "\n\nPress spacebar to continue.",wrapWidth=40,color="LightGray")
  instructions.draw()
  win.flip()
  event.waitKeys(keyList=['space','q','escape'])
  condition_s3 = random.random() < 0.5
  log3_s1 = []
  log3_s6 = []

  #begin drawing
  for block in range(1,NUM_BLOCKS3+1):
    visual.TextStim(win,text="To start block "+str(block)+" of " + str(NUM_BLOCKS3)+", press the spacebar.").draw()
    win.flip()
    event.waitKeys(keyList=['space','q','escape'])
    for trial in range(NUM_TRIALS_PER_BLOCK3):
      criticaldistractor = visual.TextStim(win,text=random.choice(["P","Z","X"]),pos=random.choice([(7,0),(-7,0),(0,-7),(0,7)]))
      criticaldistractor.height=2.5
      letter = visual.TextStim(win, text=('z' if random.random() < 0.5 else 'x'),pos=(-0.5,0),height=2)
      numbers = []
      if condition_s3:
        numbers.append(random.choice(range(10)))
      else:
        for i in range(6):
          a = range(10)
          random.shuffle(a)
          numbers = a[:6]
      #display number
      number = visual.TextStim(win,text=''.join([str(n) for n in numbers]),height=2)
      number.draw()
      win.flip()
      core.wait(NUMBER_DISPLAY_TIME)
      #display mask
      number.text = '.........'
      number.draw()
      win.flip()
      core.wait(MASK_TIME)
      #display letter
      fixation.draw()
      win.flip()
      core.wait(FIXATION_TIME)
      criticaldistractor = visual.TextStim(win,text=random.choice(["P","Z","X"]),pos=random.choice([(7,0),(-7,0),(0,-7),(0,7)]))
      criticaldistractor.height=2.5
      criticaldistractor.draw()
      letters = ['z' if random.random() < 0.5 else 'x']
      if condition_s1:
        letters += ['o']*5
      else:
        letters += ['k','s','m','v','n']
      random.shuffle(letters)
      for i,stim in enumerate(stims):
        stim.setText(letters[i])
        stim.draw()
      win.flip()
      core.wait(DISPLAY_TIME)
      win.flip()
      timer.reset()
      event.clearEvents()
      while True:
        if event.getKeys(keyList=['num_0','0','[0]']):
          if 'z' in letters:
            tempLog = "(True, "
            winsound.play()
            (log3_s1 if condition_s1 else log3_s6).append(1)
          else:
            tempLog = "(False, "
            losesound.play()
            (log3_s1 if condition_s1 else log3_s6).append(0)
          break
        elif event.getKeys(keyList=['num_2','2','[2]']):
          if 'x' in letters:
            tempLog = "(True"
            winsound.play()
            (log3_s1 if condition_s1 else log3_s6).append(1)
          else:
            tempLog = "(False"
            losesound.play()
            (log3_s1 if condition_s1 else log3_s6).append(0)
          break
        elif event.getKeys(keyList=['q','escape']):
          quit()
      log(tempLog+";"+str(letters)+";"+str(criticaldistractor.text)+";"+str(condition_s3)+";"+str(numbers)+";"+str(timer.getTime()))
      #number probe working memory
      core.wait(TONE_LENGTH)
      ans_true = random.random() < 0.5
      if ans_true:
        letter.text = random.choice(numbers)
      else:
        if condition_s3:
          temp = range(10)
          temp.remove(numbers[0])
          letter.text = random.choice(temp)
        else:
          letter.text = random.choice(a[6:])
      letter.draw()
      win.flip()
      timer.reset()
      event.clearEvents()
      while True:
        if event.getKeys(keyList=['num_0','0','[0]']):
          if ans_true:
            tempLog = "(False"
            losesound.play()
            (log3_s1 if condition_s3 else log3_s6).append(0)
          else:
            tempLog = "(True"
            winsound.play()
            (log3_s1 if condition_s3 else log3_s6).append(1)
          break
        elif event.getKeys(keyList=['num_2','2','[2]']):
          if not ans_true:
            tempLog = "(False"
            losesound.play()
            (log3_s1 if condition_s3 else log3_s6).append(0)
          else:
            tempLog = "(True"
            winsound.play()
            (log3_s1 if condition_s3 else log3_s6).append(1)
          break
        elif event.getKeys(keyList=['q','escape']):
          quit()
      log(tempLog+";"+str(letter.text)+";"+str(ans_true)+";"+str(timer.getTime()))
      core.wait(TONE_LENGTH)
    condition_s3 = not condition_s3
  s1accuracy3 = (1.0*sum(log3_s1))/len(log3_s1)
  s6accuracy3 = (1.0*sum(log3_s6))/len(log3_s6)
  #feedback = visual.TextStim(win, text=("You had an accuracy of: %.0f%% for the easy part\n\nYou had an accuracy of: %.0f%% for the hard part" % (s1accuracy3*100,s6accuracy3*100)) )
  #feedback.draw()
  log("S1 Accuracy: "+str(s1accuracy3))
  log("S6 Accuracy: "+str(s6accuracy3))
  #win.flip()
  #core.wait(5)
  ### SECTION 3 END

  # write results to a xls file with all other subjects
  try:
    import xlrd,xlwt,xlutils.copy
    excelfile = "data/rcp.xls"
    if not os.path.isfile(excelfile):
      w = xlwt.Workbook()
      ws = w.add_sheet("Data")
      style = xlwt.easyxf("font: bold on")
      ws.write(0,0,"Initials",style)
      ws.write(0,1,"Day",style)
      ws.write(0,2,"E1S1 Accuracy",style)
      ws.write(0,3,"E1S6 Accuracy",style)
      ws.write(0,4,"E2S1 Accuracy",style)
      ws.write(0,5,"E2S6 Accuracy",style)
      ws.write(0,6,"E3S1 Accuracy",style)
      ws.write(0,7,"E3S6 Accuracy",style)
      w.save(excelfile)
    oldfile = xlrd.open_workbook(excelfile,formatting_info=True)
    row = oldfile.sheet_by_index(0).nrows
    newfile = xlutils.copy.copy(oldfile)
    sheet = newfile.get_sheet(0)
    sheet.write(row,0,initials)
    sheet.write(row,1,testNo)
    sheet.write(row,2,s1accuracy1)
    sheet.write(row,3,s6accuracy1)
    sheet.write(row,4,s1accuracy2)
    sheet.write(row,5,s6accuracy2)
    sheet.write(row,6,s1accuracy3)
    sheet.write(row,7,s6accuracy3)
    newfile.save(excelfile)
  except ImportError:
    print "ERROR: NO XLRD,XLWT, or XLUTILS installed."

  log("END SUCCESS")
  logFile.close()
  core.quit()
  # end of main

def log(line):
  """Write line to logFile.

  Arguments:
  @param line: string to write to logFile
  """
  global logFile,programTime
  logFile.write(str(programTime.getTime())+": "+line+"\n")

def quit():
  """Quit the program, logging an error and then exiting."""
  log(": ERROR! QUIT OUT OF SYSTEM")
  logFile.close()
  core.quit()

if __name__ == "__main__": main(sys.argv)
