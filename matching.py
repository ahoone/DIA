import sys
import pandas as pd
import numpy as np

from difflib import SequenceMatcher

bucket1 = sys.argv[1]
bucket2 = sys.argv[2]

THRESHOLD = float(sys.argv[6])

df1 = pd.read_csv(bucket1)
df2 = pd.read_csv(bucket2)

total_lines = len(df1) * len(df2)

# We store the result of the matching
# in a matrix, to check if an object
# has matches, or none
match_matrix = np.zeros( ( len(df1),len(df2) ) )
match = 0
df_matches = pd.DataFrame( {
	f"{bucket1}": [],
	f"{bucket2}": [],
	} )

#----------------------#
#------ MATCHING ------#
#----------------------#

print(f"| ( {format(len(df1)*len(df2),',')} 	associations to check ) 	|")

for i,row1 in enumerate(df1.itertuples(index=False)) :
	for j,row2 in enumerate(df2.itertuples(index=False)) :
		print(f"{round(100*(i*len(df2)+j)/total_lines,2)} 	% combinations and {match} 	matches          ", end='\r')
		# Similarity computation
		vector = SequenceMatcher(None, row1._1, row2._1).ratio()
		if vector > THRESHOLD :
			match_matrix[i][j] = 1
			match += 1
			df_matches.loc[len(df_matches)] = [row1._0, row2._0]

#---------------------#
#------ SORTING ------#
#---------------------#

df_matches.to_csv(sys.argv[3], index=False)

if sys.argv[4] != "" :
	row_sums = 			np.sum(match_matrix, axis=1)
	unmatched_csv1 = 	np.where(row_sums == 0)[0]
	df1.loc[unmatched_csv1].to_csv(sys.argv[4], index=False)

if sys.argv[5] != "" :
	column_sums = 		np.sum(match_matrix, axis=0)
	unmatched_csv2 = 	np.where(column_sums == 0)[0]
	df2.loc[unmatched_csv2].to_csv(sys.argv[5], index=False)

print(f"| {match} matches found out of {len(df1)} x {len(df2)} lines   ", end='\r')
print("						|")

sys.exit(0)
















