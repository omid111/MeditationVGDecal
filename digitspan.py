#!/usr/bin/env python2
"""digitspan.py
A simple Digit Span psychological test using the PsychoPy python module. The 
test is comprised of two phases.
  1. NUM_PRACTICE_TRIALS of practice rounds, each with number presentation 
     of length PRACTICE_TRIAL_LENGTH.
  3. Actual rounds, beginning with a sequence of lengths within the ranges 
    REVERSE_RANGE and continuing until the sequences of length SET_SIZE_MAX or 
    the subject fails three rounds. This will be repeated NUM_TRIALS times.
  3. Actual rounds, beginning with a sequence of lengths within the ranges 
    REVERSE_RANGE and continuing until the sequences of length SET_SIZE_MAX or 
    the subject fails three rounds. The subject must recall in reverse order.
    This will be repeated NUM_TRIALS times.
In the actual experiment, the subject is presented with n digits, one at a 
time, each presented for STIMULI_TIME seconds. Then the user is asked to recall
the sequence using the number keypad on the computer.

Command-Line Execution: Instead of entering the subject initlas through the
psychopy gui, you can provide them as command line arguments when running 
with the terminal.

Log files:
  All log files are placed in the directory data/X/digitspan.txt, where X is 
  the initials of the participant. Each line of the log file describes 
  different actions occuring in the program. Here are the different possible 
  formats of each line in the log file:
    * Note: 'TIMESTAMP' indicates how many seconds have passed since the 
      initialization of the program
    * "MM/DD/YYYY HH:MM:SS" - at the beginning of the data file, indicates the 
      current date and time that the program began its execution.
    * "TIMESTAMP: SUBJECT: X" - indicates the subjects initials who this data 
      file belongs to.
    * "TIMESTAMP: Section [1-2]" - indicates that section data follows until 
      the next "Section X". Section 1 is practice, Section 2 is the real thing.
    * "TIMESTAMP: ([true/false],N,%f)" - indicates that a sequence of N squares
      has been recalled in %f time, incorrectly if false, and correctly if
      true.
    * "TIMESTAMP: END SUCCESS" - test has successfully completed
    * "TIMESTAMP: ERROR! QUIT OUT OF SYSTEM" - test has been quit by user, by
      pressing the 'q' or 'Esc' keys.
After imports, there is a list of global variables that change various aspects
of the program, modifiable to the administrators content.
"""
from psychopy import visual,core,event,gui
import random,numpy,sys,os,pyaudio
from datetime import datetime
__author__ = "Omid Rhezaii"
__email__ = "omid@rhezaii.com"
__copyright__ = "Copyright 2015, Michael Silver Lab"
__credits__ = ["Omid Rhezaii", "Sahar Yousef", "Michael Silver"]
__version__ = "1.0"
__status__ = "Awaiting Approval from Research Mentor"

# GLOBAL VARIABLE DECLARATIONS
ISI_TIME = 1.000
DIGIT_DISPLAY_TIME = 0.8000 # time each number is displayed
FORWARD_RANGE = (3,9)
REVERSE_RANGE = (2,9)
NUM_TRIALS = 1
DIGIT_SIZE = 12 # size of digits on screen display
# practice trial options
NUM_PRACTICE_TRIALS = 2
PRACTICE_TRIAL_LENGTH = 3

