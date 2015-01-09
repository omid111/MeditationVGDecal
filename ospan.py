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
     letters in the order they appeared. This is repeated NUM_TRIALS times for
     each of the set sizes in SET_SIZES. If a user takes more than mathTime 
     time to observe a math problem, it is counted as incorrect, and the test 
     continues to the next letter.

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
    * "TIMESTAMP: Section [1-3]" - indicates that section data follows until 
      the next "Section X".
    * "TIMESTAMP: ([true/fase],%f)" - indicates that a math problem has been 
      completed correctly if true, or incorrectly if false, in float %f time. 
    * "TIMESTAMP: ([true/false],N,%f)" - indicates that a sequence of N letters
      has been completed in %f time, incorrectly if false, and correctly if
      true.
    * "TIMESTAMP: END SUCCESS" - test has successfully completed
    * "TIMESTAMP: ERROR! QUIT OUT OF SYSTEM" - test has been quit by user, by
      pressing the 'q' or 'Esc' keys.
After imports, there is a list of global variables that change various aspects
of the program, modifiable to the administrators content.
"""
from psychopy import visual,core,event,gui
import random,numpy,sys,os
from datetime import datetime
__author__ = "Omid Rhezaii"
__email__ = "omid@rhezaii.com"
__copyright__ = "Copyright 2015, Michael Silver Lab"
__credits__ = ["Omid Rhezaii", "Sahar Yousef", "Michael Silver"]
__version__ = "1.0"
__status__ = "Awaiting Approval from Research Mentor"

# GLOBAL VARIABLE DECLARATIONS
LETTERS=("F", "H", "J", "K", "L", "N", "P", "Q", "R", "S", "T", "Y")
IN_BETWEEN_TRIALS_TIME = 0.5
MATH_QUESTION_CHANCE_CORRECT = 0.5
# letter display options
LETTER_DISPLAY_TIME = 0.800
LETTER_SIZE = 12       # for display size
# practice trial(section 1) options
NUM_PRACTICE_TRIALS = 1
NUM_PRACTICE_TRIAL_LETTERS = 3
IN_BETWEEN_LETTERS_TIME = 0.200
# math callibrator(section 2) options
NUM_MATH_PROBLEMS = 10
HIGHEST_NUMBER = 9
# section 3 options
SET_SIZES = range(3,8) # from base number up to but not including top number
NUM_TRIALS = 3         # number of trials for each set size.

#Keep master time for whole program
programTime = core.Clock()
#log file location
logFile = "ospan.txt"
def main():
  """Main method to be runned at beginning"""
  # beginning checks
  global logFile, programTime
  if(len(LETTERS)!=12):
    print("This program is only configured to work with 12 letters.")
    return;

  #do only if we werent given initials from the command line
  if len(argv) == 1:
    while True:
      dlg = gui.DlgFromDict(dictionary={'Initials':''},title="O-SPAN Task")
      if(dlg.OK):
        initials = dlg.data[0]
      else:
        sys.exit(1)
      if(os.path.isfile("data/"+initials+"/"+logFile)):
        error = gui.Dlg(title="Existing Log File",labelButtonOK=u'Yes',labelButtonCancel=u'No')
        error.addText("A log file with initials " + initials+ " already exists. Are you sure you want to overwrite? If not, answer no and change your initials." )
        error.show()
        if error.OK:
          os.remove("data/"+initials+"/"+logFile)
          break
        else:
          continue
      else:
        break
  elif(len(argv)==2):
    initials = argv[1]
  else:
    print "Too many command line arguments. Please read documentation."
    sys.exit(1)

  #if there is no folder data, make one
  if not os.path.isdir("data"):
    os.mkdir("data")
  #if subject has no folder in data yet, make one
  if not os.path.isdir("data/"+initials):
    os.mkdir("data/"+initials)
  logFile = open("data/"+initials+"/"+logFile,"w+")
  log(datetime.now().strftime("%d/%m/%y %H:%M"))
  log("Subject: " + initials)
  #make our monitor
  win = visual.Window([800,600],monitor="testMonitor",units="deg",fullscr=True)
  mouse = event.Mouse(win=win)

  ### SECTION 1 BEGIN
  log("Section 1")
  instructions = visual.TextStim(win,text="Operational Span Practice\n\nMemorize the order of the letters, and at the end of \nthe sequence of letters, click them in the appropriate order from the options.\n\nClick to Continue")
  instructions.draw()
  win.flip()
  # wait until mouse is pressed
  while 1 not in mouse.getPressed():
    pass
  while 1 in mouse.getPressed():
    pass
  # begin practice trial
  mouse.setVisible(0)
  for j in range(NUM_PRACTICE_TRIALS):
    x = [i for i in range(len(LETTERS))]
    random.shuffle(x)
    for i in x[:NUM_PRACTICE_TRIAL_LETTERS]:
      displayLetter(win,LETTERS[i])
      win.flip()
      core.wait(IN_BETWEEN_LETTERS_TIME)
    mouse.setVisible(1)
    temp = validateSequence(win,mouse)
    if(temp[0]==[LETTERS[i] for i in x[:NUM_PRACTICE_TRIAL_LETTERS]]):
      log("(True,"+str(NUM_PRACTICE_TRIAL_LETTERS)+","+str(temp[1])+")")
      visual.TextStim(win,text="Correct, congratulations!").draw()
    else:
      log("(False,"+str(NUM_PRACTICE_TRIAL_LETTERS)+","+str(temp[1])+")")
      visual.TextStim(win,text="Incorrect.").draw()
    win.flip()
    core.wait(IN_BETWEEN_TRIALS_TIME)
  ### SECTION 1 END

  ### SECTION 2 BEGIN
  log("Section 2")
  instructions = visual.TextStim(win, text="Math Diagnostic Test\n\nCalculate the math question and compare it to the result given, if they are equal, say true, otherwise say false. \n\n Click to continue.")
  instructions.draw()
  win.flip()
  while 1 not in mouse.getPressed():
    pass
  while 1 in mouse.getPressed():
    pass
  mathTrials = []
  for i in range(NUM_MATH_PROBLEMS):
    temp = mathQuestion(win,mouse,9999)
    log(str(temp))
    mathTrials.append(temp)
    core.wait(IN_BETWEEN_TRIALS_TIME)
  mathTimes = [mathTrials[i][1] for i in range(len(mathTrials))]
  mathTime = sum(mathTimes)/len(mathTrials) + 2.5*numpy.std(mathTimes)
  ### SECTION 2 END

  ### SECTION 3 BEGIN
  log("Section 3")
  instructions = visual.TextStim(win, text="Operational Span Test\n\nPut the skills you have practiced together, and don't take to long on the math questions. \n\nClick to continue.")
  instructions.draw()
  win.flip()
  while 1 not in mouse.getPressed():
    pass
  while 1 in mouse.getPressed():
    pass
  tests = NUM_TRIALS * SET_SIZES
  random.shuffle(tests)
  for trial in tests:
    mouse.setVisible(0)
    x = [i for i in range(len(LETTERS))]
    random.shuffle(x)
    for i in x[:trial]:
      displayLetter(win,LETTERS[i])
      win.flip()
      core.wait(IN_BETWEEN_LETTERS_TIME)
      mouse.setVisible(1)
      log(str(mathQuestion(win,mouse,mathTime)))
    temp = validateSequence(win,mouse)
    if(temp[0]==[LETTERS[i] for i in x[:trial]]):
      log("(True,"+str(trial)+","+str(temp[1])+")")
      visual.TextStim(win,text="Correct, congratulations!").draw()
    else:
      log("(False,"+str(trial)+","+str(temp[1])+")")
      visual.TextStim(win,text="Incorrect.").draw()
    win.flip()
    core.wait(IN_BETWEEN_TRIALS_TIME)
  ### SECTION 3 END

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
  @keyword a: random integer between 1 and HIGHEST_NUMBER
  @keyword b: random integer between 1 and HIGHEST_NUMBER
  @keyword c: random integer between 1 and HIGHEST_NUMBER

  Arguments:
  @param win: psychopy Window to be used for display
  @param mouse: psychopy Mouse used in display
  @param timelimit: time limit in seconds for the math question to be displayed
                    before counting as incorrect.

  @return a tuple of format: (true/false for correct response, time to answer)
  """
  answer = -100
  a = random.randint(1,HIGHEST_NUMBER)
  b = random.randint(1,HIGHEST_NUMBER)
  c = random.randint(1,HIGHEST_NUMBER)
  questiontext = "( "+str(a)+" * "+str(b)+" ) "
  if random.random() < 0.5:
    answer = a*b+c
    questiontext += "+ "+str(c) + " = ?"
  else:
    answer = a*b-c
    questiontext += "- "+str(c) + " = ?"
  instructions = visual.TextStim(win,text="Click anywhere to Continue.",pos=(0,-3))
  question = visual.TextStim(win,text=questiontext,pos=(0,2))
  instructions.draw()
  question.draw()
  mouse.setVisible(0)
  win.flip()
  timer = core.Clock()
  while 1 not in mouse.getPressed():
    if(timer.getTime()>= timelimit):
      instructions = visual.TextStim(win,text="Out of time!",pos=(0,-3))
      instructions.draw()
      win.flip()
      core.wait(1)
      return (False, timer.getTime())
    if(event.getKeys(keyList=['q','escape'])):
      quit()
  while 1 in mouse.getPressed():
    pass
  mouse.setVisible(1)
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
  trueText = visual.TextStim(win,text="True",pos=(3,-3))
  trueButton = visual.Rect(win,width=3, height=1.2, lineWidth=2)
  trueButton.setPos((3,-3))
  falseText = visual.TextStim(win,text="False",pos=(-3,-3))
  falseButton = visual.Rect(win,width=3, height=1.2, lineWidth=2)
  falseButton.setPos((-3,-3))
  ans.draw()
  trueText.draw()
  trueButton.draw()
  falseText.draw()
  falseButton.draw()
  win.flip()
  while(True):
    if(mouse.isPressedIn(trueButton)):
      while 1 in mouse.getPressed():
        pass
      if correct:
        visual.TextStim(win,text="Correct, congratulations!").draw()
      else:
        visual.TextStim(win,text="Incorrect.").draw()
      win.flip()
      core.wait(IN_BETWEEN_TRIALS_TIME)
      return (correct,time)
    elif(mouse.isPressedIn(falseButton)):
      while 1 in mouse.getPressed():
        pass
      if not correct:
        visual.TextStim(win,text="Correct, congratulations!").draw()
      else:
        visual.TextStim(win,text="Incorrect.").draw()
      win.flip()
      core.wait(IN_BETWEEN_TRIALS_TIME)
      return (not correct,time)
    if(event.getKeys(keyList=['q','escape'])):
      quit()


