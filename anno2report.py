#!/usr/bin/python
import sys
import dumper
from kongdeju import sorted_list2dict
import MySQLdb
import re
import requests

__author__ = 'D.J Kong'

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
def open_report(sample_no):
	res = requests.post("http://10.44.147.219:5000/%s/report/" % sample_no)
	print res.text



###Get the dict###
file_in = sys.argv[1]
sample_no = sys.argv[2]
#fp = open(file_in,'r')
#lines = fp.readlines()
#dict_out = table2dict(lines)

open_report(sample_no)
conn = MySQLdb.connect(host='rdsikqm8sr3rugdu1muh3.mysql.rds.aliyuncs.com',user='gpo',passwd='btlc123',db='clinic');
cursor = conn.cursor()
'''
###gene----variant####
genes = dict_out['Gene.refGene']
AAchanges = dict_out['AAchange']
effects= dict_out['ExonicFunc.refGene']
sift_degrees = dict_out['sift_degree']
sift_scores = dict_out['sift_score']
gene_variant =[]
AAchange_harmed=[]
Gene_variant=[]
gene_list=[]
for gene,AAchange,effect,sift_degree,sift_score in zip(genes,AAchanges,effects,sift_degrees,sift_scores):
		try:
			AAchange = AAchange.split('.')[1]
		except:
			continue
		if sift_degree == 'D':
			gene_variant.append([gene,effect,AAchange,float(sift_score)])
			gene_list.append(gene)
		Gene_variant.append([gene,AAchange,effect])

gene_variant = sorted(gene_variant,key=lambda x : x[3])
Gene_variant = sorted(Gene_variant,key=lambda x : x[0])
Gene_variant_dict = sorted_list2dict(Gene_variant)
uniq_genes = list(set(gene_list))
###gene---diseases###
sql = 'select gene.gene_name,disease.disease_name,disease.score from gene,disease where  gene.gene_id =disease.gene_id and gene.gene_name in (%s)'
uniq_genes_str = ',' .join(map(lambda x: "%s",uniq_genes))
sql = sql % uniq_genes_str
cursor.execute(sql,uniq_genes)
results = cursor.fetchall()
results = sorted(results,key=lambda x: (x[0],-x[2]))
gene_disease_list=[]
for a,b,c in results:
	gene_disease_list.append([a,[b,c]])
gene_disease_dict = sorted_list2dict(gene_disease_list)
###gene----variant----disease###start###
i=0
N=50
tmp_gene=[]
gene_variant_disease_lines=[]
for gene,effect,AAchange,sift_score in gene_variant:
	if gene in tmp_gene:
		continue
	else:
		try:	
			top3dis=[]
			j=0
			for item in gene_disease_dict[gene]:
				top3dis.append(item[0])
				j=j+1
				if j >=3:
					break
			i=i+1
			if i>N:
				break
			else:	
				top3dis_str = ','.join(top3dis)
				#print AAchange,"\t",sift_score,"\t",gene,"\t",effect,"\t",top3dis_str
				gene_variant_disease_lines.append([sample_no,gene,AAchange,effect,top3dis_str])
				tmp_gene.append(gene)
		except:

			pass
###gene----disease----into----mysql###
sql3 = 'insert into variant_dangerous_report (sample_no,gene,variant,effect,top3deseases) values (%s,%s,%s,%s,%s)'
        ##########check for sample_no########################
sql_select = 'select sample_no from variant_dangerous_report where sample_no = %s' % (sample_no)
sql_delete1 = 'delete from variant_dangerous_report where sample_no = %s' % (sample_no)
sql_delete2 = 'delete from variant_theraby_report where sample_no = %s' % (sample_no)
cursor.execute(sql_select)
results = cursor.fetchone()
if results:
        cursor.execute(sql_delete1)
        cursor.execute(sql_delete2)
        ###########check end###############################
cursor.executemany(sql3,gene_variant_disease_lines)
###gene----variant----disease####end###
Genes = Gene_variant_dict.keys()
###gene----variant----disease---drug####startn###
bin_path = sys.path[0]
drug_file = sys.path[0]+'/gene_drug.txt'
drug_fp = open(drug_file,'r')
tmp_gene=""
i=0
del_pat = re.compile(r'del')
ins_pat = re.compile(r'ins')
####insert into sql ###
sql4 = 'insert into variant_theraby_report (sample_no,gene,variant,variant_func,variant_effect,disease,drug,drug_response,drug_evidence,drug_article) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)'
gvdrug_lines=[]
for line in drug_fp.readlines():
	items = line.strip('\n').split('\t')
	drug_gene = items[0]
	drug_variant = items[1]
	drug_variant_func = items[2]
	drug_variant_effect = items[3]
	drug_disease = items[4]
	drug_response = items[5]
	drug = items[6]
	drug_evidence = items[7]
	drug_pmid = items[8].strip('\r')
	if drug_gene in Genes :
		variants = Gene_variant_dict[drug_gene].keys()
		variants_str = "".join(variants)
		if drug_variant in Gene_variant_dict[drug_gene].keys():
			gvdrug_lines.append([sample_no,drug_gene,drug_variant,drug_variant_func,drug_variant_effect,drug_disease,drug,drug_response,drug_evidence,drug_pmid])
		if drug_variant == 'any' and drug_gene == tmp_gene:
			i = i +1
			try:
				variant= variants[i]
				effect = Gene_variant_dict[drug_gene][variant][0]
				gvdrug_lines.append([sample_no,drug_gene,variant,effect,drug_variant_effect,drug_disease,drug,drug_response,drug_evidence,drug_pmid])
			except:
				gvdrug_lines.append([sample_no,drug_gene,drug_variant,drug_variant_func,drug_variant_effect,drug_disease,drug,drug_response,drug_evidence,drug_pmid])
				continue
		if drug_variant == 'any' and drug_gene != tmp_gene:
			variant=variants[0]
			effect = Gene_variant_dict[drug_gene][variant][0]
			tmp_gene = drug_gene
			i =  0
			#print drug_gene,"\t",variant,"\t",effect
			gvdrug_lines.append([sample_no,drug_gene,variant,effect,drug_variant_effect,drug_disease,drug,drug_response,drug_evidence,drug_pmid])
		if del_pat.search(drug_variant)	and del_pat.search(variants_str):
			#print drug_gene,"\t",drug_variant,"\t",drug_variant_func
			gvdrug_lines.append([sample_no,drug_gene,drug_variant,drug_variant_func,drug_variant_effect,drug_disease,drug,drug_response,drug_evidence,drug_pmid])
		if ins_pat.search(drug_variant)	and ins_pat.search(variants_str):
			#print drug_gene,"\t",drug_variant,"\t",drug_variant_func
			gvdrug_lines.append([sample_no,drug_gene,drug_variant,drug_variant_func,drug_variant_effect,drug_disease,drug,drug_response,drug_evidence,drug_pmid])
cursor.executemany(sql4,gvdrug_lines)
'''
sql3 = "update sample_info set stage=%s where sample_no = %s" % (3,sample_no)
cursor.execute(sql3)
cursor.close()
conn.commit()
conn.close()

