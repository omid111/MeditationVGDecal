#!/usr/bin/env python2
"""spanboard.py:
A simple Span-board psychological test using the PsychoPy python module. The 
test is comprised of two phases.
  1. NUM_PRACTICE_TRIALS of practice rounds, each with stimuli presentation 
     of length PRACTICE_TRIAL_LENGTH.
  2. Actual rounds, beginning with a sequence of length one and continuing 
    until the sequences of length SET_SIZE_MAX or the subject fails MAX_FAILS 
    rounds of the same set size in a row. This will be repeated 
    NUM_TRIAL_BLOCKS times.

The actual experiment is with ten blocks arranged in an irregular pattern in 
front of the subject. The program then highlights a number of blocks for 
HIGHLIGHT_TIME, in a sequence, and then there is ISI_TIME of a blank screen
followed by asking the user to click on the blocks in the same order they 
appeared.

Command-Line Execution: Instead of entering the subject initlas through the
psychopy gui, you can provide them as command line arguments when running 
with the terminal.

Log files:
  All log files are placed in the directory data/X/spanboard.txt, where X is 
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
    * "TIMESTAMP: Section [1-2]" - indicates that section data follows until 
      the next "Section X". Section 1 is practice, Section 2 is the real thing.
    * "TIMESTAMP: ([true/false],[correct response],[subject response],
      [accuracy],N,%f)" - indicates that a sequence of N squares have been 
      completed in %f time, incorrectly if false, and correctly if true.
    * "TIMESTAMP: Max SPAN-BOARD BLOCK X: Y" - maximum Span-Board for block X 
      is Y letters.
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
__version__ = "1.1"
__status__ = "Rough Draft"

# GLOBAL VARIABLE DECLARATIONS
ISI_TIME = 1.000
HIGHLIGHT_TIME = 0.8000 # time each square is highlighted during presentation
SET_SIZES = (1,11)  # from base number to top SS numbers
NUM_TRIAL_BLOCKS = 3
NUM_SQUARES = 12
SQUARE_SIZE = 2.5 # dimension for one side
MINIMUM_DISTANCE_BETWEEN_SQUARES = 1
SQUARE_COLOR = "DarkMagenta"
SQUARE_HIGHLIGHT_COLOR = "DarkOrange"
MAX_FAILS = 3
# sound settings
CORRECT_FREQ = 440
INCORRECT_FREQ = 330
TONE_LENGTH = 0.5
# practice trial options
NUM_PRACTICE_TRIALS = 2
PRACTICE_TRIAL_LENGTH = 3

# Keep master time for whole program
programTime = core.Clock()
# log file location
logFile = "spanboard"
dataFile = "spanboard"
squarePattern = []
iPattern = 0
def main(argv):
  """Main method to be runned at beginning"""
  global logFile, programTime, dataPath

  #do only if we werent given initials from the command line
  if len(argv) == 1:
    while True:
      dlg = gui.DlgFromDict(dictionary={'Initials':'','Test Number':'1'},title="Span-Board Task")
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
  dataPath = "data/"+initials+"/spanboard"

  if not os.path.isdir("data"):
    os.mkdir("data")
  if not os.path.isdir("data/"+initials):
    os.mkdir("data/"+initials)
  logFile = open("data/"+initials+"/"+logFile,"w+")
  log(datetime.now().strftime("%d/%m/%y %H:%M"))
  log("Subject: " + initials)
  log("Test Number: " + str(testNo))
  win = visual.Window([800,600],monitor="testMonitor",units="deg",fullscr=True)
  mouse = event.Mouse(win=win)
  winsound = sound.SoundPygame(value=CORRECT_FREQ, secs=TONE_LENGTH)
  losesound = sound.SoundPygame(value=INCORRECT_FREQ, secs=TONE_LENGTH)
  generateTemplates(win)

  ### SECTION 1 BEGIN
  log("Section 1")
  instructions = visual.TextStim(win,text="Span-board Practice\n\nIn this task, there will be squares in random locations on the screen. Then squares will become highlighted in a random order. Your task is to remember which squares were highlighted and in which order. You'll be asked to recreate the sequence at the end of the trial.\n\nClick to Continue")
  instructions.draw()
  win.flip()
  # wait until mouse is pressed and released
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

  for i in range(NUM_PRACTICE_TRIALS):
    temp = beginSequenceandProbe(win, mouse, PRACTICE_TRIAL_LENGTH)
    log(str(temp))
    win.flip()
    if temp[0]:
      winsound.play()
    else:
      losesound.play()
    core.wait(TONE_LENGTH)
  ### SECTION 1 END

  ### SECTION 2 BEGIN
  log("Section 2")
  instructions = visual.TextStim(win, text="In this task, there will be squares in random locations on the screen. Then squares will become highlighted in a random order. Your task is to remember which squares were highlighted and in which order. You'll be asked to recreate the sequence at the end of the trial. The length of the series will increase until you are not able to recall the series correctly. \n\n Click to continue.")
  instructions.draw()
  win.flip()
  while 1 not in mouse.getPressed():
    pass
  while 1 in mouse.getPressed():
    pass
  # format {setsize:[(block 1 correctness,mathpercentage),...],...}
  results_overall = dict()
  maxSpanBoard = []
  for i in range(NUM_TRIAL_BLOCKS):
    ss = SET_SIZES[0]
    numWrong = 0
    maxSpanBoard.append(0)
    while True:
      if ss not in results_overall:
        results_overall[ss] = []
      temp = beginSequenceandProbe(win, mouse, ss)
      log(str(temp))
      results_overall[ss].append(100*sum([2 if l=='TT' else 1 if l=='FT' else 0 for l in temp[3]])/(2.0*ss))
      if temp[0]:
        winsound.play()
        maxSpanBoard[-1] = ss
        if ss < SET_SIZES[1]:
          ss+= 1
        numWrong = 0
      else:
        losesound.play()
        numWrong += 1
      if numWrong >= MAX_FAILS:
        core.wait(TONE_LENGTH)
        visual.TextStim(win,text="This block is over. Your max Span-Board was {0}".format(maxSpanBoard[-1]) )
        win.flip()
        log("Max Span-Board Block "+str(i)+": " + str(maxSpanBoard[-1]))
        core.wait(3)
        break
      win.flip()
      core.wait(ISI_TIME)
  ### SECTION 2 END

  visual.TextStim(win,text="Thank you for your participation.").draw()
  win.flip()
  core.wait(3)

  spanscores = []
  for key in results_overall.keys():
    spanscores.append((100.0*sum(results_overall[key]))/NUM_TRIAL_BLOCKS)
  visual.SimpleImageStim(win, image=makeresultsplot(testNo,"Set Size","Percentage Correct(%)",results_overall.keys(),spanscores)).draw()
  win.flip()
  core.wait(8)

  # write results to a xls file with all other subjects
  import xlrd,xlwt,xlutils.copy
  excelfile = "data/spanboard.xls"
  if not os.path.isfile(excelfile):
    w = xlwt.Workbook()
    ws = w.add_sheet("Data")
    style = xlwt.easyxf("font: bold on")
    ws.write(0,0,"Initials",style)
    ws.write(0,1,"Day",style)
    ws.write(0,2,"Avg Max Span-Board",style)
    w.save(excelfile)
  oldfile = xlrd.open_workbook(excelfile,formatting_info=True)
  row = oldfile.sheet_by_index(0).nrows
  newfile = xlutils.copy.copy(oldfile)
  sheet = newfile.get_sheet(0)
  sheet.write(row,0,initials)
  sheet.write(row,1,testNo)
  sheet.write(row,2,(1.0*sum(maxSpanBoard))/len(maxSpanBoard))
  newfile.save(excelfile)

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

def makeresultsplot(name, xtext, ytext, xvalues, yvalues):
  """A simple plotter using matplotlib. 

  Arguments:
  @param name - file name prefixed by 'spanboard' for saving
  @param xtext - text for the x-axis
  @param ytext - text for the y-axis
  @param xvalues - values for the x-axis
  @param yvalues - values for the Span-Board scores

  @return path to the image where the graph is saved
  """
  import matplotlib.pyplot as plt
  fig = plt.figure()
  ax = fig.add_subplot(111)
  ax.plot(xvalues,yvalues,marker='o',label="Span-Board")
  plt.xlabel(xtext)
  plt.ylabel(ytext)
  plt.legend()
  plt.axis([SET_SIZES[0],SET_SIZES[1],0,100])
  plt.title("Graph of performance")
  plt.savefig(dataPath+str(name)+".png")
  return dataPath+str(name)+".png"

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

def generateTemplates(win):
  """Generate a bunch of ramdomized templates with NUM_SQUARES for display"""
  global squarePattern
  TIME_TO_FAIL = 2.500
  horizRange = (-10,10)
  vertRange = (-5,5)
  timer = core.Clock()
  bigN = (NUM_PRACTICE_TRIALS*PRACTICE_TRIAL_LENGTH)+(NUM_TRIAL_BLOCKS*(SET_SIZES[1]-SET_SIZES[0]))
  percent = visual.TextStim(win,text="0%")
  percent.setAutoDraw(True)
  for i in range(bigN):
    while True:
      squares = []
      timer.reset()
      for j in range(NUM_SQUARES):
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
            break
          if(event.getKeys(keyList=['q','escape'])):
            quit()
          temp.setPos((random.uniform(*horizRange),random.uniform(*vertRange)))
      #check if we failed to draw 10 squares within TIME_TO_FAIL time
      if(timer.getTime() < TIME_TO_FAIL):
        squarePattern.append(squares)
        percent.text = str("%.0f%%" % (100.0*i/bigN))
        win.flip()
        break
  percent.setAutoDraw(False)

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

  @return a tuple of format: (true/false for correctness,[correct response],
    [subject response],[accuracy] n, time to answer.)
  """
  global iPattern
  squares = squarePattern[iPattern]
  for square in squares:
    square.setAutoDraw(True)
  iPattern += 1
  #done creating irregular square pattern
  sequence = range(NUM_SQUARES)
  random.shuffle(sequence)
  for i in sequence[:n]:
    squares[i].setFillColor(SQUARE_HIGHLIGHT_COLOR)
    win.flip()
    core.wait(HIGHLIGHT_TIME)
    squares[i].setFillColor(SQUARE_COLOR)
  #erase screen
  for square in squares:
    square.setAutoDraw(False)
  win.flip()
  core.wait(ISI_TIME)
  #begin asking for the subject to recall pattern
  for square in squares:
    square.setAutoDraw(True)
  instructions = visual.TextStim(win,text="Select the squares in the order they appeared.", pos=(0,10),wrapWidth=80)
  submitText = visual.TextStim(win,text="Submit",pos=(5,-8))
  submitButton = visual.Rect(win,width=4, height=1.2, lineWidth=2)
  backText = visual.TextStim(win,text="Back",pos=(-5,-8))
  backButton = visual.Rect(win,width=3, height=1.2, lineWidth=2)
  backButton.setPos((-5,-8))
  submitButton.setPos((5,-8))
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
  timer = core.Clock()
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
      return (sequence[:n]==clicked,sequence[:n],clicked,correctness(clicked,sequence[:n]), n, timer.getTime())
    if(event.getKeys(keyList=['q','escape'])):
      quit()


if __name__ == "__main__": main(sys.argv)
