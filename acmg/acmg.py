#pvs1
def tag1(head,var):
	tag = ""
	#conditon 1
	eidx = head.index("ExonicEffect")
	effect = var[eidx]
	if effect.startswith("frameshift") or effect.startswith("nonsynonymous") or effect == "stopgain":
		tag = "PSV1"
	#conditon 2
	ridx = head.index("Region")
	region = var[ridx]
	if region == "splicing":
		tag = "PSV1"
	return tag
#ps1
def tag2(head,var):
	tag = ""
	clinvar_idx = head.index("Clinvar")
	clinvar = var[clinvar_idx]
	cosmic_idx = head.index("Cosmic")
	cosmic = var[cosmic_idx]
	hgmd_idx = head.index("Hgmd")
	hgmd = var[hgmd_idx]
	if cosmic or hgmd or clinvar:
		tag = "PS1"
	return tag
#ps2
def tag3(head,var):
	tag = ""
	return tag
#ps3
def tag4(head,var):
	tag = ""
	return tag
#ps4
def tag5(head,var):
	tag = ""
	return tag
#pm1
def tag6(head,var):
	tag = ""
	return tag
#pm2
def tag7(head,var):
	tag = ""
	popall_idx = head.index("PopAllFreq")
	popall = var[popall_idx]
	esp_idx = head.index("Esp6500Freq")
	esp = var[esp_idx]
	exac_idx = head.index("ExacAllFreq")
	exac = var[exac_idx]
	if esp == '' and popall == '' and exac == '':
		tag = "PM2"
	return tag
#pm3
def tag8(head,var):
	tag = ""
	return tag
#pm4
def tag9(head,var):
	tag = ""
	return tag
#pm5
def tag10(head,var):
	tag = ""
	return tag
#pm6
def tag11(head,var):
	tag = ""
	return tag
#pp1
def tag12(head,var):
	tag = ""
	return tag
#pp2
def tag13(head,var):
	tag = ""
	return tag
#pp3
def tag14(head,var):
	tag = ""
	sift_idx = head.index("SiftClass")
	sift = var[sift_idx]
	if sift == "D":
		tag = "PP3"
		return tag
	mt_idx = head.index("MutationTasteClass")
	mt = var[mt_idx]
	if mt == "D" or mt == "A":
		tag = "PP3"
		return tag
	svm_idx = head.index("MetasvmClass")
	svm = var[svm_idx]
	if svm == "D":
		tag = "PP3"
		return tag
	div_idx = head.index("PolyPhen2hdivClass")
	div = var[div_idx]
	if div == "D":
		tag = "PP3"
		return tag
	hvar_idx = head.index("PolyPhen2hvarClass")
	hvar = var[hvar_idx]
	if hvar == "D":
		tag = "PP3"
		return tag
	return tag
#pp4
def tag15(head,var):
	tag = ""
	return tag
#pp5
def tag16(head,var):
	tag = ""
	return tag
def Float(astr):
	if astr :
		num = float(astr)
	else:
		num = None
#ba1
def tag17(head,var):
	tag = ""
	popall_idx = head.index("PopAllFreq")
	popall = var[popall_idx]
	if Float(popall) > 0.05:
		tag = "BA1"
	esp_idx = head.index("Esp6500Freq")
	esp = var[esp_idx]
	if Float(esp) > 0.05:
		tag = "BA1"
	exac_idx = head.index("ExacAllFreq")
	exac = var[exac_idx]
	if Float(exac) > 0.05:
		tag = "BA1"
	return tag
#bs1
def tag18(head,var):
	tag = ""
	return tag
#bs2
def tag19(head,var):
	tag = ""
	return tag
#bs3
def tag20(head,var):
	tag = ""
	return tag
#bs4
def tag21(head,var):
	tag = ""
	return tag
#bp1
def tag22(head,var):
	tag = ""
	return tag
#bp2
def tag23(head,var):
	tag = ""
	return tag
#bp3
def tag24(head,var):
	tag = ""
	return tag
