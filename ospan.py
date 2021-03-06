#!/usr/bin/env python2
"""ospan.py:
A simple O-SPAN psychological test using the PsychoPy python module. The test 
is comprised of three phases:
  1. Simple Letter presentation and recall: This is practice for Phase 3 of the
     test, the subject is presented with NUM_PRACTICE_TRIAL_LETTERS letters, 
     one at a time, and at the end they are asked to recall the letters in the 
     order they were presented. Users are then presented with feedback on their
     performance. This is repeated NUM_PRACTICE_TRIALS times.
  2. Math Questions Diagnostic test: The subject is presented with 
     NUM_MATH_PROBLEMS simple math problems, and the time it takes for the 
     user to calculate each in their head before they continue is measured. The
     user then is presented with a possible solution and they must say True or 
     False to whether the answer presented is the correct answer or not. 
     MATH_QUESTION_CHANCE_CORRECT is the probability that a math question will 
     end up presenting the correct answer. The times it takes a subject to 
     solve a math problem are used to calculate mathTime, a time limit used 
     on math problems in Phase 3 of the test. mathTime is equivalent to the 
     subject's average performance plus 2.5 standard deviations.
  3. O-SPAN Task: The subject is presented with a letter followed by a math 
     question, repeated by however many letters are in the particular trial. 
     After all the letters have been displayed, the user is asked to recall the
     letters in the order they appeared. This is repeated NUM_TRIAL_BLOCKS 
     times for each of the set sizes in SET_SIZES. If a user takes more than 
     mathTime time to observe a math problem, it is counted as incorrect, and 
     if a trial is incorrect, the next trial will have a set size one less and
     and if it is correct, the trial will move to the next set size. When 
     MAX_FAILS mistakes are made in one set size, the test ends.

Correctness is measured for each trial as follows: 
  'XY' pairs where X is 'T' if the position of  sequence at that position is 
  correct and 'F' if it is not, and Y is 'T' if the sequence at that position 
  has identity correctness or 'F' if not. Identity correctness is when the 
  letter entered was somewhere else in the set, not nocessarily in the position
  stated. Note - 'TF' is impossible to have.

Command-Line Execution: Instead of entering the subject initlas through the
psychopy gui, you can provide them as command line arguments when running 
with the terminal.

Log files:
  All log files are placed in the directory data/X/ospan.txt, where X is the
  initials of the participant. Each line of the log file describes different
  actions occuring in the program. Here are the different possible formats of 
  each line in the log file:
    * Note: 'TIMESTAMP' indicates how many seconds have passed since the 
      initialization of the program
    * "MM/DD/YYYY HH:MM:SS" - at the beginning of the data file, indicates the 
      current date and time that the program began its execution.
    * "TIMESTAMP: SUBJECT: X" - indicates the subjects initials who this data 
      file belongs to.
    * "TIMESTAMP: Test Number: X" - indicates which iteration of the test the
      subject is on. X must be an integer >= 1.
    * "TIMESTAMP: Section [1-3]" - indicates that section data follows until 
      the next "Section X".
    * "TIMESTAMP: ([true/(speed/accuracy error)],%f)" - indicates that a math 
      problem has been completed correctly if true, or incorrectly if false, 
      in float %f time. 
    * "TIMESTAMP: ([true/false],[correct response],[subject response],
      [accuracy],N,%f)" - indicates that a sequence of N letters have been 
      completed in %f time, incorrectly if false, and correctly if true.
    * "TIMESTAMP: Max O-SPAN BLOCK X: Y" - maximum O-Span for block X is Y 
      letters.
    * "TIMESTAMP: END SUCCESS" - test has successfully completed
    * "TIMESTAMP: ERROR! QUIT OUT OF SYSTEM" - test has been quit by user, by
      pressing the 'q' or 'Esc' keys.
After imports, there is a list of global variables that change various aspects
of the program, modifiable to the administrators content.
"""
from psychopy import visual,core,event,gui,sound
import random,numpy,sys,os
from datetime import datetime
__author__ = "Omid Rhezaii"
__email__ = "omid@rhezaii.com"
__copyright__ = "Copyright 2015, Michael Silver Lab"
__credits__ = ["Omid Rhezaii", "Sahar Yousef", "Michael Silver"]
__version__ = "3.0"
__status__ = "Final"

