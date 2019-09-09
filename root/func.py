import classes
import container
import operator
#-----------------------------------------------------------------------------#
def rotate_employees(rotation, n):
  seniority = container.seniority_list_by_rotation
  from_new_start = rotation[seniority.index(n):]
  to_new_start = rotation[:seniority.index(n)]
  # Rotate the initial ordered list around the new starting employee
  rotated_rotation = from_new_start + to_new_start
  # Merge new rotation order with the seniority list to aquire new seniority rotation
  merged_sen_rot = sorted(zip(seniority, rotated_rotation), key=lambda x:x[0])
  new_employee_rotation = []
  for item in merged_sen_rot:
    new_employee_rotation += [item[1]]
  return new_employee_rotation
#-----------------------------------------------------------------------------#
def add_limit_option():
  for work in container.ot_work:
    w = container.ot_work[work]
    # For big events that need 17+ PCOs, padding may be added for INV assignments
    if w.emp_needed >= 17:
      in_str = '\n'+ w.__work_details__() + '\nLimit: ' + str(w.emp_needed) + ' PCOs. Add padding? (Enter 0-30)'
      w.emp_limit = validate(in_str, 0, 30)
#-----------------------------------------------------------------------------#
def validate(in_str, lower, upper):
  while True:
    try:
      n = int(raw_input(in_str + ": "))
      assert lower <= n <= upper
      break
    except ValueError:
      print('Integer values only.')
    except AssertionError:
      print('Values between ' + str(lower)+ '-' + str(upper) + ' only.')
  return n
#-----------------------------------------------------------------------------#
def check_overlapping_work(interval, date, emp):
  # Create a temporary list of currently assigned work
  current = [obj for obj in container.ot_work_assignments if obj.employee == container.employees[emp]]
  # Iterate through all current work assignments
  for index, item in enumerate(current):
    # Get the max start time and min end time between each current assignment and the proposed assignment
    start_maximum = max(int(interval[0]), int(item.work.start_time))
    if not interval[1] and not item.work.end_time:
      end_minimum = start_maximum + 300
    elif not interval[1]:
      end_minimum = int(item.work.end_time)
    elif not item.work.end_time:
      end_minimum = int(interval[1])
    else:
      end_minimum = min(int(interval[1]), int(item.work.end_time))
    # Based on two time intervals, calculate the time range 
    time_range = range(start_maximum, end_minimum)
    # Check if there is a same day overlap of 2.5 hours
    if (len(time_range) < 245) and date == item.work.date:
      return False
  return True
#-----------------------------------------------------------------------------#
def check_existing_work(seniority, work):
  # Find if an employee has existing work
  if seniority in container.existing_work:
    week = container.existing_work[seniority].week_template
    # TRUE if employee has existing work scheduled on the day of proposed work
    # FALSE otherwise
    return bool(int(week[work.day_of_week]))
#-----------------------------------------------------------------------------#
def assign_employees_to_work():
  # Iterate through all employee's choices
  for choice in container.employee_bids:
    for bid in choice[1]:
      # Get one work bid in the list of all bid requests
      otw = container.ot_work[bid[1]]
      work_to_fill = otw.emp_needed > 0
      # choice[0] is Employee Seniority ID
      no_time_overlap = check_overlapping_work([otw.start_time, otw.end_time], otw.date, choice[0])
      if container.existing_work:
        no_existing_work = not(any((obj.employee.seniority, (obj.work.date, obj.work.work_code)) == (choice[0], bid[1]) for obj in container.ot_work_assignments))
      else:
        no_existing_work = True
      if work_to_fill and no_time_overlap and no_existing_work:
        # One less employee needed
        otw.emp_needed -= 1
        # Add an ASSIGNMENT object to the final work assignments list
        container.ot_work_assignments += [classes.Assignment(container.employees[choice[0]], container.ot_work[bid[1]])]
        break
#-----------------------------------------------------------------------------#
def assign_inverse_to_work():
  # Reverse the seniority rotation list to start at the lowest seniority
  sl = list(reversed(container.seniority_list_by_rotation))
  for emp in sl:
    # Iterate through all work
    for choice in container.ot_work:
      # Get one OT work
      otw = container.ot_work[choice]
      if container.existing_work:
        no_existing_work = check_existing_work(emp, otw)
      else:
        no_existing_work = True
      # Employee has not yet been assigned to this work
      emp_work_unique = not (any((obj.employee.seniority, (obj.work.date, obj.work.work_code)) == (emp, (otw.date, otw.work_code)) for obj in container.ot_work_assignments))
      if no_existing_work and emp_work_unique:
        if otw.emp_needed > 0:
          # One less employee needed
          otw.emp_needed -= 1
          container.ot_work_assignments += [classes.Assignment(container.employees[emp], container.ot_work[(otw.date, otw.work_code)])]
          break
        elif otw.emp_needed == 0 and otw.emp_limit > 0:
          # One less employee needed in padding count
          otw.emp_limit -= 1
          container.ot_work_assignments += [classes.Assignment(container.employees[emp], container.ot_work[(otw.date, otw.work_code)])]
          break
#-----------------------------------------------------------------------------#
def group_assignments():
  # Groups final assignments by work date, work event, then seniority
  # container.ot_work_assignments.sort(key=operator.attrgetter('work.date', 'work.work_code', 'employee.seniority'))
  # Groups final assignments by work date, work event, then surname
  container.ot_work_assignments.sort(key=operator.attrgetter('work.date', 'work.work_code', 'employee.surname'))
