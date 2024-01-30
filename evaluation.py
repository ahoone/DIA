import pandas as pd
import sys

from tools import *

baseline = sys.argv[1]
matching = sys.argv[2]

len_baseline = count_matches(baseline)
len_matching = count_matches(matching)

# Precision is considered 1
# because the baseline has just done all the calculus
# while the matching on buckets has just done a part of it
# using the same similarity function
# So there cannot be False Positives
# (or they were also identified as False Positives in the baseline)

precision = 1

recall = len_matching / len_baseline

fscore = 2 * (precision*recall) / (precision+recall)

print("+-----------------------------------------------+")
print("| Evaluation :                                  |")
print("| Baseline :                                    |")
print(f"| -> {baseline}         ", end='\r')
print("						|")
print("| Matching file :                               |")
print(f"| -> {matching}         ", end='\r')
print("						|")
print("+-----------------------------------------------+")
print(f"| {len_matching} matches found", end='\r')
print("						|")
print(f"| out of {len_baseline} for this threshold", end='\r')
print("						|")
print("+-----------------------------------------------+")
print(f"| precision = {precision}      ", end='\r')
print("						|")
print(f"| recall = {round(recall,2)}      ", end='\r')
print("						|")
print(f"| fscore = {round(fscore,2)}      ", end='\r')
print("						|")
print("+-----------------------------------------------+")

sys.exit(0)