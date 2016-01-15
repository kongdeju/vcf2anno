#!/usr/bin/python
import sys
import re
raw_down = sys.argv[1]
pat1 = re.compile("(^\d+)")
pat2 = re.compile("([ATCGatcg]+)")
for line in open(raw_down,'r'):
	line = line.strip("\n")
	items = line.split("\t")
	chr = items[0]
	start = int(items[1])
	ref = items[2]
	ref_len = len(ref)
	end = start + ref_len -1
	alle = items[3]
	freq = items[4]
	rs = items[5]
	mat1 = pat1.match(alle)
	if mat1:
		digit = int(mat1.group())
		mat2 = pat2.search(alle)
		if mat2 :
			alle = mat2.group()
			if digit == 0:
				ref = "-"
		else:
			alle = "-"
				
		print "\t".join([chr,str(start),str(end),ref,alle,freq])			
	else:
		print "\t".join([chr,str(start),str(end),ref,alle,freq])