#bp4
def tag25(head,var):
	tag = ""
	sift_idx = head.index("SiftClass")
	sift = var[sift_idx]
	if sift == "T":
		tag = "BP4"
		return tag
	mt_idx = head.index("MutationTasteClass")
	mt = var[mt_idx]
	if mt == "N" and mt == "P":
		tag = "BP4"
		return tag
	svm_idx = head.index("MetasvmClass")
	svm = var[svm_idx]
	if svm == "T":
		tag = "BP4"
		return tag
	div_idx = head.index("PolyPhen2hdivClass")
	div = var[div_idx]
	if div == "T" :
		tag = "BP4"
		return tag
	hvar_idx = head.index("PolyPhen2hvarClass")
	hvar = var[hvar_idx]
	if hvar == "T":
		tag = "BP4"
		return tag
	return tag
#bp5
def tag26(head,var):
	tag = ""
	return tag
#bp6
def tag27(head,var):
	tag = ""
	return tag
#bp7
def tag28(head,var):
	tag = ""
	eidx = head.index("ExonicEffect")
	effect = var[eidx]
	if effect.startswith("synonymous"):
		tag = "BP7"
	return tag

def tagme(head,var):
	tags = []
	cmdstr = ""
	for i in range(1,29):
		cmdstr = cmdstr + "tag = tag%s(head,var)\n" % i
		cmdstr = cmdstr + "tags.append(tag)\n"
	exec(cmdstr)
	return tags

def ispathogenic(tags):
	level = 0
	nps = 0 
	npm = 0
	npp = 0 
	for item in tags:
		if item.startswith("PS"):
			nps  = nps + 1
	for item in tags:
		if item.startswith("PM"):
			npm = npm + 1
	for item in tags:
		if item.startswith("PP"):
			npp = npp + 1

	#condition i
	if "PSV1" in tags:
		if nps >=1 :
			level = 1
			return level
		if npm >= 2:
			level = 1
			return level
		if npp  >= 2:
			level = 1
			return level
		if npm  >= 1 and npp >= 1:
			level = 1
			return level
	#condition ii
	if nps >= 2:
		level =1
		return level
	#conditon iii
	if nps == 1 :
		if npm >= 3:	
			level = 1
			return level
		if npm >=2 and npp >=2:
			level = 1
			return level
		if npm == 1 and npp >= 4:
			level= 1
			return level
	return level
def islikelypathogenic(tags):
	level = 0
	nps = 0 
	npm = 0
	npp = 0 
	for item in tags:
		if item.startswith("PS"):
			nps  = nps + 1
	for item in tags:
		if item.startswith("PM"):
			npm = npm + 1
	for item in tags:
		if item.startswith("PP"):
			npp = npp + 1
	if "PVS1" in tags and npm == 1:
		level = 1
		return level
	if nps == 1 and (npm == 1 or npm == 2):
		level = 1
		return level
	if nps == 1 and npp >=2:
		level = 1
		return level
	if npm >=3:
		level = 1
		return level
	if npm == 2 and npp >= 2:
		level = 1
		return level
	if npm == 1 and npp >= 4:
		level = 1
		return level
	return level
def isbenign(tags):
	level = 0
	nba = 0
	nbs = 0
	for item in tags:
		if item.startswith("BA"):
			nba = nba + 1
	for item in tags:
		if item.startswith("BS"):
			nbs = nbs + 1
	if nba == 1 or nbs >=2:
		level = 1
		return level
	return level
def islikelybenigh(tags):
	level = 0
	nba = 0
	nbs = 0
	nbp = 0
	for item in tags:
		if item.startswith("BA"):
			nba = nba + 1
	for item in tags:
		if item.startswith("BS"):
			nbs = nbs + 1
	for item in tags:
		if item.startswith("BP"):
			nbp = nbp + 1
	if nbs == 1 and nbp == 1:
		level = 1
		return level
	if nbp >= 2:
		level = 1
		return level
	return level

def classme(tags):
	cls= "Uncertain"
	p = ispathogenic(tags)
	lp = islikelypathogenic(tags)
	b = isbenign(tags)
	lb = islikelybenigh(tags)
	if p == 1 and b != 1 and lb != 1:
		cls = "Pathogenic"
	if lp == 1 and p !=1 and b !=1 and lb != 1:
		cls = "Likely pathogenic"
	if b == 1 and p != 1 and lp != 1:
		cls = "Benign"
	if lb == 1 and b != 1 and p != 1 and lp != 1:
		cls = "Likely benign"
	return cls


def Tag(head,var):
	tags = tagme(head,var)
	label = classme(tags)
	return tags,label