# GLOBAL VARIABLE DECLARATIONS
LETTERS=("F", "H", "J", "K", "L", "N", "P", "Q", "R", "S", "T", "Y")
IN_BETWEEN_TRIALS_TIME = 0.5
MATH_QUESTION_CHANCE_CORRECT = 0.5
FEEDBACK_LENGTH = 3.000
# letter display options
LETTER_DISPLAY_TIME = 0.800
LETTER_SIZE = 12       # for display size
# practice trial(section 1) options
NUM_PRACTICE_TRIALS = 1
NUM_PRACTICE_TRIAL_LETTERS = 3
IN_BETWEEN_LETTERS_TIME = 0.200
# math callibrator(section 2) options
CORRECT_FREQ = 440
INCORRECT_FREQ = 330
TONE_LENGTH = 0.5
NUM_MATH_PROBLEMS = 15
LOWEST_NUMBER = 1
HIGHEST_NUMBER = 9
# section 3 options
SET_SIZES = (3,11) # from base number up to but not including top number
NUM_TRIAL_BLOCKS = 3   # number of trials for each set size.
MAX_FAILS = 3 # maximum number of fails before quitting

#Keep master time for whole program
programTime = core.Clock()
#log file location
logFile = "ospan"
dataPath = "ospan"
lastMathProblem = [0,0,0] # so we don't have the same math problem in a row
def main(argv):
  """Main method to be runned at beginning"""
  # beginning checks
  global logFile, programTime, dataPath
  if(len(LETTERS)!=12):
    print("This program is only configured to work with 12 letters.")
    return;

  #do only if we werent given initials from the command line
  if len(argv) == 1:
    while True:
      dlg = gui.DlgFromDict(dictionary={'Class ID':'','Test Number':'1'},title="O-SPAN Task")
      if(dlg.OK):
        initials = dlg.data[0].upper()
        testNo = dlg.data[1]
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
    print "Too many/few command line arguments. Please read documentation."
    sys.exit(1)
  initials = initials.upper()
  dataPath = "data/"+initials+"/" + dataPath

  #if there is no folder data, make one
  if not os.path.isdir("data"):
    os.mkdir("data")
  #if subject has no folder in data yet, make one
  if not os.path.isdir("data/"+initials):
    os.mkdir("data/"+initials)
  logFile = open("data/"+initials+"/"+logFile+str(testNo)+".txt","w+")
  log(datetime.now().strftime("%d/%m/%y %H:%M"))
  log("Subject: " + initials)
  log("Test Number: " + str(testNo))
  #make our monitor
  win = visual.Window([800,600],monitor="testMonitor",units="deg",fullscr=True)
  mouse = event.Mouse(win=win)
  winsound = sound.Sound(value=CORRECT_FREQ, secs=TONE_LENGTH)
  losesound = sound.Sound(value=INCORRECT_FREQ, secs=TONE_LENGTH)

  ### SECTION 1 BEGIN
  log("Section 1")
  instructions = visual.TextStim(win,text="Practice\n\nOn the screen, you will see a series of letters. You'll then be asked to reproduce the series at the end of the trial. "+
                                          "Do not say the letters out loud. \n\nClick to Continue")
  instructions.draw()
  win.flip()
  # wait until mouse is pressed
  while 1 not in mouse.getPressed():
    pass
  while 1 in mouse.getPressed():
    pass
  visual.TextStim(win,text="This is the sound of a correct response.").draw()
  win.flip()
  winsound.play()
  core.wait(2)
  visual.TextStim(win,text="This is the sound of an incorrect response.").draw()
  win.flip()
  losesound.play()
  core.wait(2)
  # begin practice trial
  for j in range(NUM_PRACTICE_TRIALS):
    x = [i for i in range(len(LETTERS))]
    random.shuffle(x)
    for i in x[:NUM_PRACTICE_TRIAL_LETTERS]:
      displayLetter(win,LETTERS[i])
      win.flip()
      core.wait(IN_BETWEEN_LETTERS_TIME)
    temp = validateSequence(win,mouse)
    win.flip()
    correctSeq = [LETTERS[i] for i in x[:NUM_PRACTICE_TRIAL_LETTERS]]
    if(temp[0]==correctSeq):
      colo = "Green"
      tempLog = "(True,"
    else:
      colo = "Orange"
      tempLog = "(False,"
    visual.TextStim(win,text="You recalled {0} letters correctly out of {1}".format(correctness(temp[0],correctSeq).count("TT"),NUM_PRACTICE_TRIAL_LETTERS),color=colo).draw()
    win.flip()
    core.wait(FEEDBACK_LENGTH)
    log(tempLog+str(correctSeq)+","+str(temp[0])+","+str(correctness(temp[0],correctSeq))+","+str(NUM_PRACTICE_TRIAL_LETTERS)+","+str(temp[1])+")")
  ### SECTION 1 END

  ### SECTION 2 BEGIN
  log("Section 2")
  instructions = visual.TextStim(win, text="You will now perform some simple math problems. The math problem will be something like:\n(10*2) + 2 = ? "+
                                           "When you click, you'll see an answer (for example: 22) and you should then decide whether the given answer is correct or incorrect. "+
                                           "Go at a steady and quick pace but try not to get more than 15% wrong.\n\n Click to continue.", wrapWidth=30)
  while True:
    instructions.draw()
    win.flip()
    while 1 not in mouse.getPressed():
      pass
    while 1 in mouse.getPressed():
      pass
    mathTrials = []
    for i in range(NUM_MATH_PROBLEMS):
      temp = mathQuestion(win,mouse,99)
      log(str(temp))
      mathTrials.append(temp)
      core.wait(IN_BETWEEN_TRIALS_TIME)
    mathTimes = [mathTrials[i][1] for i in range(len(mathTrials))]
    mathTime = sum(mathTimes)/len(mathTimes) + 2.5*numpy.std(mathTimes)
    mathPercentRight = (100.0 * sum([1 if mathTrials[i][0]=="True" else 0 for i in range(len(mathTrials))]))/len(mathTrials)
    if(mathPercentRight >= 85):
      break
    instructions = visual.TextStim(win, text="You'll need to get your math accuracy up to 85% correct. Please try again with more concentration. \n\nClick to continue")
  ### SECTION 2 END

  ### SECTION 3 BEGIN
  log("Section 3")
  instructions = visual.TextStim(win, text="We will now combine the last two tasks. Letters and Math problems will alternate. "+
                                           "You will then be asked to recall all the letters from the series, indicating the order in which the letters were presented."+
                                           "\n\nYour score is valid only if you are at least 85% accurate in evaluating the math problems, "+
                                           "so try to answer all of those problems correctly while trying also to remember the order of the letters."+
                                           "\n\nThis task is difficult and most people find it challenging and frustrating at times. Keep a steady pace and do your best, "+
                                           "and remember, do not say the letters out loud. \n\nClick to continue.", wrapWidth=30)
  instructions.draw()
  win.flip()
  while 1 not in mouse.getPressed():
    pass
  while 1 in mouse.getPressed():
    pass
  # format {setsize:[(block 1 correctness,mathpercentage),...],...}
  results_overall = dict()
  maxOspan = []
  for block in range(NUM_TRIAL_BLOCKS):
    # set i at minimum set size
    ss = SET_SIZES[0]
    if len(maxOspan) > 0:
      ss = max(maxOspan[-1]-2,SET_SIZES[0])
    numWrong = 0
    maxOspan.append(0)
    while True:
      if ss not in results_overall:
        results_overall[ss] = []
      x = [j for j in range(len(LETTERS))]
      random.shuffle(x)
      # display letters
      mathQuestions = []
      for j in x[:ss]:
        displayLetter(win,LETTERS[j])
        win.flip()
        core.wait(IN_BETWEEN_LETTERS_TIME)
        mathQuestions.append(mathQuestion(win,mouse,mathTime))
        log(str(mathQuestions[-1]))
      mathPercentRight = (100.0 * sum([1 if mathQuestions[i][0]=="True" else 0 for i in range(len(mathQuestions))]))/len(mathQuestions)
      temp = validateSequence(win,mouse)
      correctSeq = [LETTERS[i] for i in x[:ss]]
      results_overall[ss].append((1.0*sum([2 if l=='TT' else 1 if l=='FT' else 0 for l in correctness(temp[0],correctSeq)])/(2.0*ss),mathPercentRight))
      if(temp[0]==correctSeq):
        tempLog = "(True,"
        colo = "Green"
        winsound.play()
        maxOspan[-1] = ss
        if ss < SET_SIZES[1]:
          ss += 1
        else:
          core.wait(TONE_LENGTH)
          visual.TextStim(win,text="This block is over. Your max O-SPAN was {0}".format(maxOspan[-1])).draw()
          win.flip()
          log("Max O-SPAN: " + str(maxOspan[-1]))
          core.wait(IN_BETWEEN_TRIALS_TIME*2)
          break
        numWrong = 0
      else:
        tempLog = "(False,"
        colo = "Orange"
        losesound.play()
        numWrong += 1
      mathcolo = "Green" if mathPercentRight >= 85 else "Orange"
      visual.TextStim(win,text=("Math Score: %.0f%%" % (mathPercentRight)),color=mathcolo,pos=(12,9)).draw()
      visual.TextStim(win,text="You recalled {0} letters correctly out of {1}".format(correctness(temp[0],correctSeq).count("TT"),len(correctSeq)),color=colo,wrapWidth=30).draw()
      numerrors = sum([1 if mathQuestions[i][0]!="True" else 0 for i in range(len(mathQuestions))])
      visual.TextStim(win,text="You made {0} math error{1} for this set of trials.".format(numerrors,"" if numerrors == 1 else "s"),color=mathcolo,pos=(0,-5),wrapWidth=30).draw()
      win.flip()
      core.wait(FEEDBACK_LENGTH)
      log(tempLog+str(correctSeq)+","+str(temp[0])+","+str(correctness(temp[0],correctSeq))+","+str(len(correctSeq))+","+str(temp[1])+")")
      if numWrong >= MAX_FAILS:
        if maxOspan[-1] <= 0 and ss > SET_SIZES[0]:
          ss -= 1
          continue
        core.wait(TONE_LENGTH)
        visual.TextStim(win,text="This block is over. Your max O-SPAN was {0}".format(maxOspan[-1])).draw()
        win.flip()
        log("Max O-SPAN: " + str(maxOspan[-1]))
        core.wait(IN_BETWEEN_TRIALS_TIME*2)
        break
  ### SECTION 3 END

  visual.TextStim(win,text="Thank you for your participation.").draw()
  win.flip()
  core.wait(3)

  oscores = []
  mathscores = []
  for key in results_overall.keys():
    oscores.append((100.0*sum([i[0] for i in results_overall[key]]))/len(results_overall))
    mathscores.append((1.0*sum([i[1] for i in results_overall[key]]))/len(results_overall))
  visual.SimpleImageStim(win, image=makeresultsplot(testNo,"Set Size","Percentage Correct(%)",results_overall.keys(),oscores,mathscores)).draw()
  win.flip()
  core.wait(8)

  # write results to a xls file with all other subjects
  try:
    import xlrd,xlwt,xlutils.copy
    excelfile = "data/ospan.xls"
    if not os.path.isfile(excelfile):
      w = xlwt.Workbook()
      ws = w.add_sheet("Data")
      style = xlwt.easyxf("font: bold on")
      ws.write(0,0,"Initials",style)
      ws.write(0,1,"Day",style)
      ws.write(0,2,"Avg Max O-SPAN",style)
      ws.write(0,3,"Avg Math Score",style)
      w.save(excelfile)
    oldfile = xlrd.open_workbook(excelfile,formatting_info=True)
    row = oldfile.sheet_by_index(0).nrows
    newfile = xlutils.copy.copy(oldfile)
    sheet = newfile.get_sheet(0)
    sheet.write(row,0,initials)
    sheet.write(row,1,testNo)
    sheet.write(row,2,(1.0*sum(maxOspan))/len(maxOspan))
    sheet.write(row,3,(1.0*sum(mathscores))/len(mathscores))
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

