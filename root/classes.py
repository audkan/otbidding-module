from datetime import datetime
import calendar
#-----------------------------------------------------------------------------#
# Each EMPLOYEE contains information on Badge ID, Seniory Number, Surname and First Name
class Employee():
  def __init__(self, bdg, sen, sur='', fn=''):
    self.badge_id = bdg
    self.seniority = sen
    self.surname = sur
    self.first_name = fn

  # Returns string format of Employee object for abbreviated output
  def __short__(self):
    return self.surname + ', ' + self.first_name[:1] + '.'

  # Returns string format of Employee object for full output
  def __str__(self):
    return (str(self.seniority) + '\t' + str(self.badge_id) 
    + '\t' + self.surname + '\t' + self.first_name)
#-----------------------------------------------------------------------------#
# Each WORK object contains information on Date of Work, Work Name, Work Code, 
# Start Time, End Time, Comp Status, Number of Employees Needed, and Max Employee Limit
class Work():
  def __init__(self, dt, n, co, st, en, ct, nd):
    self.date = dt
    self.work_name = n
    self.work_code = co
    self.start_time = st
    self.end_time = en
    self.is_comp_time = ct
    self.emp_needed = nd
    self.emp_limit = 0
    # Convert MM/DD/YY string into a datetime object
    s = dt.split('/', 2)
    date = datetime(int(s[2]), int(s[0]), int(s[1]))
    # Retrieve day of week index
    self.day_of_week = date.isoweekday()
    if self.day_of_week == 7: 
      self.day_of_week = 0
    # Retrieve day of week string
    self.day_str = (calendar.day_name[date.weekday()]).upper()

  # Returns string format of Work object for formatted output
  def __work_details__(self):
    if self.work_code: 
      codeStr = ' (' + self.work_code.upper() + ')'
    else: 
      codeStr = ''
    if self.is_comp_time: 
      compStr = ' OR COMP'
    else: 
      compStr = ' HRS'
    if not self.end_time:
      endStr = ' UNTIL COMP'
      compStr = ''
    else: 
      endStr = '-' + self.end_time
    return (self.work_name.upper() + '\n' + self.day_str + " " + self.date + '\n'
    + self.start_time + endStr + compStr + '\n-----------------------')
  
  # Returns string format of Work object for full, unformatted output
  def __str__(self):
    return (self.date + '\t' + self.work_name.upper() + '\t' 
    + self.work_code + '\t' + self.start_time + '\t' + self.end_time 
    + '\t' + str(self.is_comp_time))
#-----------------------------------------------------------------------------#
# Each EXISTING WORK object contains information on Seniority Number, 
# Working Days Per Week, and Start Date
class ExistingWork():
  def __init__(self, sen, wt, st):
    self.seniority = sen
    self.week_template = wt
    self.start_date = st

  # Returns string format of Existing Work object for output
  def __str__(self):
    return (str(self.seniority) + '\t' 
    + self.week_template + '\t' + self.start_date)
#-----------------------------------------------------------------------------#
# Each ASSIGNMENT object contains an EMPLOYEE object and a WORK object
class Assignment():
  def __init__(self, emp, wk):
    self.employee = emp
    self.work = wk

  # Returns formatted string of Employee object
  def __emp__(self):
    return self.employee.__short__()

  # Returns formatted string of Work object
  def __work__(self):
    return self.work.__work_details__()

  # Returns string of an Assignment object for unformatted, ungrouped output
  def __str__(self):
    return self.employee.__str__() + '\t' + self.work.__str__()
#-----------------------------------------------------------------------------#
