"""
main.py is a Python module that implements an employee rotation and PCO work bid assignment.
Employee seniotity, bid preferences, and available work data can be sourced from Trapeze. 
Employee names are arbitrarily generated for test data.

Input files must be tab-delimited text files.
Output file (as a tab-delimited text file) may be opened and saved as an .xlsx or .csv file. 
Output file may be imported into Trapeze. 

Created by Audrey Kan, June-July 2019
"""
#-----------------------------------------------------------------------#
#                               CLASSES
#-----------------------------------------------------------------------#
class Employee():
  # Stores info about a single employee
  def __init__(self, badge, sen, sur='', name=''):
    self._badgeID = badge
    self._seniority = sen
    self._surname = sur
    self._firstName = name
  
  def employeeName(self):
    return self._surname + ', ' + self._firstName[:1]
  
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
    
  def workDetails(self):
    if self._workCode != '': codeStr = ' (' + self._workCode.upper() + ')'
    else: codeStr = ''
    if self._isComp: compStr = ' OR COMP'
    else: compStr = ' HRS'
    if self._endTime == '':
      endStr = ' UNTIL COMP'
      compStr = ''
    else: endStr = '-' + self._endTime
    return self._workName.upper() + ' ' + codeStr + '\n' + self._startTime + endStr + compStr + '\n' + str(self._numEmpNeeded)
  
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
#                             MAIN FUNCTIONS
#-----------------------------------------------------------------------#
def rotateEmployees(senList, rotList, n):
  # Slice list to rotate rotation list
  rotated = rotList[-senList.index(n):] + rotList[:-senList.index(n)]
  # Merges senority list and rotated rotation list
  tempSortedList = sorted(zip(senList, rotated), key=lambda x:x[1])
  newEmployeeRot = []
  # Set new employee rotation according to re-ordered seniority 
  for senRot in tempSortedList:
    newEmployeeRot += [senRot[0]]
  return newEmployeeRot

def overlappingWork(timeInterval, date, emp):
  global assignments
  global employees
  existingWork = [obj for obj in assignments if obj._employee == employees[emp]]
  for idx, val in enumerate(existingWork):
    lowerMax = max(int(timeInterval[0]), int(val._work._startTime))
    upperMin = min(int(timeInterval[1]), int(val._work._endTime))
    if not(len(range(lowerMax, upperMin)) < 245) and date == val._work._date:
      return False
  return True

# Regular assignment iterations through rotated employee list 
def assignEmployeesToWork(employeeBids, openWork):
  global assignments # Read and write to variable in main function
  for choice in employeeBids:
    for bid in choice[1]:
      # If there is work to be filled, no 2.5hr work overlap, and Employee-Work combo does not exist in assignments yet
      if openWork[bid[1]]._numEmpNeeded > 0 and not(any((obj._employee._seniority, (obj._work._date, obj._work._workCode)) == (choice[0], bid[1]) for obj in assignments)):
        if overlappingWork([openWork[bid[1]]._startTime, openWork[bid[1]]._endTime], openWork[bid[1]]._date, choice[0]):
          #Check against existing work 
          # Subtract from work count and assign employee to work
          openWork[bid[1]]._numEmpNeeded -= 1
          assignments += [Assignment(employees[choice[0]], openWork[bid[1]])]
          break

# Inverse assignment iteration through reversed seniority list 
def assignInverse(seniorityList, openWork):
  global assignments  # Read and write to variable in main function
  for emp in seniorityList:
    for choice in openWork:
      # If there is work to be filled and Employee-Work combo does not exist in assignments yet
      if openWork[choice]._numEmpNeeded > 0 and not(any((obj._employee._seniority, (obj._work._date, obj._work._workCode)) == (emp, (openWork[choice]._date, openWork[choice]._workCode)) for obj in assignments)):
        # Subtract from work count and assign employee to work
        openWork[choice]._numEmpNeeded -= 1
        assignments += [Assignment(employees[emp], openWork[(openWork[choice]._date, openWork[choice]._workCode)])]
        break

