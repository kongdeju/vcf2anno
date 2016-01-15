import sys

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
def format_gene(genes):
	new_genes = []
	for gene in genes:
		gene = gene.split(",")[0].split('(')[0]
		new_genes.append(gene)
	return new_genes
def degree(scores,mod):
	degree_col = []
	if mod == "sift":
		for score in scores:
			try:
				if float(score) < 0.01:
					degree_col.append("D")
				else:
					degree_col.append("T")
			except:
				degree_col.append("")
	if mod == "mt":
		probs = []
		for score in scores:
			if score == "":
				probs.append("")
				degree_col.append("")
			else:
				items = score.split("_")
				prob = items[0]
				tag = items[1]
				probs.append(prob)
				degree_col.append(tag)
		return probs,degree_col
	if mod == "metasvm"	:
		for score in scores:
			try:
				if float(score) <= 0:
					degree_col.append("T")
				else:
					degree_col.append("D")
			except:
				degree_col.append("")
		
	if mod == "pp2hdiv"	:
		for score in scores:
			try:
				if float(score) <= 1 and float(score) >= 0.957:
					degree_col.append("D")
				elif float(score) >= 0.453 and float(score) <= 0.596:
					degree_col.append("P")
				else:
					degree_col.append("T")
			except:
				degree_col.append("")
	if mod == "pp2hvar"	:
		for score in scores:
			try:
				if float(score) <= 1 and float(score) >= 0.909:
					degree_col.append("D")
				elif float(score) >= 0.447 and float(score) <= 0.908:
					degree_col.append("P")
				else:
					degree_col.append("T")
			except:
				degree_col.append("")
	return degree_col

def format_change(changes):
	trans = []
	exons = []
	nacs = []
	aacs = []
	for change in changes:
		tmp_trans = []
		tmp_exons = []
		tmp_nacs = []
		tmp_aacs = []
		if change and ":" in change:
			items = change.split(",")
			for item in items:
				iitems = item.split(":")
				if len(iitems) == 2:
					tran = iitems[0]
					nac = iitems[1]
					exon = ""
					aac = "" 
				else :
					tran = iitems[1]
					exon = iitems[2]
					nac = iitems[3]
					try:
						aac = iitems[4]
					except:
						aac = ""
				tmp_trans.append(tran)
				tmp_exons.append(exon)
				tmp_nacs.append(nac)
				tmp_aacs.append(aac)
			transtr = tmp_trans[0]
			exonstr = tmp_exons[0]
			nacstr = tmp_nacs[0]
			aacstr = tmp_aacs[0]
			trans.append(transtr)
			exons.append(exonstr)
			nacs.append(nacstr)
			aacs.append(aacstr)
		else:
			trans.append("")
			exons.append("")
			nacs.append("")
			aacs.append("")
	return trans,exons,nacs,aacs
def vartyper(ref,alt):
	vartype = "snp"
	if ref == "-" or alt == "-" or len(ref) != len(alt):
		vartype = "indel"
	return vartype
def format_gene_anno(out,sn):
	anno_file = sn + '.format.anno'
	fpo = open(anno_file,'w')
	lines = open(out,'r').readlines()
	anno_dict = table2dict(lines)
	chr_col = anno_dict['Chr']
	start_col = anno_dict['Start']
	end_col = anno_dict['End']
	ref_col = anno_dict['Ref']
	alt_col = anno_dict['Alt']
	locus_col = anno_dict['Func.refGene']
	gene_col = anno_dict['Gene.refGene']
	exofunc_col = anno_dict['ExonicFunc.refGene']
	change_col = anno_dict['AAChange.refGene']
	gene_col = format_gene(gene_col)
	trans_col,exon_col,nac_col,aac_col = format_change(change_col)
	head  =['Chr','Start','End','Ref','Alt','Region','Gene','ExonicEffect','Transcripts','Exon','DNAchange','PROchange']
	headstr = "\t".join(head) + "\n"
	fpo.write(headstr)
	for chr,start,end,ref,alt,reg,gene,exoeff,trans,exon,nac,aac in zip(chr_col,start_col,end_col,ref_col,alt_col,locus_col,gene_col,exofunc_col,trans_col,exon_col,nac_col,aac_col):
		lineout =  "\t".join([chr,start,end,ref,alt,reg,gene,exoeff,trans,exon,nac,aac]) + "\n"
		fpo.write(lineout)
	return anno_file
