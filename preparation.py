import re
import csv
import sys

filepath = sys.argv[1]
total_lines = int(sys.argv[2])
output_file = sys.argv[3]

def extract_data(block) :

	#Check year
	year = r'#t(\d*)'
	blockYear = re.compile(year).findall(block)
	if len(blockYear) != 1 :
		#print("error multi/no year")
		return None
	elif int(blockYear[0]) < 1995 or int(blockYear[0]) > 2004 :
		#print("outdated")
		return None
	else :
		blockYear = int(blockYear[0])
		pass

	#Check venue
	venue = r'#c([ \S]*)'
	blockVenue = re.compile(venue).findall(block)
	if len(blockVenue) == 0 :
		#print("error no venue")
		return None
	elif len(blockVenue) > 1 :
		#Should not happen
		#print("error multi venue")
		#print(block)
		return None
	elif not("VLDB" in blockVenue[0]) and not("SIGMOD" in blockVenue[0]) :
		#print("not vldb/sigmod")
		return None
	else :
		blockVenue = blockVenue[0]
		pass

	#Extract other info
	author = r'#@([ \S]*)'
	title = r'#\*([ \S]*)'
	index = r'#index([ \S]*)'

	blockAuthor = re.compile(author).findall(block)
	blockTitle = re.compile(title).findall(block)
	blockIndex = re.compile(index).findall(block)

	if len(blockAuthor) == 1 :
		blockAuthor = blockAuthor[0]
	elif len(blockAuthor) == 0 :
		blockAuthor = None
	else :
		#print(block)
		pass

	if len(blockTitle) == 1 :
		blockTitle = blockTitle[0]
	elif len(blockTitle) == 0 :
		blockTitle = None
	else :
		#print(block)
		pass

	if len(blockIndex) == 1 :
		blockIndex = blockIndex[0]
	elif len(blockIndex) == 0 :
		blockIndex = None
	else :
		#print(block)
		pass

	return [blockIndex, blockTitle, blockAuthor, blockVenue, blockYear]



def read_large_file(filepath, start_line, end_line, writer) :

	with open(filepath) as infile :
		block = ""
		for i,line in enumerate(infile) :
			if i < start_line :
				pass
			elif i > end_line :
				break
			else :
				if line == "\n" :
					data = extract_data(block)
					if data != None :
						#print(data)
						writer.writerow(data)
					block = ""
				else :
					block += line
			#print(i,"lines treated", end='\r')



def read_file(filepath, writer) :

	# Number of detected objects
	# included ones with missing values
	count = 0

	with open(filepath) as infile :
		block = ""
		for i,line in enumerate(infile) :
			if line == "\n" :
				data = extract_data(block)
				if data != None :
					#print(data)
					writer.writerow(data)
					count += 1
				block = ""
			else :
				block += line
			print(f"| {round(100*i/total_lines,2)}	% lines read ({format(i,',')}/{format(total_lines,',')})	|", end='\r')

	return count
			
def main() :

	#---------------------#
	#------ Parsing ------#
	#---------------------#

	with open(output_file, mode='w', newline='') as file :
		writer = csv.writer(file)
		header = ["Paper ID", "Paper title", "Author names", "Publication venue", "Publication year"]
		writer.writerow(header)
		#read_large_file(filepath,0,2_000_000,writer)
		count = read_file(filepath, writer)

	print(f"{count} objects detected                         ")

	#----------------------#
	#------ Cleaning ------#
	#----------------------#

	# The objective is to remove in a same file
	# entities that are recurrent


main()
sys.exit(0)










