import time
import subprocess
import os
import pandas as pd

from tools import *

def matching(THRESHOLD) -> None :

	dir1 = "ACM_1995_2004"
	dir2 = "DBLP_1995_2004"

	ls1 = os.listdir(dir1)
	ls2 = os.listdir(dir2)

	# matching directory
	# and unmatched directories
	dir_matching = "matching"
	os.makedirs(dir_matching, exist_ok = True)
	dir1_unmatched = dir1 + "_unmatched"
	dir2_unmatched = dir2 + "_unmatched"
	os.makedirs(dir1_unmatched, exist_ok = True)
	os.makedirs(dir2_unmatched, exist_ok = True)
	print("+-----------------------------------------------+")
	print("| Directory /matching created.                  |")
	print(f"| Directory /{dir1_unmatched} created. 	|")
	print(f"| Directory /{dir2_unmatched} created. 	|")
	print("+-----------------------------------------------+")

	threshold = str(THRESHOLD)

	start_time = time.time()
	for file1 in ls1 :
		for file2 in ls2 :
			if file1 == file2 :
				print(f"| Matching file {file1}			|")
				input1 = dir1 + '/' + file1
				input2 = dir2 + '/' + file2
				matching_output = dir_matching + '/' + file1 #file1 is equal to file2
				no_match_file1 = dir1_unmatched + '/' + file1
				no_match_file2 = dir2_unmatched + '/' + file2
				extra_args = [input1, input2, matching_output, no_match_file1, no_match_file2, threshold]
				process = subprocess.Popen(['python3', 'matching.py'] + extra_args)
				process.wait()
				process.terminate()
				print("+-----------------------------------------------+")

	print(f"| Matching done in {round(time.time() - start_time,2)} sec			|")
	print("+-----------------------------------------------+\n")

	#-----------------------#
	#------ Gathering ------#
	#-----------------------#

	matched = "matched.csv"
	gather(dir_matching, matched)

	#--------------------------------------------------------------------------------#

	unmatched_csv1 = "unmatched.csv"
	gather(dir1_unmatched, unmatched_csv1)

	#--------------------------------------------------------------------------------#

	unmatched_csv2 = "unmatched.csv"
	gather(dir2_unmatched, unmatched_csv2)

	#------------------------#
	#------ Evaluation ------#
	#------------------------#

	# Check if the corresponding baseline exists
	assert THRESHOLD in [0.5, 0.6, 0.7, 0.8, 0.9],"Err: No baseline found for this threshold."

	baseline = "baseline/baseline_matched_" + threshold + ".csv"
	csv = dir_matching + '/' + matched

	extra_args = [baseline, csv]
	process = subprocess.Popen(['python3', 'evaluation.py'] + extra_args)
	process.wait()
	process.terminate()	




#-------------------------#
#------ Preparation ------#
#-------------------------#

doPreparation = input("\nDo Preparation step ? (Y/N) ")

if doPreparation == "Y" or doPreparation == "y" :

	#------------------------#
	#------ Database 1 ------#
	#------------------------#

	print("+-----------------------------------------------+")
	print("| Preparation databases :                       |")

	database1 =     "../citation-acm-v8.txt"
	number_lines1 = "24_450_330"
	output1 =       "ACM_1995_2004.csv"

	print("+-----------------------------------------------+")
	print("| Database 1 :                                  |")
	extra_args = [database1, number_lines1, output1]

	start_time = time.time()
	process = subprocess.Popen(['python3', 'preparation.py'] + extra_args)
	process.wait()
	process.terminate()

	print(f"| treated in {round(time.time() - start_time,2)} sec				|")
	print("+-----------------------------------------------+")

	#------------------------#
	#------ Database 2 ------#
	#------------------------#

	database2 =     "../dblp.txt"
	number_lines2 = "28_028_156"
	output2 =       "DBLP_1995_2004.csv"

	print("| Database 2 :                                  |")
	extra_args = [database2, number_lines2, output2]

	start_time = time.time()
	process = subprocess.Popen(['python3', 'preparation.py'] + extra_args)
	process.wait()
	process.terminate()

	print(f"| treated in {round(time.time() - start_time,2)} sec				|")
	print("+-----------------------------------------------+")

