import pandas as pd
import sys
import os

file = sys.argv[1]

df = pd.read_csv(file)

df = df.groupby('Publication year')

#print(df)

for year, year_df in df:
	#print(f"Group {year}:")
	#print(year_df)

	group_condition = lambda row: 'SIGMOD' if 'SIGMOD' in row['Publication venue'] else 'VLDB'

	year_df['group_condition'] = year_df.apply(group_condition, axis=1)

	grouped_by_condition = year_df.groupby('group_condition')

	for venue, venue_year_df in grouped_by_condition :
		#print(venue_year_df)
		venue_year_df = venue_year_df.drop(columns=venue_year_df.columns[-1])
		os.makedirs(f"{file[:-4]}", exist_ok=True)
		#venue_year_df.dropna().to_csv(f"{file[:-4]}/{venue}-{year}.csv", index=False)
		venue_year_df.to_csv(f"{file[:-4]}/{venue}-{year}.csv", index=False)

sys.exit(0)