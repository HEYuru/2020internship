
def computeNum(filename):
	f = open(filename,'r')
	l = f.readlines()
	s = l[0].split(',')
	print(len(s)/2)
	return 


fname = '../data/add.txt'
computeNum(fname)
print('ok')
