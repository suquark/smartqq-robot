import os,random
def doer(d):
	temp1=str(random.random())
	temp2=str(random.random())
	f=open(temp1,'w')
	f.write(d)
	f.write('\nexit')
	f.close()
	a=os.system('ulimit -t 5;ulimit -v 1000000;ulimit -m 1000000;sh <'+temp1+' >'+temp2+' 2>'+temp2)
        if a!=0:
        	return "ERROR:when running"
	f=open(temp2,'r')
	ans=f.read()
	f.close()
	os.system('rm '+temp1+' '+temp2)
        t = True
	while t:
		if ans.find('\n\n')==-1:
			t = False
		ans=ans.replace('\n\n','\n')
	return ans
