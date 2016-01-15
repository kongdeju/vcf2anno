import sys
import os
def format_vcf(vcf,sample_no):
	out  = sample_no + ".format.vcf"
	os.system("sed -i s/^Chr// %s" % vcf)
	os.system("sed -i s/^chr// %s" % vcf)
	os.system("vcfbreakmulti %s > %s" % (vcf,out))
	lines = open(out,'r').readlines()
	head = []
	vars = []
	for line in lines:
		line = line.strip("\n")
		if line.startswith('#'):
			head.append(line)
		else:
			items = line.split("\t")
			chr = items[0]
			start = items[1]
			id = items[2]
			ref = items[3]
			alle = items[4]
			qual = items[5]
			info = items[6]
			formt = items[7]

if __name__ == "__main__":
	raw_vcf = sys.argv[1]
	sample_no = sys.argv[2]
	break_vcf(raw_vcf,sample_no)	
	
 