def validateSequence(win, mouse):
  """Display a screen where users pick letters in the order they remember.
  
  Arguments:
  @param win: psychopy Window to be used for display
  @param mouse: psychopy Mouse used in display
  
  @return a tuple of the form: ([list of letters], time taken)
  """
  instructions = visual.TextStim(win,text="Select the letters in the order they appeared.", pos=(0,10),wrapWidth=80)
  submitText = visual.TextStim(win,text="Submit",pos=(5,-5))
  submitButton = visual.Rect(win,width=4, height=1.2, lineWidth=2)
  backText = visual.TextStim(win,text="Back",pos=(-5,-5))
  backButton = visual.Rect(win,width=3, height=1.2, lineWidth=2)
  backButton.setPos((-5,-5))
  submitButton.setPos((5,-5))
  submitButton.setAutoDraw(True)
  submitText.setAutoDraw(True)
  backButton.setAutoDraw(True)
  backText.setAutoDraw(True)
  instructions.setAutoDraw(True)
  instructions.draw()
  submitButton.draw()
  submitText.draw()
  backButton.draw()
  backText.draw()
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
  numbers = []
  clicked = []
  while(True):
    for i in range(len(LETTERS)):
      if(mouse.isPressedIn(letterRects[i]) and i not in clicked):
        clicked.append(i)
        numbers.append(visual.TextStim(win,text=currentI,color="DarkMagenta",pos=(6*(-1.7+(i/3)),4*((i%3)))))
        numbers[currentI-1].setAutoDraw(True)
        numbers[currentI-1].draw()
        currentI += 1
        win.flip()
    if(mouse.isPressedIn(backButton) and currentI > 1):
      currentI -= 1
      clicked.remove(clicked[len(clicked)-1])
      numbers[currentI-1].setAutoDraw(False)
      numbers.remove(numbers[currentI-1])
      win.flip()
      core.wait(0.2)
    if(mouse.isPressedIn(submitButton)):
      #erase display
      for n in numbers:
        n.setAutoDraw(False)
      submitButton.setAutoDraw(False)
      submitText.setAutoDraw(False)
      backButton.setAutoDraw(False)
      backText.setAutoDraw(False)
      instructions.setAutoDraw(False)
      for i in range(len(LETTERS)):
        letterRects[i].setAutoDraw(False)
        letterBoxes[i].setAutoDraw(False)
      return ([LETTERS[i] for i in clicked],timer.getTime())
    if(event.getKeys(keyList=['q','escape'])):
      quit()

if __name__ == "__main__": main(sys.argv)
