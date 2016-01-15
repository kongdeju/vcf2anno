import sys
import os
def format_vcf(vcf,sample_no):
	out  = sample_no + ".format.vcf"
	out2  = sample_no + ".norm.vcf"
	os.system("sed -i s/^Chr// %s" % vcf)
	os.system("sed -i s/^chr// %s" % vcf)
	os.system("vcfbreakmulti %s > %s" % (vcf,out))
	os.system("vt normalize -r /expan/programs/fastq2vcf/hg19/hg19.fa %s -o %s" % (out,out2))
	return out2

if __name__ == "__main__":
	raw_vcf = sys.argv[1]
	sample_no = sys.argv[2]
	format_vcf(raw_vcf,sample_no)	
	
 
