SSDE OVERTIME BID AND ASSIGNMENT MODULE
==========================
This is a simple Python (2.7.16) application intended to provide SSDE business 
automation opportunities for assigning PCO/SUP overtime work.

FEATURES
--------------------------
MAIN.PY
calls init.py and func.oy and runs the main functionality of the application. 
Generates two output files: 1) OT assignments in the order of assignment, 
showing all details within a row and 2) OT assignments grouped by event date and
name, showing only employee names assigned to each work

INIT.PY
takes all the input files and initialzes all corresponding 
data structures and objects to begin the assignment process. Init.py loads the
employee, work, and existing work data into three ordered dictionaries of 
Employee(), Work() and ExistingWork() objects, respectively. It also creates
a list of employee bids, allows additional padding to employee count, and 
generates a new seniority rotation.

FUNC.PY
holds a variety of functions used by main.py and init.py. 
The functionality held in this module includes: 1) rotating the seniority list, 
2) adding additional padding to employee count, 3) validating input for 
seniority rotation start and padding amount, 4) checking existing work and 
2.5hr time overlap, 5) assigning employees through regular passes and inverse, 
and 6) grouping the final assignments for formatted output.

EXAMPLES
--------------------------
Running main.py (with value and range error handling):

	Enter SEN # to begin next rotation: 0
	Values between 1-318 only.

	Enter SEN # to begin next rotation: x
	Integer values only.

	Enter SEN # to begin next rotation: 150

	4-20 EVENT
	SATURDAY 4/20/2019
	900-1800 OR COMP
	-----------------------
	Limit: 50 PCOs. Add padding? (Enter 0-30): 31
	Values between 0-30 only.

	4-20 EVENT
	SATURDAY 4/20/2019
	900-1800 OR COMP
	-----------------------
	Limit: 50 PCOs. Add padding? (Enter 0-30): 0

	Done. Assignments generated.

Raw output will appear as follows:

	SENIORITY BADGE SURNAME FIRST DATE WATCH CODE START END COMP
	199 80 LEE JERRY 4/20/2019 PORT ENFORCEMENT PE 1800 2200	
	205 213 SEIKI JUSTIN 4/20/2019 4-20 EVENT 420 900 1800 COMP
	209 42 HENRY JAIME (J.R.) 4/21/2019 4TH & BRANNAN 4TH 730 1930 COMP
	216 224 SYLVESTER III	HUBERT	4/20/2019 4-20 EVENT 420 900 1800 COMP
	221 65 MACHADO MIGUEL 4/20/2019 4-20 EVENT 420 900 1800 COMP
	234 286 YU JONATHAN 4/20/2019 MISSION CRIT MC 1400 2200	COMP
	237 105 BAXTER TODD 4/21/2019 4TH & BRANNAN 4TH	730 1930 COMP

Formatted output will appear as follows:

	MISSION CRIT
	SATURDAY 4/20/2019
	1400-2200 OR COMP
	-----------------------
	CASTRO, V.
	CHAMBERS, N.
	GYOTOKU, M.
	YU, J.

	PORT ENFORCEMENT
	SATURDAY 4/20/2019
	1800-2200 HRS
	-----------------------
	LEE, J.

	4TH & BRANNAN
	SUNDAY 4/21/2019
	730-1930 OR COMP
	-----------------------
	BAXTER, T.
	HENRY, J.

	CHERRY BLOSSOM FESTIVAL
	SUNDAY 4/21/2019
	1000-1830 HRS
	-----------------------
	ENRIQUEZ, S.
	HENRY, S.
	
	MA, K. (#66) WAS THE LAST PCO ON THESE OT ASSIGNMENTS.
	McDOWELL, A. (#67) IS THE FIRST ELIGIBLE FOR THE NEXT OT ASSIGNMENTS.

DIRECTORIES
--------------------------
- Do not modify files inside path\PyMod\root\employee unless necessary (i.e. to 
add/remove employes or update existing work). For each OT Assignment, replace
Bids.txt and OTWork.txt with new files in path\PyMod\root\input, which contains
employee bids and overtime work postings.
- The path\PyMod\root directory also contains all necessary files to use the 
application: input files, Python scripts, and compiled Python scripts. The final
raw and formatted assignment postings will appear in the path\PyMod\root directly
as well. 
- To test further SUP or PCO OT assignments, replace existing files in
path\PyMod\root\input with SUP Test Data or PCO Test Data.

INPUT
--------------------------
Input must be tab-delimited text files that must be formated as shown in "Input Template.xlsx". The applcation only supports the following input text files names: "OTWork.txt", "Bids.txt", "Employees.txt", and "ExistingWork.txt"

RUNNING THE APPLICATION
--------------------------
Open Python (2.7.16) IDLE Shell and select File > Open > path\PyMod\root\main.py. Once the main.py file is open, select Run > Run Module or F5.
