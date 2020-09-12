import rdflib
import json

def loaddata(g):
	gdict = {}
	for i in g:
		s = str(i[0])
		p = str(i[1])
		o = str(i[2])
		if s not in gdict:
			gdict[s] = {}
		gdict[s][p]=o
	return gdict

def getSame(g,s):
	dic_Same = {}
	for i in g:
		if s in i[2]:
			dic_Same[str(i[0])] = str(i[2])
	return dic_Same		

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


def Mapping(g,s):
	dic = {}
	key = set()
	for i in g:
		if s in i[0]:
			if i[0] not in key:
				key.add(i[0])
				dic[i[0]]= ['1','2']
			if 'entity1' in i[1]:
				dic[i[0]][0] = i[2]
			if 'entity2' in i[1]:
				dic[i[0]][1] = i[2]
	mapping = {}
	for i in dic:
		mapping[dic[i][0]]=dic[i][1]
	for j in mapping:
		print(j,mapping[j])
	return mapping


def functionality(g):
	properties = set()
	subject = {}
	valuer = {}
	for triple in g:
		p = triple[1]
		if p not in properties:
			properties.add(p)
			subject[p] = set()
			valuer[p] = []
		subject[p].add(triple[0])
		valuer[p].append(triple[2])
	dic_fun = {}
	for p in properties:
		dic_fun[p] = len(subject[p])/ len(valuer[p])
	
	return dic_fun

def diffFrom(dic1,dic2,mapping,sameas):
	label = 'http://www.w3.org/2000/01/rdf-schema#label'
	key1 = 'http://edas#hasLocation'
	key2 = 'http://ekaw#heldIn'
	key3 = 'http://edas#relatedToEvent'
	key4 = 'http://ekaw#paperPresentedAs'
	key5 = 'http://edas#relatedToPaper'
	key6 = 'http://ekaw#presentationOfPaper'
	#diff_dict = {}
	f = open('./res/edas_ekaw_diff.txt','w')
	for i in dic1:
		#diff_dict[i] = []
		for j in dic2:

			sim = 0
			if label in dic1[i] and label in dic2[j]:
				if dic1[i][label] == dic2[j][label]:
					sim = sim+1
					
			if key1 in dic1[i] and key2 in dic2[j]:
				if dic1[i][key1] in sameas:
					if sameas[dic1[i][key1]] == dic2[j][key2]:
						sim = sim+1
						
			if key3 in dic1[i] and key4 in dic2[j]:
				if dic1[i][key3] in sameas:
					if sameas[dic1[i][key3]] == dic2[j][key4]:
						sim = sim+1
						
			if key5 in dic1[i] and key6 in dic2[j]:
				if dic1[i][key5] in sameas:
					if sameas[dic1[i][key5]] == dic2[j][key6]:
						sim = sim+1			
			if sim == 0:
				#diff_dict[i].append(j)
				s = str(i) + 'diffrent from' +str(j)
				f.write(s+'\n')
	f.close()
	return 