def format_detail_anno(out,sn):
	anno_file = sn + ".format.anno"
	fpo = open(anno_file,'w')
	lines = open(out,'r').readlines()
	anno_dict = table2dict(lines)
	chr_col = anno_dict['Chr']
	start_col = anno_dict['Start']
	end_col = anno_dict['End']
	ref_col = anno_dict['Ref']
	alt_col = anno_dict['Alt']
	locus_col = anno_dict['Func.refGene']
	gene_col = anno_dict['Gene.refGene']
	exofunc_col = anno_dict['ExonicFunc.refGene']
	change_col = anno_dict['AAChange.refGene']
	gene_col = format_gene(gene_col)
	trans_col,exon_col,nac_col,aac_col = format_change(change_col)
	pop_all_col = anno_dict['pop_all']
	dbsnp_col = anno_dict['dbsnp']
	pop_eas_col = anno_dict['pop_eas']
	esp6500_col = anno_dict['esp6500si_all']
	exac_all_col = anno_dict['ExAC_ALL']
	exac_eas_col = anno_dict['ExAC_EAS']
	mt_col = anno_dict['mt']
	mt_probs_col,mt_degree_col = degree(mt_col,'mt')
	sift_score_col = anno_dict['sift']
	sift_degree_col = degree(sift_score_col,'sift')
	svm_col = anno_dict['metasvm']
	svm_degree_col = degree(svm_col,'metasvm')
	pp2hdiv_col = anno_dict['pp2hdiv']
	pp2hdiv_degree_col = degree(pp2hdiv_col,'pp2hdiv')
	pp2hvar_col = anno_dict['pp2hvar']
	pp2hvar_degree_col = degree(pp2hdiv_col,'pp2hvar')
	clinvar_col = anno_dict['clinvar']
	cosmic_col = anno_dict['cosmic']
	hgmd_col = anno_dict['hgmd']
	head  =['Chr','Start','End','Ref','Alt','VarType','Region','DBsnp','Gene','ExonicEffect','Transcripts','Exon','DnaChange','ProChange','PopAllFreq','PopEasFreq','Esp6500Freq','ExacAllFreq','ExacEasFreq','SiftScore','SiftClass','MutationTasteProb','MutationTasteClass','MetasvmScore','MetasvmClass','PolyPhen2hdivScore','PolyPhen2hdivClass','PolyPhen2hvarScore','PolyPhen2hvarClass','Clinvar','Cosmic','Hgmd']
	headstr = "\t".join(head) + "\n"
	fpo.write(headstr)
	for chr,start,end,ref,alt,region,rs,gene,exoeff,tran,exon,nac,aac,pop_all,pop_eas,esp,exac_all,exac_eas,sift_score,sift_degree,mts,mtd,svms,svmd,divs,divd,hvars,hvard,clinvar,cosmic,hgmd in zip(chr_col,start_col,end_col,ref_col,alt_col,locus_col,dbsnp_col,gene_col,exofunc_col,trans_col,exon_col,nac_col,aac_col,pop_all_col,pop_eas_col,esp6500_col,exac_all_col,exac_eas_col,sift_score_col,sift_degree_col,mt_probs_col,mt_degree_col,svm_col,svm_degree_col,pp2hdiv_col,pp2hdiv_degree_col,pp2hvar_col,pp2hvar_degree_col,clinvar_col,cosmic_col,hgmd_col):
		vartype = vartyper(ref,alt)	
		outline = "\t".join([chr,start,end,ref,alt,vartype,region,rs,gene,exoeff,tran,exon,nac,aac,pop_all,pop_eas,esp,exac_all,exac_eas,sift_score,sift_degree,mts,mtd,svms,svmd,divs,divd,hvars,hvard,clinvar,cosmic,hgmd]) + "\n"
		fpo.write(outline)
	fpo.close()
	return anno_file

def format_anno(anno,sno,mod):
	if mod == "gene":
		format_anno = format_gene_anno(anno,sno)
	if mod == "detail":
		format_anno = format_detail_anno(anno,sno)
	return format_anno

if __name__ == "__main__":
	out = format_anno(sys.argv[1],sys.argv[2],'detail')
