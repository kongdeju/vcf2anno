#!/usr/bin/python
import sys
import MySQLdb
import kongdeju
import dumper
import fisher
import gene2pathway
import re
def table2dict(lines):
        colnames = lines[0].strip("\n").split('\t')
        colnums = len(colnames)
        dict_out = {}
        for item in colnames:
                dict_out[item] =[]
        for line in lines[1:]:
                i = 0
                items = line.strip('\n').split('\t')
                for item in items:
                        dict_out[colnames[i]].append(item)
                        i = i + 1
        return dict_out
def real_gene(genes):
	pat = re.compile('(.+?)\(|(.+?)\,')	
	new_genes = []
	for line in genes:
		mat = pat.search(line)
		if mat:
			if mat.group(1):
				gene = mat.group(1)
				new_genes.append(gene)
			else:
				gene = mat.group(2)
				new_genes.append(gene)
		else:
			if line:
				new_genes.append(line)
	return new_genes

fp = open(sys.argv[1],'r')
sample_no = sys.argv[2]
lines = fp.readlines()
dict_out = table2dict(lines)
genes = dict_out['Gene.refGene']
genes = real_gene(genes)
exo_type = dict_out['Func.refGene']
###sample_vairant_num######
genome_variant_num = len(exo_type)
exo_dict = kongdeju.list2dict(exo_type)
try:
	exo_variant_num = exo_dict['exonic']
except:
	exo_variant_num = 0
genes_num = len((set(genes)))
genes=list(set(genes))
#############get from mysql###################
conn = MySQLdb.connect(host='rdsikqm8sr3rugdu1muh3.mysql.rds.aliyuncs.com',user='gpo',passwd='btlc123',db='clinic')
cursor = conn.cursor()
try:
	pathway_dict = gene2pathway.gene2pathway(genes)
	paths=[]
	for a,aitems in pathway_dict.items():
		for b ,bitems in aitems.items():
			paths.extend(bitems.keys())
	paths_num = len(paths)
except:
	paths_num=0
sql3_insert = "insert into variant_data_nums (sample_no,genome_variant,exonic_variant,genes,pathways) values (%s,%s,%s,%s,%s)" % (sample_no,genome_variant_num,exo_variant_num,genes_num,paths_num)
sql3_update = "update variant_data_nums set genome_variant=%s,exonic_variant=%s,genes=%s,pathways=%s where sample_no = %s" % (genome_variant_num,exo_variant_num,genes_num,paths_num,sample_no)
try:
	cursor.execute(sql3_insert)
except:
	cursor.execute(sql3_update)
cursor.close()
conn.commit()
conn.close()
