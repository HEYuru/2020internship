def laoddisax(filename):
	with open(filename,'r') as f:
		dis = []
		while True:
			lines = f.readline()
			if not lines:
				break
			l = lines.split()
			couple1 = []
			couple1.append(l[0])
			couple1.append(l[2])
			dis.append(couple1)
			couple2 = []
			couple2.append(l[2])
			couple2.append(l[0])
			dis.append(couple2)
	return dis


def laodsame(filename):
	with open(filename,'r') as f:
		dic = {}
		while True:
			lines = f.readline()
			if not lines:
				break
			l = lines.split()
			dic[l[0]] = l[2]
			dic[l[2]] = l[0]
	return dic

def change(dis1,dis2,mapping):
	newdis = {}
	for i in dis1:
		if i[1] in mapping.keys():
			if i[0] not in newdis.keys():
				newdis[i[0]]=set()
			newdis[i[0]].add(mapping[i[1]])
	for j in dis2:
		if j[0] in mapping.keys():
			newclass = mapping[j[0]]
			if newclass not in newdis.keys():
				newdis[newclass] = set()
			newdis[newclass].add(j[1])
	print(newdis)
			
					

if __name__=='__main__':
	disfile1 = 'data/disax1.txt'
	disfile2 = 'data/disax2.txt'
	disax1 = laoddisax(disfile1)
	disax2 = laoddisax(disfile2)
	mappingfile = "data/mappings.txt"
	mapping = laodsame(mappingfile)
	new = change(disax1,disax2,mapping)

	

