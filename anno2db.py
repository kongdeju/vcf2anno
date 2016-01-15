import sys
import MySQLdb
import re
from multiprocessing import Pool
pat = re.compile('(.+?)\(')
pat1 = re.compile('(.+?)\,')
inf = sys.argv[1]
fp = open(inf,'r');
variant_lines = []
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
fp_lines = fp.readlines()
out_dict = table2dict(fp_lines)
chr_col = out_dict['Chr']
chr_new = []
for item in chr_col:
	new_item = item.replace('chr','')
	chr_new.append(new_item)
start_col = out_dict['Start']
ref_col = out_dict['Ref']
alt_col = out_dict['Alt']
num = len(chr_col)
try:
	snp138_col = out_dict['snp138']
except:
	snp138_col=[]
	for i in range(num):
		snp138_col.append("")
try:
	g2012_col = out_dict['1000g2014oct_all']
except:
	print "1000g"
	g2012_col=[]
	for i in range(num):
		g2012_col.append("")
try:
	esp6500_col = out_dict['esp6500si_all']
except:
	esp6500_col=[]
	for i in range(num):
		esp6500_col.append("")
try:
	sift_score_col = out_dict['sift_score']
except:
	sift_score_col=[]
	for i in range(num):
		sift_score_col.append("")
try:
	sift_degree_col = out_dict['sift_degree']
except:
	sift_degree_col=[]
	for i in range(num):
		sift_degree_col.append("")
try:
	pp2hdiv_score_col = out_dict['pp2hdiv_score']
except:
	print "pp2hiv_score"
	pp2hdiv_score_col=[]
	for i in range(num):
		pp2hdiv_score_col.append("")
try:
	pp2hdiv_degree_col = out_dict['pp2hdiv_degree']
except:
	pp2hdiv_degree_col=[]
	for i in range(num):
		pp2hdiv_degree_col.append("")
try:
	pp2hvar_score_col = out_dict['pp2hvar_score']
except:
	pp2hvar_score_col=[]
	for i in range(num):
		pp2hvar_score_col.append("")
try:
	pp2hvar_degree_col = out_dict['pp2hvar_degree']
except:
	pp2hvar_degree_col=[]
	for i in range(num):
		pp2hvar_degree_col.append("")
try:
	clinvar_col = out_dict['clinvar_20140929']
except:
	clinvar_col=[]
	for i in range(num):
		clinvar_col.append("")
try:
	cosmic_col = out_dict['cosmic70']
except:
	cosmic_col=[]
	for i in range(num):
		cosmic_col.append("")
for chr,start,ref,alt,snp138,g2012apr_all,esp6500si_all,sift_score,sift_degree,pp2hdiv_score,pp2hdiv_degree,pp2hvar_score,pp2hvar_degree,clinvar_20140929,cosmic70 in zip(chr_new,start_col,ref_col,alt_col,snp138_col,g2012_col,esp6500_col,sift_score_col,sift_degree_col,pp2hdiv_score_col,pp2hdiv_degree_col,pp2hvar_score_col,pp2hvar_degree_col,clinvar_col,cosmic_col):
	variant_id = chr + '_' + start + '_' +ref + '->' + alt
	if sift_score == '':
		sift_score = None
	if g2012apr_all == '':
		g2012apr_all = None
	if esp6500si_all == '':
		esp6500si_all = None
	if sift_score == '':
		sift_score=None
	if pp2hdiv_score == '':
		pp2hdiv_score = None
	if pp2hvar_score == '':
		pp2hvar_score = None
	variant_line = (snp138,g2012apr_all,esp6500si_all,sift_score,sift_degree,pp2hdiv_score,pp2hdiv_degree,pp2hvar_score,pp2hvar_degree,clinvar_20140929,cosmic70,variant_id)
	variant_lines.append(variant_line)
conn = MySQLdb.connect(host='rdsikqm8sr3rugdu1muh3.mysql.rds.aliyuncs.com',user='gpo',passwd='btlc123',db='clinic');
cursor = conn.cursor()
sql2 = "update variant_anno set snp138=%s,1000g2012apr_all=%s,esp6500si_all=%s,sift_score=%s,sift_deleterious_degree=%s,polyphen_hdiv_score=%s,polyphen_hdiv_deleterious_degree=%s,polyphen_hvar_score=%s,polyphen_hvar_deleterious_degree=%s,clinvar_20140929=%s,cosmic70=%s where variant_id=%s"
for item in variant_lines:
	cursor.execute(sql2,item)
conn.commit()
cursor.close()
conn.close()