def makeresultsplot(name, xtext, ytext, xvalues, yvalues, yvalues2):
  """A simple plotter using matplotlib. 

  Arguments:
  @param name - file name prefixed by 'ospan' for saving
  @param xtext - text for the x-axis
  @param ytext - text for the y-axis
  @param xvalues - values for the x-axis
  @param yvalues - values for the OSPAN scores
  @param yvalues2 - values for the Math scores

  @return path to the image where the graph is saved
  """
  try:
    import matplotlib.pyplot as plt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(xvalues,yvalues,marker='o',label="O-SPAN")
    ax.plot(xvalues,yvalues2,marker='o',label="Math")
    plt.xlabel(xtext)
    plt.ylabel(ytext)
    plt.legend()
    plt.axis([SET_SIZES[0],SET_SIZES[1],0,101])
    plt.title("Graph of performance")
    plt.savefig(dataPath+str(name)+".png")
    return dataPath+str(name)+".png"
  except ImportError:
    print "ERROR: NO MATPLOTLIB.PYPLOT installed."

def correctness(sequence, correct):
  """Compares @param sequence to @param correct sequence for correctness.

  Arguments:
  @param sequence - the sequence from the subject
  @param correct - the correct sequence to be expected

  @return an array of 'XY' pairs where X is 'T' if the position of @param 
  sequence at that position is correct and 'F' if it is not, and Y is 'T' if 
  the sequence at that position has identity correctness or 'F' if not. 
  """
  measure = []
  i = 0
  while i < len(sequence):
    if i >= len(correct):
      measure.append('F')
    else:
      measure.append('T' if sequence[i]==correct[i] else 'F')
    measure[-1] += 'T' if sequence[i] in correct else 'F'
    i += 1
  return measure

