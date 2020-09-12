import rdflib
import time
import csv

def classpart(g,s):
	dic = {}
	cla = set()
	for i in g:
		if 'type' in i[1] and s in i[2]:
			if i[2] not in cla:
				cla.add(i[2])
				dic[i[2]]=set()
			dic[i[2]].add(i[0])
	return dic

'''
def CreateQuery(s):
	qhead = 'select ?c where {<'
	qtier = "> <http://www.w3.org/2002/07/owl#sameAs> ?c. filter strstarts( str(?c), 'http://confOf-instances#' )}"
	q = qhead+s+qtier
	return q

def getNewDic(dic):
	newDic = {}
	for i in dic:
		newDic[i] = set()
		for j in dic[i]:
			q = CreateQuery(str(j))
			x = g1.query(q)
			t = str(list(x))
			end = len(t) - 5
			t = (t[22:end])
			newDic[i].add(t)
		print(newDic[i])
	return newDic
'''

def getSame(g,s):
	dic_Same = {}
	for i in g:
		if s in i[2]:
			dic_Same[i[0]] = i[2]
	return dic_Same

def getNewClass(cla,same):
	new_class = {}
	for i in cla:
		new_class[i] = set()
		for j in cla[i]:
			if j in same:
				new_class[i].add(same[j])
	return new_class

def disjoint2onto(dic1,dic2):
	intersec = {}
	jacc = {}
	for i in dic1:
		for j in dic2:
			e11 = len(dic1[i] & dic2[j])
			intersec[(i,j)] = e11
			tmp_jacc = e11 / (len(dic1[i] | dic2[j]))
			jacc[(i,j)]=tmp_jacc
	return intersec,jacc


def getFileName(s):
	hander = './data/populated_datasets_data_20_'
	tier = '_20.ttl'
	return hander+s+tier
	
def getSameFileName(s):
	hander = './data/populated_datasets_data_20_alignment_'
	tier = '_20.ttl'
	return hander+s+tier
	
def saveRes(dic,s1,s2,t):
	outFileName = 'res/'+s1+'_'+s2+'_'+t+'.csv'
	outfile = open(outFileName,'w',newline = '')
	fwriter = csv.writer(outfile)
	for i in dic:
		tmplist = []
		tmplist.append(i[0])
		tmplist.append(i[1])
		tmplist.append(dic[i])
		if tmplist:
			fwriter.writerow(tmplist)
	outfile.close()


def isSub(dic):
	for i in dic:
		for j in dic:
			if dic[j].issubset(dic[i]) and i<j:
				print(j,end='  ')
				print('is subset of',end=' ')
				print(i)


if __name__ == '__main__':
	
	s1 = 'ekaw'
	s2 = 'confOf'
	g1name = getFileName(s1)
	g2name = getFileName(s2)
	g_sameas_name = getSameFileName(s1)
	
	g1 = rdflib.Graph()
	g1.parse(g1name, format='n3')
	
	g2 = rdflib.Graph()
	g2.parse(g2name, format='n3')
	
	g_same = rdflib.Graph()
	g_same.parse(g_sameas_name, format='n3')
	print('load success')
	
	class1 = classpart(g1,s1)
	dic_same = getSame(g_same,s2)
	new_class1 = getNewClass(class1,dic_same)
	
	class2 = classpart(g2,s2)
	intersec,jacc = disjoint2onto(new_class1,class2)
	t1 = 'intersec'
	t2 = 'jacc'
	saveRes(intersec,s1,s2,t1)
	saveRes(jacc,s1,s2,t2)
	print('save success')
	
	#isSub(class1)
	
			
			




	







'''
q = " select ?c where {<http://cmt-instances#topic-496612146> <http://www.w3.org/2002/07/owl#sameAs> ?c . filter strstarts( str(?c), 'con' )}"
x = g1.query(q)
t = list(x)
print(t)
'''