# Keep master time for whole program
programTime = core.Clock()
# log file location
logFile = "digitspan.txt"
def main(argv):
  """Main method to be runned at beginning"""
  global logFile, programTime

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

  if not os.path.isdir("data"):
    os.mkdir("data")
  if not os.path.isdir("data/"+initials):
    os.mkdir("data/"+initials)
  logFile = open("data/"+initials+"/"+logFile,"w+")
  log(datetime.now().strftime("%d/%m/%y %H:%M"))
  log("Subject: " + initials)
  win = visual.Window([800,600],monitor="testMonitor",units="deg",fullscr=True)
  mouse = event.Mouse(win=win)

  ### SECTION 1 BEGIN
  log("Section 1")
  instructions = visual.TextStim(win,text="Digit Span Practice\n\nIn this test you will have to try to remember a sequence of numbers that will appear on the screen one after the other.  When you hear the beep, type all of the numbers into the keyboard in the sequence in which they occurred.  If you correctly remember all of the numbers then the next list of numbers will be one number longer.  If you make a mistake then the next list of numbers will be one number shorter.  After three errors, the test will end.\n\nPress any key to Continue",wrapWidth=40)
  instructions.draw()
  win.flip()
  # wait until a key is pressed
  event.waitKeys()
  # begin practice trial
  for i in range(NUM_PRACTICE_TRIALS):
    x = range(10)
    random.shuffle(x)
    for i in x[:PRACTICE_TRIAL_LENGTH]:
      displayDigit(win,i)
    sound.soundPyo()
    temp = validateSequence(win,mouse)
    if temp[0]==x[:PRACTICE_TRIAL_LENGTH]:
      log("(True,"+str(PRACTICE_TRIAL_LENGTH)+","+str(temp[1])+")")
      feedback = visual.TextStim(win,text="Correct. Nice!")
    else:
      log("(False,"+str(PRACTICE_TRIAL_LENGTH)+","+str(temp[1])+")")
      feedback = visual.TextStim(win,text="Incorrect.")
    feedback.draw()
    win.flip()
    core.wait(1)
  ### SECTION 1 END

  ### SECTION 2 BEGIN
  log("Section 2")
  instructions = visual.TextStim(win,text="Digit Span Forward\n\nIn this test you will have to try to remember a sequence of numbers that will appear on the screen one after the other.  When you hear the beep, type all of the numbers into the keyboard in the same sequence in which they occurred.  If you correctly remember all of the numbers then the next list of numbers will be one number longer.  If you make a mistake then the next list of numbers will be one number shorter.  After three errors, the test will end.\n\nPress any key to Continue",wrapWidth=40)
  instructions.draw()
  win.flip()
  # wait until a key is pressed
  event.waitKeys()
  # begin practice trial
  for i in range(NUM_TRIALS):
    numFails = 0
    i = FORWARD_RANGE[0]
    while i <= FORWARD_RANGE[1]:
      x = range(10)
      random.shuffle(x)
      for dig in x[:i]:
        displayDigit(win,dig)
      temp = validateSequence(win,mouse)
      if temp[0]==x[:i]:
        log("(True,"+str(i)+","+str(temp[1])+")")
        feedback = visual.TextStim(win,text="Correct. Nice!")
        i += 1
      else:
        log("(False,"+str(i)+","+str(temp[1])+")")
        feedback = visual.TextStim(win,text="Incorrect.")
        if numFails == 3:
          feedback.draw()
          core.wait(1)
          break
        numFails += 1
      feedback.draw()
      win.flip()
      core.wait(1)
  ### SECTION 2 END

  ### SECTION 3 BEGIN
  log("Section 2")
  instructions = visual.TextStim(win,text="Digit Span Reverse\n\nIn this test you will have to try to remember a sequence of numbers that will appear on the screen one after the other.  When you hear the beep, type all of the numbers into the keyboard in the reverse sequence in which they occurred.  If you correctly remember all of the numbers then the next list of numbers will be one number longer.  If you make a mistake then the next list of numbers will be one number shorter.  After three errors, the test will end.\n\nPress any key to Continue",wrapWidth=40)
  instructions.draw()
  win.flip()
  # wait until a key is pressed
  event.waitKeys()
  # begin practice trial
  for i in range(NUM_TRIALS):
    numFails = 0
    i = REVERSE_RANGE[0]
    while i <= REVERSE_RANGE[1]:
      x = range(10)
      random.shuffle(x)
      for dig in x[:i]:
        displayDigit(win,dig)
      temp = validateSequence(win,mouse,reverse=" reverse")
      if temp[0]==x[:i][::-1]:
        log("(True,"+str(i)+","+str(temp[1])+")")
        feedback = visual.TextStim(win,text="Correct. Nice!")
        i += 1
      else:
        log("(False,"+str(i)+","+str(temp[1])+")")
        feedback = visual.TextStim(win,text="Incorrect.")
        if numFails == 3:
          feedback.draw()
          core.wait(1)
          break
        numFails += 1
      feedback.draw()
      win.flip()
      core.wait(1)
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

def displayDigit(win,digit):
  """Display number to screen.

  Arguments:
  @param win: psychopy Window to be used for display
  @param digit: digit to be displayed
  """
  # randomize letter's indices
  letter = visual.TextStim(win,text=str(digit))
  letter.setHeight(DIGIT_SIZE)
  letter.draw()
  win.flip()
  core.wait(DIGIT_DISPLAY_TIME)

def validateSequence(win,mouse,reverse=''):
  """Display a screen where users pick digits in the order they remember.
  
  Arguments:
  @param win: psychopy Window to be used for display
  @param mouse: psychopy Mouse used in display
  
  @return a tuple of the form: ([list of digits], time taken)
  """
  # numpad key values are prefixed with 'num_'
  DIGIT_SET=['num_'+str(i) for i in range(10)] + [str(i) for i in range(10)]

  instructions = visual.TextStim(win,text="Type the digits in the"+reverse+" order they appeared using the number keypad.", pos=(0,10),wrapWidth=80)
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
  win.flip()
  timer = core.Clock()
  numbers = []
  clicked = []
  while(True):
    for key in event.getKeys(keyList=DIGIT_SET):
      if len(key) > 1:
        key = key[4]
      if(key and key not in clicked):
        clicked.append(key)
        numbers.append(visual.TextStim(win,text=key,color="DarkMagenta",pos=(-10+2*len(numbers),0)))
        numbers[-1].setAutoDraw(True)
        numbers[-1].draw()
        win.flip()
    if(mouse.isPressedIn(backButton) and len(clicked) > 0):
      clicked.remove(clicked[len(clicked)-1])
      numbers[-1].setAutoDraw(False)
      numbers.remove(numbers[-1])
      win.flip()
      core.wait(0.2)
    if(mouse.isPressedIn(submitButton) or event.getKeys(keyList=['enter'])):
      #erase display
      for n in numbers:
        n.setAutoDraw(False)
      submitButton.setAutoDraw(False)
      submitText.setAutoDraw(False)
      backButton.setAutoDraw(False)
      backText.setAutoDraw(False)
      instructions.setAutoDraw(False)
      return ([int(i) for i in clicked],timer.getTime())
    if(event.getKeys(keyList=['q','escape'])):
      quit()

