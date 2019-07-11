"""
main.py implements an employee rotation and PCO work assignment.
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
    return str(self._seniority) + '\t' +self._surname + ', ' + self._firstName[:1] + '.' + ' ('+ str(self._badgeID) + ')' 
  
  def __str__(self):
    return str(self._seniority) + '\t' + str(self._badgeID) + '\t' + self._surname + '\t' + self._firstName
#-----------------------------------------------------------------------#
class Work():
  # Stores info about a single work event
  def __init__(self, d, name, code, start, end, comp, num):
    self._date = d
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
    return self._workName.upper() + ' ' + codeStr + '\n' + self._startTime + endStr + compStr
  
  def __str__(self):
    return self._date + '\t' + self._workName.upper() + '\t' + self._workCode + '\t' + self._startTime + '\t' + self._endTime + '\t' + str(self._isComp)
#-----------------------------------------------------------------------#
class Assignment():
  # Stores info about an assignment: employee and work
  def __init__(self, emp, work):
    self._employee = emp
    self._work = work
    
  def __str__(self):
    return self._employee.__str__() + '\t' + self._work.__str__()

#-----------------------------------------------------------------------#
def rotateEmployees(senList, rotList, n):
  rotated = rotList[-senList.index(n):] + rotList[:-senList.index(n)]
  tempSortedList = sorted(zip(senList, rotated), key=lambda x:x[1])
  newEmployeeRot = []
  for senRot in tempSortedList:
    newEmployeeRot += [senRot[0]]
  return newEmployeeRot

def assignEmployeesToWork(employeeBids, openWork):
  global assignments
  for choice in employeeBids:
    for bid in choice[1]:
      if openWork[bid[1]]._numEmpNeeded > 0 and not(any((obj._employee._seniority, (obj._work._date, obj._work._workCode)) == (choice[0], bid[1]) for obj in assignments)):
        openWork[bid[1]]._numEmpNeeded -= 1
        assignments += [Assignment(employees[choice[0]], openWork[bid[1]])]
        break
#-----------------------------------------------------------------------#
#                               MAIN PROGRAM
#-----------------------------------------------------------------------#
from collections import OrderedDict
import csv

employees = OrderedDict() # Holds all refs of Employee objects
openWork = OrderedDict() # Holds all refs of Work objects
employeeBids = [] # Holds all refs to Employee preferences
seniorityList = []
assignments = [] # Holds all refs to employee/work assignment
#----------------------PROCESS INPUT TXT TILES--------------------------#
empFile = 'pco_emp_test.txt'
workFile = 'pco_otwork.txt'
choiceFile = 'pco_choices.txt'

#Initializes employees
with open(empFile, 'r') as employeeStr:
  employee_reader = csv.reader(employeeStr, delimiter='\t')
  for line in employee_reader:
    ref = int(line[0])
    employees[ref] = Employee(line[3], ref, line[1], line[2])
    seniorityList += [ref]

nextEmp = input('Enter SEN # to begin next rotation: ')
newEmployeeRotation = rotateEmployees(seniorityList, list(range(1, len(seniorityList) + 1)), nextEmp)
employees = OrderedDict((key, employees[key]) for key in newEmployeeRotation)

#What if Debbie wants to rotate again?

#Initializes openWork
with open(workFile, 'r') as workStr:
  work_reader = csv.reader(workStr, delimiter='\t')
  for line in work_reader:
    ref = (line[0], line[2])
    if line[5].upper() == 'YES': comp = True
    else: comp = False
    openWork[ref] = Work(line[0], line[1], line[2], line[3], line[4], comp, int(line[6]))

#Initializes employeeBids
with open(choiceFile, 'r') as choicesStr:
  workKeys = list(openWork.keys())
  choice_reader = csv.reader(choicesStr, delimiter='\t')
  for line in choice_reader:
    choiceList = []
    for count, preference in enumerate(line[1:]):
      # For all employee preferences, add to the employee's choice list 
      if preference != '': 
        choiceList += [(int(preference), workKeys[count])]
    if choiceList != []: 
      choiceList = sorted(choiceList, key=lambda x:x[0])
      employeeBids += [(int(line[0]), choiceList)]

tempBidList = []
for pos in newEmployeeRotation:
  tempBidList += [(pos, bid[1]) for bid in employeeBids if bid[0] == pos]
employeeBids = tempBidList

#-------------------------ASSIGNMENT ITERATIONS-------------------------#
# First iteration through assignment
assignEmployeesToWork(employeeBids, openWork)
# Second iteration through assignment
assignEmployeesToWork(employeeBids, openWork)

#if employeesToAssign() != 0:
# find index of work not filled
# start at the end of the list
# if (sen, (date,work) is not in assignments
# assign inverse work 

with open('FinalAssignments.txt', 'w') as out: 
  for index, value in enumerate(assignments): out.write(assignments[index].__str__()+'\n')
