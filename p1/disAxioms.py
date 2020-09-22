import numpy as np
import csv
import time
from rdflib.plugins.parsers.ntriples import NTriplesParser, Sink

#  parsers data	
class Stream(Sink):
	
	def __init__(self):
		self.data = set()
	
	def triple(self, s, p, o):
		self.data.add((s, p, o))	
	
	def graph(self):
		return self.data		

# load file
def classPart(filename):
	
	stream = Stream()
	parser = NTriplesParser(stream) 	
	with open(filename,"rb") as data:
		parser.parse(data)
	graph = stream.graph()	# garaph(set) is the dataset <s1,p1,o1> <s2,p2,o2>...
	print('success load')
	
	classes = {}
	c = set()
	p = set()
	for triple in graph:
		c.add(triple[2])
		p.add(triple[0])
		if triple[2] not in classes:
			classes[triple[2]] = set()
		classes[triple[2]].add(triple[0])
	print('the number of classes: ',end='')
	print(len(c))
	print('the number of instances: ',end='')
	print(len(p))
	
	return classes

# discover the disjointness axioms and output
def disAxioms(classes,filename):	
	cl = list(classes.keys())
	dis = {}
	disAxiom = set()
	Inter = set()
	outfile = filename + 'disAxioms.txt'
	f = open(outfile,'w',encoding='utf-8')
	outfile2 = filename + 'dis.csv'
	f2 = open(outfile2,'w',encoding='utf-8',newline='')
	csv_writer = csv.writer(f2)
	
	for i in range(len(cl)):
		for j in range(i+1,len(cl)):
			if cl[i]<cl[j] :
				key = (cl[i],cl[j])
			else:
				key = (cl[j],cl[i])
				
			if len(classes[cl[i]] & classes[cl[j]]) == 0:
				disAxiom.add(key)
				f.write(str(key[0])+'  ')
				f.write('DisjointWith  ')
				f.write(str(key[1])+'\n')
				
			else:
				Inter.add(key)
				dis[key] = classes[cl[i]] & classes[cl[j]]
				l = []
				l.append(key[0])
				l.append(key[1])
				l.append(dis[key])
				csv_writer.writerow(l)
				
	print(len(disAxiom))
	print(len(Inter))
	f.close()
	f2.close()
	'''
	m = [] #dic -> list	
	print(len(disAxiom))
	print(len(Inter))
	for c1,c2 in dis:
		tmp = [c1,c2,dis[(c1,c2)]]
		m.append(tmp)
	
	headers = ['class1','class2','instance']
	outfile = filename+'disAxioms.csv'
	with open(outfile,'w',encoding='utf-8') as f:
		f_csv = csv.writer(f)
		f_csv.writerow(headers)
		f_csv.writerows(m)
	'''		
	return dis,Inter,disAxiom

# discove the disjointness axioms and NOT output	
def DAS(classes):	
	cl = list(classes.keys())
	disAxiom = set()
	inter = {}
	
	for i in range(len(cl)):
		for j in range(i+1,len(cl)):
			if cl[i]<cl[j] :
				key = (cl[i],cl[j])
			else:
				key = (cl[j],cl[i])
				
			if len(classes[cl[i]] & classes[cl[j]]) == 0:
				disAxiom.add(key)
			else:
				inter[key] = classes[cl[i]] & classes[cl[j]]
				
	print(len(disAxiom))
	print(len(inter))				
	return disAxiom,inter
	
# compute instances between two dataset AND output
def diff(old,new):
	delect = {}
	f3 =  open('delect.csv','w',encoding='utf-8',newline='')
	csv_writer = csv.writer(f3)
	for key in old:
		if key in new:
			if not len(old[key].difference(new[key]))==0:
				delect[key] = old[key].difference(new[key]) #old have,new havn't
				l = []
				l.append(key)
				l.append(delect[key])
				csv_writer.writerow(l)
	f3.close()	
	return delect

# compute add disjointness axioms between two old class
def addAxioms(delect,old):
	addAxioms = set()
	for c1,c2 in old:
		if c1 in delect.keys() and len(old[(c1,c2)] & delect[c1]) != 0:
			old[(c1,c2)] =  old[(c1,c2)] - delect[c1]
			if len(old[(c1,c2)])==0:
				addAxioms.add((c1,c2))
				continue
		if c2 in delect.keys() and len(old[(c1,c2)] & delect[c2]) != 0:
			old[(c1,c2)] =  old[(c1,c2)] - delect[c2]
			if len(old[(c1,c2)])==0:
				addAxioms.add((c1,c2))
	return addAxioms

# add the disjointness axioms between the new classes and others
def addDisAxioms(new,dif):
	adddis = set()
	#addinter = {}

	for i in dif:
		for j in new:
			if len(new[i] & new[j])==0:
				if i<j:
					adddis.add((i,j))
				else:
					adddis.add((j,i))
			'''
			else:
				if(i != j ):
					if i<j:
						addinter[(i,j)]= new[i] & new[j]
					else:
						addinter[(j,i)]= new[i] & new[j]
			'''
	print('the number of add axioms: ',end = '')
	print(len(adddis))
	return adddis

# delete the dijointness axioms between the removed classes and others	
def dele(dele,old):
	delete = set()
	for i in dele:
		for j in old:
			if i<j:
				key = (i,j)
			else:
				key = (j,i)	
			delete.add(key)
	print('the number of remove axioms: ',end='')
	print(len(delete))
	return delete


oldf = '../data/instance_types_en_2015.ttl'
st = time.time()
old = classPart(oldf)
print('load and classify running time: ',end='')
print(time.time()-st)
#dis_old,inter_old,disAxiom_old = disAxioms(old,oldf)
dasv1,interv1 = DAS(old)
print('success discover disAxiom')
 
newf = '../data/instance_types_en_201604.ttl'
st = time.time()
new = classPart(newf)
print('load and classify running time: ',end='')
print(time.time()-st)
#dis_new,inter_new,disAxiom_new = disAxioms(new,newf)
st = time.time()
dasv2,interv2 = DAS(new)
print('running time: ',end = '')
print(time.time()-st)
print('scuccess discover disAxiom')


'''
dins = diff(old,new)
addbis = addAxioms(dins,interv1)
'''
stime = time.time()
newclass = new.keys() - old.keys()
add = addDisAxioms(new,newclass)

removeclass = old.keys()-new.keys()
rom = dele(removeclass,old)

"""
there are not put out like a file for disjointness axioms
I wrote a function to output the file
"""

res = ( add | dasv1 )-rom

print('my algo running time: ',end = '')
print(time.time()-stime)
print('output disjointness axioms: ',end = '')
print(len(res))
print('my algo add disjointness axioms: ',end = '')
print(len(res - dasv1))
print('my algo remove disjointness axioms: ',end = '')
print(len(dasv1 - res))


print('-------------------------')
print('same classes: ',end='')
print(len( old.keys() & new.keys() ))
print('same axioms:  ',end='')
print(len(dasv1 & dasv2))

recall = len(res & dasv2) / len(dasv2)
precision = len(res & dasv2) / len(res)
print('recall: ',end='')
print(recall)
print('precision: ',end = '')
print(precision)

print('Effectively added axioms: ',end = '')
ea = (res - dasv1) & ( dasv2 - dasv1 )
print(len(ea))
print('Effectively remove axioms: ',end = '')
er = (dasv1 - res) & ( dasv1 - dasv2 )
print(len(er))

print('dd:',end = '')
print(len(res & dasv2))