def beginSequenceandProbe(win, mouse, n):
  """Creates a random pattern of NUM_SQUARES squares of size SQUARE_SIZE 
  dimensions on the screen, and then proceeds to highlight a sequence of 
  @param n of them one at a time each for HIGHLIGHT_TIME. The program then 
  waits ISI_TIME, and then probes the subject by requesting that they recall
  the sequence that they just saw.
 
  Arguments:
  @param win: psychopy Window to be used for display
  @param mouse: psychopy Mouse used in display
  @param n: The length of the sequence of squares to be presented to the 
            subject

  @return a tuple of format: (true/false for correctness, n, time to answer.)
  """
  TIME_TO_FAIL = 5.000
  horizRange = (-10,10)
  vertRange = (-5,5)
  squares = []
  timer = core.Clock()
  for i in range(NUM_SQUARES):
    dimen = SQUARE_SIZE+MINIMUM_DISTANCE_BETWEEN_SQUARES
    temp = visual.Rect(win,lineWidth=0,pos=(random.uniform(*horizRange),random.uniform(*vertRange)),width=dimen,height=dimen,fillColor=SQUARE_COLOR)
    while timer.getTime() < TIME_TO_FAIL:
      overlaps = False
      for square in squares:
        if temp.overlaps(square):
          overlaps = True
          break
      if not overlaps:
        squares.append(temp)
        temp.setHeight(SQUARE_SIZE)
        temp.setWidth(SQUARE_SIZE)
        temp.draw()
        temp.setAutoDraw(True)
        break
      temp.setPos((random.uniform(*horizRange),random.uniform(*vertRange)))
  #check if we failed to draw 10 squares within TIME_TO_FAIL time
  if(timer.getTime()>=TIME_TO_FAIL):
    for square in squares:
      square.setAutoDraw(False)
    visual.TextStim(win,text="Computing...\n\nPlease Contact Your Test Administrator").draw()
    win.flip()
    log("COMPUTATION ERROR: SQUARES TOO BIG")
    print "COMPUTATION ERROR: SQUARES TOO BIG"
    core.wait(1)
    return

  #done creating irregular square pattern
  win.flip()
  sequence = range(NUM_SQUARES)
  random.shuffle(sequence)
  mouse.setVisible(0)
  for i in sequence[:n]:
    squares[i].setFillColor(SQUARE_HIGHLIGHT_COLOR)
    win.flip()
    core.wait(HIGHLIGHT_TIME)
    squares[i].setFillColor(SQUARE_COLOR)
  #erase screen
  for square in squares:
    square.setAutoDraw(False)
  win.flip()
  mouse.setVisible(1)
  core.wait(ISI_TIME)
  #begin asking for the subject to recall pattern
  for square in squares:
    square.setAutoDraw(True)
  instructions = visual.TextStim(win,text="Select the squares in the order they appeared.", pos=(0,10),wrapWidth=80)
  submitText = visual.TextStim(win,text="Submit",pos=(5,vertRange[0]-3))
  submitButton = visual.Rect(win,width=4, height=1.2, lineWidth=2)
  backText = visual.TextStim(win,text="Back",pos=(-5,vertRange[0]-3))
  backButton = visual.Rect(win,width=3, height=1.2, lineWidth=2)
  backButton.setPos((-5,vertRange[0]-3))
  submitButton.setPos((5,vertRange[0]-3))
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
  win.flip()
  #done rendering, time to start timer for subject response
  timer.reset()
  currentI=1
  numbers = []
  clicked = []
  while(True):
    for i in range(len(squares)):
      if(mouse.isPressedIn(squares[i]) and i not in clicked):
        clicked.append(i)
        numbers.append(visual.TextStim(win,text=currentI,pos=(squares[i].pos)))
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
      for number in numbers:
        number.setAutoDraw(False)
      submitButton.setAutoDraw(False)
      submitText.setAutoDraw(False)
      backButton.setAutoDraw(False)
      backText.setAutoDraw(False)
      instructions.setAutoDraw(False)
      for i in range(len(squares)):
        squares[i].setAutoDraw(False)
      return (sequence[:n]==clicked, n, timer.getTime())
    if(event.getKeys(keyList=['q','escape'])):
      quit()


if __name__ == "__main__": main(sys.argv)
