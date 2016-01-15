import kongdeju
import sys
import json
import dumper
import matplotlib
import MySQLdb
matplotlib.use('Agg')
from matplotlib import pylab as plot
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
def Ti_Tv(type_list):
	Ti = ['AG','GA','CT','TC']
	Ti_num = 0
	Tv_num = 0
	for item in type_list:
		if item in Ti:
			Ti_num = Ti_num +1
		else:
			Tv_num = Tv_num +1
	try:
		ratio = float(Ti_num)/float(Tv_num)
	except:
		ratio = 0
	return ratio
fp = open(sys.argv[1],'r')
lines = fp.readlines()
dict_out = table2dict(lines)
#####This is for chrome picture#####
chrome_list =  dict_out['Chr']
chrome_dict = kongdeju.list2dict(chrome_list)
####This is for genomic Ti/Tv#######
refs = dict_out['Ref']
vars = dict_out['Alt']
exotic_type = dict_out['Func.refGene']
genome_type_list = []
exotic_type_list = []
for ref,var,exo in zip(refs,vars,exotic_type):
	type = ref + var
	if not '-' in type:
		genome_type_list.append(type)
		if exo == 'exonic':
			exotic_type_list.append(type)

genome_ti_tv = round(Ti_Tv(genome_type_list),2)
exotic_ti_tv = round(Ti_Tv(exotic_type_list),2)
#### This is for coverage ####
read1 = dict_out['read1']
read2 = dict_out['read2']
coverage = []
for r1,r2 in zip(read1,read2):
	if r1:
		r1 = int(r1)
	else:
		r1 = 0
	if r2:
		r2 = int(r2)
	else:
		r2 = 0
	cov = r1 + r2
	coverage.append(cov)

cov_mean = kongdeju.median(coverage)
cov_mean = round(cov_mean,2)
#####This is for quality ######
try:
	qual = dict_out['quality']
	qnums = len(qual)
	qn = 0
	for item in qual:
		if item:
			item = float(item)
			if item >= 40:
				qn = qn + 1
	q40 = (float(qn)/float(qnums)) * 100
	q40 = round(q40,2)
except:
	q40=0
sample_no = sys.argv[2]
pic1=[genome_ti_tv,exotic_ti_tv,cov_mean,q40]
y,x,z = plot.hist(coverage,50,normed=1,histtype='bar',cumulative=-1,color='Burlywood')
'''
plot.xlabel('SNP depth')
plot.ylabel('Fraction of total SNP')
plot.title('Coverage')
out_fig = sample_no + '_pic2.svg'
plot.savefig(out_fig,format='svg')
'''
zft=[]
vals = []
pic2_data = []
for x1,y1 in zip(x,y):
	x1 = round(x1,2)
	y1 = round(y1,2)
	tmp_dict = {}
	tmp_dict['x'] = x1
	tmp_dict['y'] = y1
	pic2_data.append(tmp_dict)
pic2_dict={}
pic2_dict['x-lable'] = 'SNP depth'
pic2_dict['y-lable'] = 'Fraction of total SNP'
pic2_dict['data'] = pic2_data
zft=[pic2_dict]
pic2_str= json.dumps(zft)

conn = MySQLdb.connect(host='rdsikqm8sr3rugdu1muh3.mysql.rds.aliyuncs.com', port=3306, user='gpo',
                                    passwd='btlc123', db='clinic', charset='utf8')
cursor = conn.cursor()
sql_check = 'select pic1 from variant_data_pic where sample_no = %s' % sample_no
cursor.execute(sql_check)
one_line_got = cursor.fetchone()
if one_line_got:
	pic1_list_already_in = json.loads(one_line_got[0])
	last2items = pic1_list_already_in[-2:]
	pic1_str_update = pic1.extend(last2items)
	pic1_str_update = json.dumps(pic1)
	sql2 = "update variant_data_pic set pic1= '%s', pic2='%s' where sample_no =%d" % (pic1_str_update,pic2_str,int(sample_no))
	cursor.execute(sql2)
else:
	pic1.extend([0,0])
	pic1_str_insert = json.dumps(pic1)
	sql1 = "INSERT INTO variant_data_pic(sample_no,pic1,pic2) VALUES (%d,'%s','%s')" % (int(sample_no),  pic1_str_insert, pic2_str)
	cursor.execute(sql1)
cursor.close()
conn.commit()
conn.close()
#####This is end ##########