def diff(class1,class2,dic1,dic2,sameas):
	label = 'http://www.w3.org/2000/01/rdf-schema#label'
	key1 = 'http://edas#hasLocation'
	key2 = 'http://ekaw#heldIn'
	key3 = 'http://edas#relatedToEvent'
	key4 = 'http://ekaw#paperPresentedAs'
	key5 = 'http://edas#relatedToPaper'
	key6 = 'http://ekaw#presentationOfPaper'

	f = open('./res/edas_ekaw_disjoint.txt','a')
	num_disjoint = 0
	for x in class1:
		for y in class2:
			num_diff = 0
			for i in class1[x]:
				for j in class2[y]:
					sim = 0
					i = str(i)
					j = str(j)

					if label in str(dic1[i]) and label in str(dic2[j]):
						if dic1[i][label] == dic2[j][label]:
							print(i,' same as ',j)
							sim = sim+1

					if key1 in str(dic1[i]) and key2 in str(dic2[j]):
						if dic1[i][key1] in sameas:
							if sameas[dic1[i][key1]] == dic2[j][key2]:
								sim = sim+1
								print(i,' key1 ',j)

					if key3 in dic1[i] and key4 in dic2[j]:
						if dic1[i][key3] in sameas:
							if sameas[dic1[i][key3]] == dic2[j][key4]:
								sim = sim+1
								print(i,' key3 ',j)

					if key5 in dic1[i] and key6 in dic2[j]:
						if dic1[i][key5] in sameas:
							if sameas[dic1[i][key5]] == dic2[j][key6]:
								sim = sim+1
								print(i, ' key5 ' ,j )

					if sim == 0:
						num_diff = num_diff+1
					else:
						print(i,'same as',j)

			card = len(class1[x]) * len(class2[y])
			print('card: ',card)
			print('num_diff: ',num_diff)
			v = num_diff / card
			print(v)
			if v == 1:
				s = str(x) + '  disjoint with  ' +str(y)
				f.write(s+'\n')
				num_disjoint = num_disjoint+1
				print(num_disjoint,':  ',s)
	f.close()
	return num_disjoint

def test(dic1,dic2):
	key1 = 'http://www.w3.org/2000/01/rdf-schema#label'
	for i in dic1:
		for j in dic2:
			if key1 in dic1[i] and key1 in dic2[j]:
				if dic1[i][key1] == dic2[j][key1]:
					print(i, ' sameAs ',j)

		

def getFileName(s):
	hander = './data/populated_datasets_data_20_'
	tier = '_20.ttl'
	return hander+s+tier

def getSameFileName(s):
	hander = './data/populated_datasets_data_20_alignment_'
	tier = '_20.ttl'
	return hander+s+tier
	
	
if __name__ == '__main__':

	s1 = 'edas'
	s2 = 'ekaw'
	g1name = getFileName(s1)
	g2name = getFileName(s2)

	
	g1 = rdflib.Graph()
	g1.parse(g1name, format='n3')
	#pro_fun1 = functionality(g1)
	class1 = classpart(g1,s1)
	gdic1 = loaddata(g1)
	print('step1 sucess: part ontology1')

	g2 = rdflib.Graph()
	g2.parse(g2name, format='n3')
	#pro_fun2 = functionality(g2)
	class2 = classpart(g2,s2)
	gdic2 = loaddata(g2)
	print('step2 sucess:part ontology2')

	g_sameas_name = getSameFileName(s1)
	g_same = rdflib.Graph()
	g_same.parse(g_sameas_name, format='n3')
	dic_same = getSame(g_same,s2)
	print('step3 sucess:get the sameAs mapping')
	
	g3 = rdflib.Graph()
	mapName = './data/'+s1+'-'+s2+'.edoal'
	g3.parse(mapName)
	s = s1+'-'+s2
	mapping = Mapping(g3,s)
	print('step4 sucess:get the mapping')
	for i in gdic1:
		print(gdic1[i])
		break
	#test(gdic1,gdic2)
	
	#diffdict = diffFrom(gdic1,gdic2,mapping,dic_same)
	#json_str = json.dumps(diffdict,indent = 4)
	#f = open('edas_ekaw_diff.json','w')
	#f.write(json_str)
	#f.close()

	num = diff(class1,class2,gdic1,gdic2,dic_same)
	
	'''
	for i in mapping:
		j = mapping[i]
		if i in pro_fun1 and j in pro_fun2:
			print(i,':',pro_fun1[i])
			print(j,':',pro_fun2[j])
			print('----------------')
	'''


'''
http://edas#hasLocation : 1.0
http://ekaw#heldIn : 1.0

http://edas#relatedToEvent : 1.0
http://ekaw#paperPresentedAs : 1.0

http://edas#relatedToPaper : 1.0
http://ekaw#presentationOfPaper : 1.0
'''
