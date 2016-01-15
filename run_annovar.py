import sys
import os
import glob
from multiprocessing import Pool

annovar_script = '/expan/programs/anno_vcf/annovar/table_annovar.pl'
human_db = '/expan/programs/anno_vcf/annovar/humandb/'

def fast_annovar(avi,sample_no):
	os.system("perl %s %s --remove --outfile %s %s -buildver hg19 -protocol refGene -operation g" % (annovar_script,avi,sample_no,human_db,))
	out = sample_no + ".hg19_multianno.txt"
	return out
def slow_annovar(avi,sample_no):
	os.system(" perl %s %s --remove  -buildver hg19 %s  -protocol refGene,dbsnp,pop_all,pop_eas,esp6500si_all,exac03,mt,sift,pp2hdiv,pp2hvar,metasvm,clinvar,cosmic,hgmd -operation g,f,f,f,f,f,f,f,f,f,f,f,f,f --outfile %s" % (annovar_script,avi,human_db,sample_no))
	out = sample_no + ".hg19_multianno.txt"
	return out
def run_annovar(avi,mod,sample_no):
	if mod == 'gene':
		avo = fast_annovar(avi,sample_no)
	if mod == 'detail':
		avo = slow_annovar(avi,sample_no)
	return avo
def split(avi,sample_no):
	prex = sample_no + "_"
	os.system("split -l 10000 -d -a 3 %s %s" % (avi,prex))
	avis = glob.glob("%s_0*" % sample_no)
	return avis
def merge(avos):
	avos.sort()
	sample_no = avos[0].split(".")[0].split("_")[0]
	head = sample_no + '.anno.head'
	os.system("head -1 %s >%s " % (avos[0],head))
	out = sample_no + ".anno.out"
	for avo in avos:
		os.system("sed -i '1d' %s" % avo)
	avostr = " ".join(avos)
	os.system("cat %s %s > %s" % (head,avostr,out))
	#os.system("ls %s*| grep -v %s | xargs rm -f " % (sample_no,out))
	return out
def run_annovar_batch(avi,mod,sample_no,num=1):
	pools = Pool(num)
	avies = split(avi,sample_no)
	avos = [x.get() for x in [pools.apply_async(run_annovar,(avi,mod,avi)) for avi in avies]]
	out = merge(avos)
	return out

if __name__ == '__main__':
	avi = sys.argv[1]
	sample_no = sys.argv[2]
	run_annovar_batch(avi,'slow',sample_no)
