from collections import OrderedDict
import csv
import classes
import container
import func
import os.path
from os import path
#-----------------------------------------------------------------------------#
def initialize_objects():
  # Retrieve current working directory and all input files 
  cwd = os.getcwd()
  WORK = os.path.join(cwd, 'input', 'OTWork.txt')
  BIDS = os.path.join(cwd, 'input', 'Bids.txt')
  EMPLOYEE = os.path.join(cwd, 'employee', 'Employees.txt')
  EXISTING_WORK = os.path.join(cwd, 'employee', 'ExistingWork.txt')
  # Process existing work, if the file is found 
  if path.exists(EXISTING_WORK):
    with open(EXISTING_WORK, 'r') as existing_str:
      existing_reader = csv.reader(existing_str, delimiter='\t')
      next(existing_str)
      for line in existing_reader:
        if not line[0]:
          break
        # line[0] (i.e. SENIORITY) is used as the Existing Work dictionary key
        ref = int(line[0])
        # Each EXISTING WORK object contains information on Seniority Number, Working Days Per Week, and Start Date
        container.existing_work[ref] = classes.ExistingWork(ref, line[1], line[2])

  with open(EMPLOYEE, 'r') as employee_str:
    employee_reader = csv.reader(employee_str, delimiter='\t')
    next(employee_str)
    for line in employee_reader:
      if not line[0]:
        break
      # line[0] (i.e. SENIORITY) is used as the Employee dictionary key
      ref = int(line[0])
      # EMPLOYEE takes Badge ID, Seniority, Surname and First Name
      container.employees[ref] = classes.Employee(line[3], ref, line[1], line[2])
      # Populate rotation list
      container.seniority_list_by_rotation += [ref]
      
  sl = container.seniority_list_by_rotation
  in_str = '\nEnter SEN # to begin next rotation'
  next_employee = func.validate(in_str, 1, len(sl))
  # Rotate the employee list to obtain the new seniority rotation
  new_employee_rotation = func.rotate_employees(list(range(1, len(sl) + 1)), int(next_employee))
  # Reorder Employee list to follow the new seniority rotation
  container.employees = OrderedDict((key, container.employees[key]) for key in new_employee_rotation)

  with open(WORK, 'r') as work_str:
    work_reader = csv.reader(work_str, delimiter='\t')
    next(work_str)
    for line in work_reader:
      if not line[0]:
        break
      # line[0], line[2] (i.e. DATE, CODE) is used as the Work dictionary key
      ref = (line[0], line[2])
      comp = line[5].upper()
      # WORK takes Date of Work, Work Name, Work Code, Start Time, End Time, Comp Status, Number of Employees Needed, and Max Employee Limit
      container.ot_work[ref] = classes.Work(line[0], line[1], line[2], line[3], line[4], comp, int(line[6]))

  # The option to add padding for larger work events
  func.add_limit_option()

  with open(BIDS, 'r') as bids_str:
    # Get a list of all key references to work
    work_keys = list(container.ot_work.keys())
    bids_reader = csv.reader(bids_str, delimiter='\t')
    next(bids_str)
    next(bids_str)
    # Bid_reader is a list of all bids in seniority order 1 to n
    for line in bids_reader:
      if not line[0]:
        break
      temp_bids_container = []
      # Add each bid to the temporary list 
      for index, bid in enumerate(line[3:]):
        if bid: 
          temp_bids_container += [(int(bid), work_keys[index])]
      # If there are bids
      if temp_bids_container: 
        # Sort the bids by employee's preference
        sorted_bid_list = sorted(temp_bids_container, key=lambda x:x[0])
        # Add the ordered bids to the all-encompassing bid list
        container.employee_bids += [(int(line[0]), sorted_bid_list)]

  # Reorded the bids to correspond to the new employee rotation
  reorder_all_bids = []
  for item in new_employee_rotation:
    for bid in container.employee_bids:
      if bid[0] == item:
        reorder_all_bids += [(item, bid[1])]
  container.employee_bids = reorder_all_bids
