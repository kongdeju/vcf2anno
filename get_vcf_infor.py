import sys

def get_infors(vcf,sample_no):
	lines = open(vcf,'r').readlines()
	out = sample_no + ".vars.info"
	fpo = open(out,'w')
	head = "\t".join(['Chr','Start','Ref','Alt','Quality','GenoType','GTQuality','Depth','Read1','Read2','VarFreq'])+"\n"
	fpo.write(head)
	for line in lines:
		infors = {}
		line = line.strip("\n")
		if line.startswith("#"):
			continue
		else:
			items = line.split("\t")	
			chr = items[0]
			start = items[1]
			ref = items[3]	
			allele = items[4]
			qual = items[5]	
			keys = items[8].split(":")
			values = items[9].split(":")
			for k,v in zip(keys,values):
				infors[k] = v
			try:
				gt = infors['GT']
			except:
				gt = ""
			try:
				dp = infors["DP"]
			except:
				dp = ""
			try:
				gtq = infors["GQ"]
			except:
				gtq = ""
			try:
				read1 = infors["AD"]
				read1 = read1.split(",")[0]
			except:
				try:
					read1 = infors['RO']
				except:
					read1 = ""
			if dp and read1:
				dps = float(dp)
				read1s = int(read1)
				read2 = str(int(dps-read1s))
				var_freq = str(round(float(read2)/dps,2))
			else:
				read2 = ""
				var_freq = ""
			outline ="\t".join([chr,start,ref,allele,qual,gt,gtq,dp,read1,read2,var_freq]) + "\n"
			fpo.write(outline)
	fpo.close()
	return out		
if __name__ == "__main__":
	vcf = sys.argv[1]
	sample_no = sys.argv[2]
	get_infors(vcf,sample_no)