def displayLetter(win,letter):
  """Display letter to screen.

  Arguments:
  @param win: psychopy Window to be used for display
  @param letter: letter to be displayed
  """
  # randomize letter's indices
  letter = visual.TextStim(win,text=letter)
  letter.setHeight(LETTER_SIZE)
  letter.draw()
  win.flip()
  core.wait(LETTER_DISPLAY_TIME)

def mathQuestion(win,mouse,timelimit):
  """Display a math question, waiting for user to click when ready, and then
  displays a possible answer, asking the user true or false. 
  Question must be answered within @param timelimit seconds, otherwise it will
  be counted as wrong.

  Math questions will be in the form:
          (a*b)+/-c=?
  @keyword a: random integer between LOWEST_NUMBER and HIGHEST_NUMBER
  @keyword b: random integer between LOWEST_NUMBER and HIGHEST_NUMBER
  @keyword c: random integer between LOWEST_NUMBER and HIGHEST_NUMBER

  Arguments:
  @param win: psychopy Window to be used for display
  @param mouse: psychopy Mouse used in display
  @param timelimit: time limit in seconds for the math question to be displayed

  @return a tuple of format: (true/error response, time to answer)
  """
  global lastMathProblem
  answer = -100
  winsound = sound.Sound(value=CORRECT_FREQ, secs=TONE_LENGTH)
  losesound = sound.Sound(value=INCORRECT_FREQ, secs=TONE_LENGTH)
  while True: # no same math problem twice in a row.
    a = random.randint(LOWEST_NUMBER,HIGHEST_NUMBER)
    b = random.randint(LOWEST_NUMBER,HIGHEST_NUMBER)
    c = random.randint(LOWEST_NUMBER,HIGHEST_NUMBER)
    if [a,b,c] != lastMathProblem: break
  lastMathProblem = [a,b,c]
  questiontext = "( "+str(a)+" * "+str(b)+" ) "
  if random.random() < 0.5:
    answer = a*b+c
    questiontext += "+ "+str(c) + " = ?"
  else:
    answer = a*b-c
    questiontext += "- "+str(c) + " = ?"
  instructions = visual.TextStim(win,text="When you have solved the math problem, click the mouse to continue.",pos=(0,-3),wrapWidth=30)
  question = visual.TextStim(win,text=questiontext,pos=(0,2))
  instructions.draw()
  question.draw()
  win.flip()
  timer = core.Clock()
  while 1 not in mouse.getPressed():
    if(timer.getTime()>= timelimit):
      instructions = visual.TextStim(win,text="Out of time!",pos=(0,-3))
      instructions.draw()
      win.flip()
      core.wait(1)
      return ("Speed Error", timer.getTime())
    if(event.getKeys(keyList=['q','escape'])):
      quit()
  while 1 in mouse.getPressed():
    pass
  time = timer.getTime()
  correct = random.random()<MATH_QUESTION_CHANCE_CORRECT
  ans = answer
  if not correct:
    if(random.random()<0.16):
      a -= 1
    elif(random.random()<0.33):
      a += 1
    elif(random.random()<0.49):
      b -= 1
    elif(random.random()<0.66):
      b += 1
    elif(random.random()<0.82):
      c -= 1
    else:
      c += 1
    ans = a*b+c
  ans = visual.TextStim(win,text=str(ans))
  trueText = visual.TextStim(win,text="True",pos=(-3,-3))
  trueButton = visual.Rect(win,width=3, height=1.2, lineWidth=2)
  trueButton.setPos((-3,-3))
  falseText = visual.TextStim(win,text="False",pos=(3,-3))
  falseButton = visual.Rect(win,width=3, height=1.2, lineWidth=2)
  falseButton.setPos((3,-3))
  ans.draw()
  trueText.draw()
  trueButton.draw()
  falseText.draw()
  falseButton.draw()
  win.flip()
  while(True):
    if(mouse.isPressedIn(trueButton)):
      while 1 in mouse.getPressed(): # wait until mouse is released
        pass
      if correct:
        tempLog = "True"
        winsound.play()
      else:
        tempLog = "Accuracy Error"
        losesound.play()
      win.flip()
      return (tempLog,time)
    elif(mouse.isPressedIn(falseButton)):
      while 1 in mouse.getPressed():
        pass
      if correct:
        tempLog = "Accuracy Error"
        losesound.play()
      else:
        tempLog = "True"
        winsound.play()
      win.flip()
      core.wait(TONE_LENGTH)
      return (tempLog,time)
    if(event.getKeys(keyList=['q','escape'])):
      quit()


