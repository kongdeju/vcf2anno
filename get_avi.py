import sys
import os

script_path = '/expan/programs/anno_vcf/convert2annovar.pl '
def get_avi(vcf,sample_no):
	prex = vcf.split(".")[0]
	out = sample_no + ".avi"
	os.system("perl %s -format vcf4old %s > %s" % (script_path,vcf,out))
	return out
if __name__ == "__main__":
	vcf = sys.argv[1]
	sample_no = sys.argv[2]
	get_avi(vcf,sample_no)
	

