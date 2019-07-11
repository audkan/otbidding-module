Bidding-Mod
==========================
All input text files must be tab-delimited
--------------------------
- pco_otwork.txt contains DATE EVENT CODE START END COMP NUM
- pco_emp_test.txt contains SENIORITY SURNAME FNAME BADGE
- pco_choices.txt contains SEN PREF PREF PREF PREF PREF ...

BUGS
--------------------------
- 185, 187, 189, 263, 268, 302 are extraneous second assignments that do not match Debbie's assignments.
*How does Debbie decide who gets a second assignment or not? What location in rotation does she begin the second iteration? Does it begin  arbitrarily or at the start?*
- 78, 112, 116, 119 are assigned by Debbie but not in the bidding script results. *Job positions are filled, but why are extra positions given out? How to constrain this?*
- 299, 301, 307, 310, 311, 317, 318 are assigned by Debbie but not in the bidding script results. *How to input INV assignments? When does INV order stop?*
- Debbie's assignments are missing 12 PCOs to reach 50 PCO requirement on 4/20 for 420
- 299 should be INV to 4/20 420 but is given 4/21 CP by Python script.
- 23 is given an assignment by Python script, but no Debbie.
