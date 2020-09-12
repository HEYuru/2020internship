from rdflib.plugins.parsers.ntriples import NTriplesParser, Sink

#  parsers data	
class Stream(Sink):
	
	def __init__(self):
		self.data = set()
	
	def triple(self, s, p, o):
		self.data.add((s, p, o))	
	
	def graph(self):
		return self.data		


def DisAimos(graph):
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
	pass
	



stream = Stream()
parser = NTriplesParser(stream) 

# parsers data
with open("../data/en.lhd.core.2015-10.nt","rb") as data:
	parser.parse(data)
	
# garaph(set) is the dataset <s1,p1,o1> <s2,p2,o2>...
graph = stream.graph()	

# Create a dictionary  class1:instant1,instant2,instant3...
classes = {}
c = set()
p = set()
for triple in graph:
	c.add(triple[2])
	p.add(triple[0])
	if triple[2] not in classes:
		classes[triple[2]] = set()
	classes[triple[2]].add(triple[0])

cl = list(c)
print(len(c))
print(len(p))
num = 0
f = open('disAxioms201510.txt','w')
for i in range(len(cl)):
	for j in range(i+1,len(cl)):
		if classes[cl[i]].isdisjoint(classes[cl[j]]):
			f.write(cl[i])
			f.write('   disjoint with  ')
			f.write(cl[j])
			f.write('\n')
			num = 1+num

print(num)			
	

