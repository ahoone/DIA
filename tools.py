import pandas as pd
import os

#-------------------#
#------ Tools ------#
#-------------------#

# Used after the matching process
# to gather matches in one file
def gather(dir_matching, matched) -> None :

	print("+-----------------------------------------------+")
	print("| Gathering in process...                       |")
	print("| CSVs assembled in :                           |")
	print(f"| {dir_matching + '/' + matched}", end='\r')
	print("						|")
	print("+-----------------------------------------------+\n")

	df_gather = []

	for file in os.listdir(dir_matching) :

		if file != matched :

			iterate_df = pd.read_csv(dir_matching + '/' + file)

			if len(df_gather) > 0 :
				iterate_df.columns = df_gather.columns.tolist()
				df_gather = pd.concat( [df_gather,iterate_df] , axis=0, ignore_index=True)
			else :
				df_gather = iterate_df

	df_gather.to_csv(dir_matching + '/' + matched, index=False)

def count_matches(filename_csv) -> int :

	return len(pd.read_csv(filename_csv))