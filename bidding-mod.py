"""
bidding-mod.py implements an employee rotation and PCO work assignment.
Choices and available work data is sourced from Trapeze. 
Employee names are arbitrarily generated.
Input files must be tab-delimited text files.

Created by Audrey Kan, June-August 2019
"""
#-----------------------------------------------------------------------#
class Employee():
  # Stores info about a single employee
  def __init__(self, badge, sen, sur='', name=''):
    self._badgeID = badge
    self._seniority = sen
    self._surname = sur
    self._firstName = name
  
  # Prints BADGE  SURNAME, FIRST INITIAL
  def printEmployee(self):
    return str(self._badgeID) + '\t' +self._surname + ', ' \
      + self._firstName[:1] + '.'
  
  def __str__(self):
    return self._seniority + '\t' + str(self._badgeID) + '\t' 
      + self._surname + '\t' + self._firstName[:1]
#-----------------------------------------------------------------------#
class Work():
  # Stores info about a single work event
  def __init__(self, date, name, code, start, end, comp, num):
    self._date = date
    self._workName = name
    self._workCode = code
    self._startTime = start
    self._endTime = end
    self._isComp = comp
    self._numEmpNeeded = num
    
  # Prints NAME (CODE)  START-END COMP
  def printWork(self):
    if self._workCode != '': codeStr = ' (' + self._workCode.upper() + ')'
    else: codeStr = ''
    if self._isComp: compStr = ' OR COMP'
    else: compStr = ' HRS'
    if self._endTime == '':
      endStr = ' UNTIL COMP'
      compStr = ''
    else: endStr = '-' + self._endTime
    return self._workName.upper() + ' ' + codeStr + '\n' + self._startTime \
      + '-' + endStr + compStr
  
  def __str__(self):
    return self._date + '\t' + self._workName.upper() + '\t' 
      + self._workCode + '\t' + self._startTime + '\t' 
      + self._endTime + '\t' + str(self._isComp)
#-----------------------------------------------------------------------#
class Assignment():
  # Stores info about an assignment: employee and work
  def __init__(self, emp, work):
    self._employee = emp
    self._work = work
    
  def __str__(self):
    return self._employee.__str__() + '\t' + self._work.__str__()

#-----------------------------------------------------------------------#
class SSD():
  # Stores variables for global use
  def __init__(self):
    employees = {} # Holds all refs of Employee objects
    openWork = {} # Holds all refs of Work objects
    employeeBids = [] # Holds all refs to Employee preferences
    seniorityList = []
    assignments = [] # Holds all refs to employee/work assignment
    
#-----------------------------------------------------------------------#
def rotateEmployees(n):
  global rotationList
  rotationList = rotationList[SSD.senList.index(n):] \
    + rotationList[:SSD.senList.index(n)]
  return zip(rotationList, SSD.senList)

def employeesToAssign():
  sum = 0
  for i in SSD.openWork: sum += SSD.openWork[i]._numEmpNeeded
  return sum

def assignEmployeesToWork():
  for choice in SSD.employeeBids:
    for bid in choice[1]:
      if SSD.openWork[bid[1]]._numEmpNeeded > 0 and not(any(
        (obj._employee._seniority, (obj._work._date, obj._work._workCode)) 
        == (choice[0], bid[1]) for obj in SSD.assignments)):
        openWork[bid[1]]._numEmpNeeded -= 1
        SSD.assignments += [Assignment
                            (employees[choice[0]], openWork[bid[1]])]
        break
#-----------------------------------------------------------------------#
#                               MAIN PROGRAM
#-----------------------------------------------------------------------#

import csv

#----------------------PROCESS INPUT TXT TILES--------------------------#
empFile = 'pco_emp_test.txt'
workFile = 'pco_otwork.txt'
choiceFile = 'pco_choices.txt'

with open(empFile, 'r') as employeeStr:
  employee_reader = csv.reader(employeeStr, delimiter='\t')
  for line in employee_reader:
    ref = int(line[0])
    SSD.employees[ref] = Employee(line[3], ref, line[1], line[2])
    SSD.seniorityList += [ref]
    
with open(workFile, 'r') as workStr:
  work_reader = csv.reader(workStr, delimiter='\t')
  for line in work_reader:
    ref = (line[0], line[2])
    if line[5].upper() == 'YES': comp = True
    else: comp = False
    SSD.openWork[ref] = Work(line[0], line[1], line[2], line[3], \
                              line[4], comp, int(line[6]))

with open(choiceFile, 'r') as choicesStr:
  openWorkKeys = list(SSD.openWork.keys())
  choice_reader = csv.reader(choicesStr, delimiter='\t')
  for line in choice_reader:
    choiceList = []
    for count, preference in enumerate(line[1:]):
      # For all employee preferences, add to the employee's choice list 
      if preference != '': choiceList 
        += [(int(preference), openWorkKeys[count])]
    if choiceList != []: 
      SSD.employeeBids += [
        (int(line[0]), sorted(choiceList, key=lambda pref:pref[0]))]

#------------------------EMPLOYEE ROTATION------------------------------#
nextEmp = input('Enter SEN # to begin next rotation: ')
rotationList = range(1, len(SSD.seniorityList) + 1)
seniorityRotationList = rotateEmployees(nextEmp)
print(seniorityRotationList)

# How to integrate employee rotation with iterations? 

#-------------------------ASSIGNMENT ITERATIONS-------------------------#
assignEmployeesToWork() # First iteration through assignment
assignEmployeesToWork() # Second iteration through assignment

#if employeesToAssign() != 0:
# find index of work not filled
# start at the end of the list
# if (sen, (date,work) is not in assignments
# assign inverse work 

# Print formatted assignment for checking 
 employees = {} # Holds all refs of Employee objects
    openWork = {} # Holds all refs of Work objects
    employeeBids = [] # Holds all refs to Employee preferences
    seniorityList = []
    assignments = [] # Holds all refs to employee/work assignment
    
i = 0
while i != len(assignments):
  print(assignments[i].__str__())
  i += 1

with open("FinalAssignments.txt", "w") as out: 
  for i in SSD.assignments:
    out.write(assignments[i].__str__())
    
