"""
OTBidding.py implements an employee rotation and PCO work assignment.
Data source is from Trapeze. Input files must be tab-delimited text files.

Created by Audrey Kan, July 2019
"""
#-----------------------------------------------------------------------#
class Employee():
  # Stores info about a single employee: seniority, badge, and name
  def __init__(self, b, s, sur='', n=''):
    self._badge = b
    self._sen = s
    self._surname = sur
    self._name = n
  
  # Prints BADGE  SURNAME, FIRST INITIAL
  def __str__(self):
    return str(self._badge) + '\t' +self._surname + ', ' + self._name[:1] + '.'
#-----------------------------------------------------------------------#
class Work():
  # Stores info about a single event: date, time, name (code), and number of employees needed
  def __init__(self, dt, name, c, s, e, comp, n):
    self._date = dt
    self._name = name
    self._code = c
    self._start = s
    self._end = e
    self._comp = comp
    self._numEmp = n

  # Decrements total employees needed when an employee is assigned
  def assignEmp(self):
    self._numEmp -= 1

  # Prints NAME (CODE)  START-END COMP
  def __str__(self):
    if self._code != '': codeStr = ' (' + self._code.upper() + ')'
    else: codeStr = ''
    if self._comp: compStr = ' OR COMP'
    else: compStr = ' HRS'
    if self._end == '':
      endStr = ' UNTIL COMP'
      compStr = ''
    else: endStr = '-' + self._end
    return self._name.upper() + codeStr + '\n' + self._start + endStr + compStr + '\n'
#-----------------------------------------------------------------------#
class Assignment():
  # Stores info about an assignment: employee and work
  def __init__(self, e, w):
    self._emp = e
    self._work = w

  # Prints SURNAME, FIRST INITIAL and NAME (CODE)  START-END COMP
  def __str__(self):
    return self._emp.__str__() + '\n' + self._work.__str__()

#-----------------------------------------------------------------------#
def rotate(n):
  global rot
  return rot[n:] + rot[:n]

def mergeSort(r, s):
  return zip(r, s)

def empRotation(s, n):
  global rot
  rot = rot[sen.index(n):] + rot[:sen.index(n)]
  return mergeSort(rot, s)

#-----------------------------------------------------------------------#
#                               MAIN PROGRAM
#-----------------------------------------------------------------------#

import csv

emp = {} #Holds all refs of Employee objects
sen = []
otw = {} #Holds all refs of Work objects
choices = [] #Holds all refs to Employee preferences
assignments = [] #Holds all refs to the final employee/work assignment

empFile = 'pco_emp.txt'
otwFile = 'pco_otwork.txt'
choiceFile = 'pco_choices.txt'

with open(empFile, 'r') as empStr:
  emp_reader = csv.reader(empStr, delimiter='\t')
  for line in emp_reader:
    ref = int(line[0])
    emp[ref] = Employee(line[3], ref, line[1], line[2])
    sen += [ref]
    
with open(otwFile, 'r') as otwStr:
  otw_reader = csv.reader(otwStr, delimiter='\t')
  for line in otw_reader:
    ref = (line[0], line[2])
    if line[5].upper() == 'YES': comp = True
    else: comp = False
    otw[ref] = Work(line[0], line[1], line[2], line[3], line[4], comp, int(line[6]))

with open(choiceFile, 'r') as choicesStr:
  w = list(otw.keys())
  choice_reader = csv.reader(choicesStr, delimiter='\t')
  for line in choice_reader:
    c = []
    for count, x in enumerate(line[1:]):
      if x!='':
        c += [(int(x),w[count])]
    if c != []: 
      c = sorted(c, key=lambda x:x[0])
      choices += [(int(line[0]), c)]

nextEmp = input('Enter SEN # of next first employee: ')
rot = range(1, len(sen) + 1)
rotatedList = empRotation(sen, nextEmp)
print(rotatedList)

# First iteration through assignments
for choice in choices:
  for bid in choice[1]:
    if otw[bid[1]]._numEmp > 0:
      otw[bid[1]].assignEmp()
      assignments += [Assignment(emp[choice[0]], otw[bid[1]])]
      break

# Second iteration through assignments
for choice in choices:
  for bid in choice[1]:
    if otw[bid[1]]._numEmp > 0 and not(any((obj._emp._sen, (obj._work._date, obj._work._code)) == (choice[0], bid[1]) for obj in assignments)):
      otw[bid[1]].assignEmp()
      assignments += [Assignment(emp[choice[0]], otw[bid[1]])]
      break

# If not all otw is filled
# start at the end of the list
# assign inverse work 

# rotate employee by picking employee sen# as 1st. 
# Generate rotation list in order based on given employee seniority #

# Print formatted assignment for checking 

# Write to file for final copy

"""
i = 0
while i != len(assignments):
  print(assignments[i].__str__())
  i += 1

for i in otw:
  print(otw[i]._numEmp)

"""
