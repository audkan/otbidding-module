"""
bidding-mod.py implements an employee rotation and PCO work assignment.
Choices and available work data is sourced from Trapeze. Employee names are arbitrarily generated.
Input files must be tab-delimited text files.

Created by Audrey Kan, June-August 2019
"""
#-----------------------------------------------------------------------#
class Employee():
  # Stores info about a single employee: seniority, badge, and name
  def __init__(self, badge, sen, sur='', name=''):
    self._badgeID = badge
    self._seniority = sen
    self._surname = sur
    self._firstName = name
  
  # Prints BADGE  SURNAME, FIRST INITIAL
  def __str__(self):
    return str(self._badgeID) + '\t' +self._surname + ', ' + self._firstName[:1] + '.'
#-----------------------------------------------------------------------#
class Work():
  # Stores info about a single event: date, time, name (code), and number of employees needed
  def __init__(self, date, name, code, start, end, comp, num):
    self._date = date
    self._workName = name
    self._workCode = code
    self._startTime = start
    self._endTime = end
    self._isComp = comp
    self._numEmpNeeded = num

  # Decrements total employees needed when an employee is assigned
  def assignEmp(self):
    self._numEmpNeeded -= 1

  # Prints NAME (CODE)  START-END COMP
  def __str__(self):
    if self._workCode != '': codeStr = ' (' + self._workCode.upper() + ')'
    else: codeStr = ''
    if self._isComp: compStr = ' OR COMP'
    else: compStr = ' HRS'
    if self._endTime == '':
      endStr = ' UNTIL COMP'
      compStr = ''
    else: endStr = '-' + self._endTime
    return self._workName.upper() + codeStr + '\n' + self._startTime + endStr + compStr + '\n'
#-----------------------------------------------------------------------#
class Assignment():
  # Stores info about an assignment: employee and work
  def __init__(self, emp, work):
    self._employee = emp
    self._work = work

  # Prints SURNAME, FIRST INITIAL and NAME (CODE)  START-END COMP
  def __str__(self):
    return self._employee.__str__() + '\n' + self._work.__str__()

#-----------------------------------------------------------------------#
def rotateEmployees(senList, nextEmp):
  global rotationList
  rotationList = rotationList[senList.index(nextEmp):] + rotationList[:senList.index(nextEmp)]
  return zip(rotationList, senList)

#-----------------------------------------------------------------------#
#                               MAIN PROGRAM
#-----------------------------------------------------------------------#

import csv

employees = {} # Holds all refs of Employee objects
availableWork = {} # Holds all refs of Work objects
employeeChoices = [] # Holds all refs to Employee preferences
seniorityList = []
finalAssignments = [] # Holds all refs to the final employee/work assignment

#----------------------PROCESS INPUT TXT TILES--------------------------#
empFile = 'pco_emp.txt'
workFile = 'pco_otwork.txt'
choiceFile = 'pco_choices.txt'

with open(empFile, 'r') as employeeStr:
  employee_reader = csv.reader(employeeStr, delimiter='\t')
  for line in employee_reader:
    ref = int(line[0])
    employees[ref] = Employee(line[3], ref, line[1], line[2])
    seniorityList += [ref]
    
with open(workFile, 'r') as workStr:
  work_reader = csv.reader(workStr, delimiter='\t')
  for line in work_reader:
    ref = (line[0], line[2])
    if line[5].upper() == 'YES': comp = True
    else: comp = False
    availableWork[ref] = Work(line[0], line[1], line[2], line[3], line[4], comp, int(line[6]))

with open(choiceFile, 'r') as choicesStr:
  availableWorkKeys = list(availableWork.keys())
  choice_reader = csv.reader(choicesStr, delimiter='\t')
  for line in choice_reader:
    choiceList = []
    for count, preference in enumerate(line[1:]):
      # For all employee preferences, add to the employee's choice list 
      if preference != '': choiceList += [(int(preference), availableWorkKeys[count])]
    if choiceList != []: 
      choiceList = sorted(choiceList, key=lambda pref:pref[0])
      employeeChoices += [(int(line[0]), choiceList)]

#------------------------EMPLOYEE ROTATION------------------------------#
nextEmp = input('Enter SEN # to begin next rotation: ')
rotationList = range(1, len(seniorityList) + 1)
seniorityRotationList = rotateEmployees(seniorityList, nextEmp)
print(seniorityRotationList)

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