def validateSequence(win, mouse):
  """Display a screen where users pick letters in the order they remember.
  
  Arguments:
  @param win: psychopy Window to be used for display
  @param mouse: psychopy Mouse used in display
  
  @return a tuple of the form: ([list of letters], time taken)
  """
  instructions = visual.TextStim(win,text="Select the letters in the order presented. Use the blank button to fill in forgotten letters.", pos=(0,10),wrapWidth=40)
  submitText = visual.TextStim(win,text="Submit",pos=(5,-5))
  submitButton = visual.Rect(win,width=4, height=1.2, lineWidth=2)
  backText = visual.TextStim(win,text="Back",pos=(-5,-5))
  backButton = visual.Rect(win,width=3, height=1.2, lineWidth=2)
  blankText = visual.TextStim(win,text="Blank",pos=(0,-3))
  blankButton = visual.Rect(win,width=3, height=1.2, lineWidth=2)
  blankButton.setPos((0,-3))
  backButton.setPos((-5,-5))
  submitButton.setPos((5,-5))
  submitButton.setAutoDraw(True)
  submitText.setAutoDraw(True)
  backButton.setAutoDraw(True)
  backText.setAutoDraw(True)
  blankButton.setAutoDraw(True)
  blankText.setAutoDraw(True)
  instructions.setAutoDraw(True)
  instructions.draw()
  submitButton.draw()
  submitText.draw()
  backButton.draw()
  backText.draw()
  blankButton.draw()
  blankText.draw()
  letterRects = []
  letterBoxes = []
  i = 0
  for i in range(len(LETTERS)):
    letterBoxes.append(visual.TextStim(win, text=LETTERS[i], pos=(6*(-1.5+(i/3)),4*((i%3)))))
    letterRects.append( visual.Rect(win,width=1.2,height=1.2,lineWidth=2))
    letterRects[i].setPos((6*(-1.5+(i/3)),4*(-0.03+(i%3))))
    letterRects[i].setAutoDraw(True)
    letterBoxes[i].setAutoDraw(True)
    letterRects[i].draw()
    letterBoxes[i].draw()
    i += 1
  win.flip()
  timer = core.Clock()
  currentI=1
  blankI=0
  numbers = []
  numbers2 = []
  clicked = []
  while(True):
    for i in range(len(LETTERS)):
      if(mouse.isPressedIn(letterRects[i]) and i not in clicked):
        clicked.append(i)
        numbers.append(visual.TextStim(win,text=currentI,color="DarkMagenta",pos=(6*(-1.7+(i/3)),4*((i%3)))))
        numbers[currentI-1].setAutoDraw(True)
        numbers[currentI-1].draw()
        currentI += 1
        numbers2.append(visual.TextStim(win,text=LETTERS[i],color="DarkMagenta",pos=(-10+2*len(numbers),-10)))
        numbers2[-1].setAutoDraw(True)
        numbers2[-1].draw()
        win.flip()
    if(mouse.isPressedIn(blankButton) and len(clicked) <= SET_SIZES[1]):
      clicked.append(-1)
      numbers.append(visual.TextStim(win,text=currentI,color="DarkMagenta",pos=(2+blankI,-3)))
      numbers[currentI-1].setAutoDraw(True)
      numbers[currentI-1].draw()
      currentI += 1
      blankI += 1
      numbers2.append(visual.TextStim(win,text="-",color="DarkMagenta",pos=(-10+2*len(numbers),-10)))
      numbers2[-1].setAutoDraw(True)
      numbers2[-1].draw()
      win.flip()
      core.wait(0.2)
    if(mouse.isPressedIn(backButton) and currentI > 1):
      currentI -= 1
      if clicked[-1] == -1:
        blankI -= 1
      clicked.remove(clicked[len(clicked)-1])
      numbers[currentI-1].setAutoDraw(False)
      numbers2[-1].setAutoDraw(False)
      numbers.remove(numbers[currentI-1])
      numbers2.remove(numbers2[-1])
      win.flip()
      core.wait(0.2)
    if(mouse.isPressedIn(submitButton)):
      #erase display
      for n in numbers+numbers2:
        n.setAutoDraw(False)
      submitButton.setAutoDraw(False)
      submitText.setAutoDraw(False)
      backButton.setAutoDraw(False)
      backText.setAutoDraw(False)
      blankButton.setAutoDraw(False)
      blankText.setAutoDraw(False)
      instructions.setAutoDraw(False)
      for i in range(len(LETTERS)):
        letterRects[i].setAutoDraw(False)
        letterBoxes[i].setAutoDraw(False)
      return ([LETTERS[i] if i != -1 else "-" for i in clicked],timer.getTime())
    if(event.getKeys(keyList=['q','escape'])):
      quit()

if __name__ == "__main__": main(sys.argv)
