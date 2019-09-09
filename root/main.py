# main.py implements an employee rotation, then processes and assigns OT work.

# Input files must be tab-delimited text files.
# Output file (as a tab-delimited text file) may be saved as an .xlsx or .csv file

# Created by Audrey Kan, June-August 2019

import init
import container
import func

#-----------------------------------------------------------------------------#
init.initialize_objects()
#-----------------------------------------------------------------------------#
# Save container into a short variable name for brevity
a = container.ot_work_assignments
with open('OTAssignmentsRaw.txt', 'w') as out: 
  # Output headers for the final assignments list
  out.write('SENIORITY\tBADGE\tSURNAME\tFIRST\tDATE\tWATCH\tCODE\tSTART\tEND\tCOMP\n')
  # Run through five passes of OT watch assignment
  for i in range(10):
    func.assign_employees_to_work()
  last_assigned = a[len(a)-1]
  # Inverse assignment to fill up remaining watches
  func.assign_inverse_to_work()
  # Output each assignment to a text file
  for index, item in enumerate(a):
    out.write(a[index].__str__()+'\n')
out.close()

# Sort "raw" assignments into groups and display formatted output
func.group_assignments()
with open('OTAssignmentsPost.txt', 'w') as out:
  # Set current work object and output first Work() object as a string
  header = a[0].work
  out.write(a[0].__work__()+'\n')
  for index, item in enumerate(a):
    # If work details are the same, omit work details and output assigned employee
    if a[index].work == header:
      out.write(a[index].__emp__()+'\n')
    # If different work details, print new work details and output assigned employee
    else:
      out.write('\n' + a[index].__work__()+'\n')
      out.write(a[index].__emp__()+'\n')
      # Track current work object
      header = a[index].work
  # Track last assigned to get starting seniority of the next rotation 
  lst = last_assigned.employee
  nxt = container.employees[lst.seniority + 1].__short__()
  # Output to the bottom of the text file 
  out.write('\n' + last_assigned.__emp__() + ' (#' + str(lst.seniority) + ') WAS THE LAST PCO ON THESE OT ASSIGNMENTS.\n')
  out.write(nxt + ' (#' + str(lst.seniority + 1) + ') IS THE FIRST ELIGIBLE FOR THE NEXT OT ASSIGNMENTS.')
out.close()
print("\nDone. Assignments generated.")
#-----------------------------------------------------------------------------#
