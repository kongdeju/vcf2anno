#!/usr/bin/python
import sys
from format_vcf import format_vcf
from get_avi import get_avi
from get_vcf_infor import get_infors
from run_annovar import run_annovar_batch
from format_anno import format_anno
from merge_infor_anno import merge

usage = """
	
	python vcf2out.py -i <vcf> -o <prex> -m <gene|detail> -n <thread>
	
	"""
def parse_opt():
	opts = sys.argv[1:]
	mod = 'detail'
	num = 1
	for item in opts:
		idx = opts.index(item)
		if item == '-i':
			vcf = opts[idx+1]
		if item == '-o':
			out = opts[idx+1]
		if item == '-m':
			mod = opts[idx+1]
		if item == '-t':
			num = opts[idx+1]
			num = int(num)
	if '-i' in opts and '-o' in opts :
		return vcf,out,mod,num
	else:
		print usage 
		sys.exit()

if __name__ == '__main__':
	raw_vcf,sample_no,mod,num = parse_opt()
	vcf   = format_vcf(raw_vcf,sample_no)
	avi   = get_avi(vcf,sample_no)
	vif   = get_infors(vcf,sample_no)
	ano   = run_annovar_batch(avi,mod,sample_no,num)
	ans   = format_anno(ano,sample_no,mod)
	out   = merge(vif,raw_vcf,ans,sample_no)

