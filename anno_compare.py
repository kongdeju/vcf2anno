#!/usr/bin/python
import sys
import re

usage = '''
	python anno_compare.py  [join(default)| intersect |filter|head] <file1> <file2>..<filen> -f "column1 [>!=<] value and column2 [>!=<] value and value in column3..or.etc"

'''

def parse_opt():
	items = sys.argv[1:]
	anno_files = []
	commands = ""
	mod = "join"
	if items[0] in ["join","intersect","filter","head"]:
		mod = items[0]
	for item in items:
		if item == "-f":
			break
		elif item == "join" or item == "intersect" or item == "filter" or item == "head":
			continue
		else:
			anno_files.append(item)
	for i in range(len(items)):
		if items[i] ==  "-f":
			commands = items[i+1]
		if items[i] == '-h':
			print usage
			sys.exit()
	return anno_files,commands,mod
		
def print_head(anno_files,mod):
	anno_fp = open(anno_files[0],'r')
	head = anno_fp.readline()
	items= head.strip("\n").split("\t")
	head_lines = "\t".join(items)
	if mod == "filter":
		print head_lines
		return items,[]
	if mod == "head":
		print head_lines
		sys.exit()
	samples = []
	for anno in anno_files:
		prex = anno.split('.')[0] 
		items.append(prex)
		samples.append(prex)
	anno_fp.close()
	head_lines = "\t".join(items)
	print head_lines
	return items,samples
def parse_command(head,command,samples,mod):
	total_command = "1"
	samples_command = ""
	float_ones = []
	if mod == "intersect" :
		for sample in samples:
			key_idx = head.index(sample)
			condition = "'1' in item%s " % key_idx 
			if sample == samples[-1]:
				samples_command = samples_command + condition 
			else:
				samples_command = samples_command + condition + " and "
		total_command = total_command + " and " + samples_command
	if command:
		filt_command = ""
	else:
		return total_command,float_ones
	big_items = re.split('(and|or)',command)
	for i in range(0,len(big_items),2):
		small_item = big_items[i].strip()
		ssmall_items = re.split('\s+',small_item)
		key = ssmall_items[0]
		value = ssmall_items[-1]
		option  = ssmall_items[1]
		try:
			key_idx = head.index(key)
		except:
			key_idx = head.index(value)
		if '>' in option or '<' in option :
			condition = "item%s %s %s" % (key_idx,option,value)	
			float_ones.append(key_idx)
		elif value == "''":
			condition = "item%s %s %s" % (key_idx,option,value)
		else:
			condition = "item%s %s '%s'" % (key_idx,option,value)
		if 'in' in option:
			condition = " '%s' %s item%s" % (key,option,key_idx)
		if i == len(big_items) -1:
			filt_command = filt_command + " " + condition
			break
		else:
			filt_command = filt_command + " " + condition + " " + big_items[i+1]

	total_command = total_command + " and " + filt_command
	return total_command,float_ones

def variant_compare(anno_files,mod):
	variants_anno = {}
	variants_samples = {}
	for anno in anno_files:
		fp = open(anno,'r')
		fp.readline()
		lines = fp.readlines()
		fp.close()
		sample_dict = {}
		for line in lines:
			items = line.strip("\n").split("\t")
			chrome = items[0]
			start = items[1]
			end = items[2]
			ref = items[3]
			alle = items[4]
			vid = chrome + '_' + start + '_' + end + '_' + ref + '_' + alle
			infor = items[5:]
			gt = items[6]
			variants_anno[vid] = infor
			sample_dict[vid] = gt
		variants_samples[anno] = sample_dict
	vars_infor = []
	filter_mod = []
	for var in variants_anno.keys():
		var_infor = []
		gt_list = []
		for anno in anno_files:
			gt = '0/0'
			if var in variants_samples[anno]:
				gt = variants_samples[anno][var]
				if gt:
					gts = re.split('[/|]',gt)
					if gts[0] != gts[-1]:
						tgt = "het" + "_" + gt
					else:
						tgt = "hom" + "_" + gt
					gt_list.append(tgt)
				else:
					gt_list.append("NA_NA")
			else:
				gt_list.append('hom_0/0')
		var_items = var.split("_")
		var_infor.extend(var_items)
		var_infor.extend(variants_anno[var])
		filter_mod.append(var_infor)
		tmp_list = []
		tmp_list.extend(var_infor)
		tmp_list.extend(gt_list)
		vars_infor.append(tmp_list)
	if mod == 'filter':
		return filter_mod
	else:
		return vars_infor
def filt(vars_infor,command,float_ones):
	cmd = ""
	cmd = "for items in vars_infor:\n"
	for i in range(len(vars_infor[0])):
		cmd = cmd +  "\titem%s = items[%s]\n" % (i,i)
	for i in float_ones:
		cmd = cmd + "\ttry:\n"
		cmd = cmd + "\t\titem%s = float(item%s)\n" % (i,i)
		cmd = cmd + "\texcept:\n\t\tcontinue\n"
	cmd = cmd +   "\tif %s :\n" % command
	cmd = cmd + "\t\tprint '\t'.join(items)\n"
#	print cmd
	exec(cmd)

if __name__ == "__main__":
	anno_files,commands,mod = parse_opt()
	head,samples = print_head(anno_files,mod) 
	commands_str,float_list = parse_command(head,commands,samples,mod)
	vars_infor = variant_compare(anno_files,mod)
	filt(vars_infor,commands_str,float_list)
	
