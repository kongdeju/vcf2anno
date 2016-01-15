import sys
raw = sys.argv[1]
for line in open(raw,'r'):
	line = line.strip("\n")
	items = line.split("\t")
	chr = items[0]
	start = items[1]
	ref = items[2]
	allele = items[3]
	info = items[4]
	ref_len = len(ref)
	end = int(start) + ref_len -1
	print "\t".join([chr,start,str(end),ref,allele,info])
