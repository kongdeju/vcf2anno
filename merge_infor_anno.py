import sys
import os
import json
import msgpack

def merge(info,vcf,anno,sno):
	infos = open(info,'r').readlines()
	annos = open(anno,'r').readlines()
	total = []
	of = sno + '.xls'
	offp = open(of,'w')
	ofjson = sno + ".bson"
	ofjsonfp = open(ofjson,'wb')
	for infor,anno in zip(infos,annos):
		tmp = []
		anno_items = anno.strip("\n").split("\t")
		basic = anno_items[:5]
		others = anno_items[5:]
		vars = infor.strip("\n").split("\t")[4:]
		tmp.extend(basic)
		tmp.extend(vars)
		tmp.extend(others)
		total.append(tmp)
		ol =  "\t".join(tmp) + "\n"
		offp.write(ol)
	bins = msgpack.packb(total)
	ofjsonfp.write(bins)
	os.system("ls %s* | grep -v %s | grep -v %s | grep -v %s |  xargs rm -f" % (sno,vcf,ofjson,of))
if __name__ == "__main__":
	merge(sys.argv[1],sys.argv[2],sys.argv[3])