#-----------------------------------------------------------------------#
#                               MAIN PROGRAM
#-----------------------------------------------------------------------#
from collections import OrderedDict
import csv

employees = OrderedDict() # Holds Employee objects
openWork = OrderedDict() # Holds Work objects
employeeBids = [] # Holds all Employee preferences
seniorityList = [] # Placeholder, tracks rotation
assignments = [] # Holds Employee-Work assignment

#----------------------PROCESS INPUT TXT TILES--------------------------#
'''
empFile = raw_input('Enter EMPLOYEES text file name: ')
workFile = raw_input('Enter WORK text file name: ')
choiceFile = raw_input('Enter BIDS text file name: ')

empFile = 'PCO_emp0402.txt'
workFile = 'PCO_work0402.txt'
choiceFile = 'PCO_bid0402.txt'
'''
empFile = 'SUP_emp0709.txt'
workFile = 'SUP_work0709.txt'
choiceFile = 'SUP_bid0709.txt'

# Initializes Employee objects
with open(empFile, 'r') as employeeStr:
  employee_reader = csv.reader(employeeStr, delimiter='\t')
  for line in employee_reader:
    if line[0] == '':
      break
    # Set SENIORITY as the key
    ref = int(line[0])
    # Set (BADGE, SENIORITY, SURNAME, FIRST) tuple as the value
    employees[ref] = Employee(line[3], ref, line[1], line[2])
    # Add SENIORITY to the placeholder list
    seniorityList += [ref]

# Request employee start index from user
nextEmp = input('Enter SEN # to begin next rotation: ')
# Retrieve new employee rotation 
newEmployeeRotation = rotateEmployees(seniorityList, list(range(1, len(seniorityList) + 1)), nextEmp)
# Reorder employee dictionary according to new employee rotation
employees = OrderedDict((key, employees[key]) for key in newEmployeeRotation)

# Initializes Work objects
with open(workFile, 'r') as workStr:
  work_reader = csv.reader(workStr, delimiter='\t')
  for line in work_reader:
    if line[0] == '':
      break
    # Set (DATE, CODE) tuple as the key
    ref = (line[0], line[2])
    if line[5].upper() == 'YES': comp = True
    else: comp = False
    # Set (DATE, NAME, CODE, START, END, COMP, NUM) tuple as the value
    openWork[ref] = Work(line[0], line[1], line[2], line[3], line[4], comp, int(line[6]))

#Initializes bid preference list
with open(choiceFile, 'r') as choicesStr:
  # Create a placeholder for Work object keys 
  workKeys = list(openWork.keys())
  choice_reader = csv.reader(choicesStr, delimiter='\t')
  for line in choice_reader:
    if line[0] == '':
      break
    choiceList = []
    for count, preference in enumerate(line[1:]):
      # For all declared preferences, add to employee's choice list 
      if preference != '': 
        choiceList += [(int(preference), workKeys[count])]
    # If employee's choice list is not empty, sort preferences in order
    if choiceList != []: 
      choiceList = sorted(choiceList, key=lambda x:x[0])
      # Add to overall employee bid list 
      employeeBids += [(int(line[0]), choiceList)]

# Reorder employee bid list to match the new employee rotation order
tempBidList = []
for pos in newEmployeeRotation:
  tempBidList += [(pos, bid[1]) for bid in employeeBids if bid[0] == pos]
employeeBids = tempBidList

#-------------------------ASSIGNMENT ITERATIONS-------------------------#
with open('FinalAssignments.txt', 'w') as out: 
  # Write column headers to output file
  out.write('SENIORITY\tBADGE\tSURNAME\tFIRST\tDATE\tWATCH\tCODE\tSTART\tEND\tCOMP\n')
  for x in range(5):
    assignEmployeesToWork(employeeBids, openWork) # Five passes through assignments
  assignInverse(list(reversed(seniorityList)), openWork) # Inverse pass through assignments (to fill all remaining work)
  for index, value in enumerate(assignments): 
    out.write(assignments[index].__str__()+'\n')
out.close()