else :

	print("Preparation step skipped.")



#----------------------#
#------ Blocking ------#
#----------------------#

doBlocking = input("\nDo Blocking step ? (Y/N) ")

if doBlocking == "Y" or doBlocking == "y" :

	csv1 = "ACM_1995_2004.csv"
	csv2 = "DBLP_1995_2004.csv"

	print("+-----------------------------------------------+")
	print("| Blocking --+--> 20 buckets                    |")
	print("|            |                                  |")
	print("|            +-> per each publication year      |")
	print("|            |                                  |")
	print("|            +-> per publication venue category |")
	print("|                (vldb or sigmod)               |")
	print("+-----------------------------------------------+")

	extra_args = [csv1]
	process = subprocess.Popen(['python3', 'blocking.py'] + extra_args)
	process.wait()
	process.terminate()

	print(f"| csv1 divided -> /{csv1[:-4]} 		|")
	print("+-----------------------------------------------+")	

	extra_args = [csv2]
	process = subprocess.Popen(['python3', 'blocking.py'] + extra_args)
	process.wait()
	process.terminate()

	print(f"| csv2 divided -> /{csv2[:-4]} 		|")
	print("+-----------------------------------------------+")	

else :

	print("Blocking step skipped.")



#----------------------#
#------ Baseline ------#
#----------------------#

doBaseline = input("\nCreate Baseline ? (Y/N) ")

if doBaseline == "Y" or doBaseline == "y" :

	threshold = input("threshold : ")
	assert(float(threshold) < 1)
	assert(float(threshold) > 0.1)

	os.makedirs("baseline", exist_ok=True)

	print("+-----------------------------------------------+")
	print("| Directory /baseline created.                  |")

	csv1 = "ACM_1995_2004.csv"
	csv2 = "DBLP_1995_2004.csv"
	baselinefile = "baseline/baseline_matched_" + threshold + ".csv"
	unmatched_csv1 = ""
	unmatched_csv2 = ""
	# unmatched_csv1 = "baseline/" + csv1[:-4] + "_unmatched.csv"
	# unmatched_csv2 = "baseline/" + csv2[:-4] + "_unmatched.csv"
	

	print("+-----------------------------------------------+")
	print("| Baseline :                                    |")
	print("| - look for matches thanks to the paper title  |")
	print(f"| THRESHOLD : {threshold} 				|")
	print("|                                               |")
	print(f"| Output : {baselinefile} 	|")
	print("| unmatched_csv1 :                              |")
	print(f"| {unmatched_csv1}", end='\r')
	print("						|")
	print("| unmatched_csv2 :                              |")
	print(f"| {unmatched_csv2}", end='\r')
	print("						|")
	print("+-----------------------------------------------+")

	extra_args = [csv1, csv2, baselinefile, unmatched_csv1, unmatched_csv2, threshold]
	start_time = time.time()
	process = subprocess.Popen(['python3', 'matching.py'] + extra_args)
	process.wait()
	process.terminate()

	print(f"| baseline time construction : {round(time.time() - start_time,2)} sec 	|")
	print("+-----------------------------------------------+")

else :

	print("Baseline creation skipped.")



#----------------------#
#------ Matching ------#
#----------------------#

doMatching = input("\nDo Matching between buckets ? (Y/N) ")

if doMatching == "Y" or doMatching == "y" :

	#-------------------------#
	#------ Association ------#
	#-------------------------#

	threshold = float(input("threshold : "))
	assert(threshold < 1)
	assert(threshold > 0.1)

	matching(threshold)

else :

	print("Matching on multiple buckets skipped.")



#------------------------#
#------ Clustering ------#
#------------------------#

doClustering = input("\n Do Clustering ? (Y/N) ")

if doClustering == "Y" or doClustering == "y" :

	pass

else :

	print("Clustering step skipped.")













# import pandas as pd

# csv = "baseline/baseline_matched.csv"

# df = pd.read_csv(csv)

# dfs = df.groupby("DBLP_1995_2004.csv")

# for cate, i in dfs :

# 	if len(i) >= 4 :
# 		print(i)












































