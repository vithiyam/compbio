import pandas as pd
import os
from statistics import mean,median

def compare(boot,gibb,truth):
	#Temp file names
	file1 = "bootcomp"
	file2 = "gibbscomp"

	tid = {}
	f = open(truth, "r")
	line = f.readline()
	line = f.readline()

	while line:
		parts = line.split("\t")
		tid[parts[0]] = float(parts[1])/2
		line = f.readline()
	f.close()

	bootstrap = {}
	f = open(boot, "r")
	line = f.readline()
	line = f.readline()
	range1 = 0
	range2 = 0
	text_file = open(file1, "w")
	string = 'transcript\ttruth\tmean\tmedian\n'
	text_file.write("%s" % string)
	while line:
		parts = line.split("\t")
		vals = [float(parts[i]) for i in xrange(1, len(parts))]
		if min(vals) <= tid[parts[0]] <= max(vals):
			bootstrap[parts[0]] = True
			range1+=1
		else:
			bootstrap[parts[0]] = False
			range2+=1
		string = parts[0]+'\t'+str(tid[parts[0]])+'\t'+str(mean(vals))+'\t'+str(median(vals))+'\n'
		text_file.write("%s" % string)
		line = f.readline()

	text_file.close()
	f.close()
	print "========================RANGE=========================="
	print "No.of Bootstrap values that contain truth value WITHIN range", range1
	print "No.of Bootstrap values that contain truth value OUT OF range", range2

	sample = {}
	f = open(gibb, "r")
	line = f.readline()
	line = f.readline()
	range1 = 0
	range2 = 0
	text_file = open(file2, "w")
	string = 'transcript\ttruth\tmean\tmedian\n'
	text_file.write("%s" % string)
	while line:
		parts = line.split("\t")
		vals = [float(parts[i]) for i in xrange(1, len(parts))]
		if min(vals) <= tid[parts[0]] <= max(vals):
			sample[parts[0]] = True
			range1+=1
		else:
			sample[parts[0]] = False
			range2+=1
		string = parts[0]+'\t'+str(tid[parts[0]])+'\t'+str(mean(vals))+'\t'+str(median(vals))+'\n'
		text_file.write("%s" % string)
		line = f.readline()

	text_file.close()
	f.close()
	print "\n========================RANGE=========================="
	print "No.of Gibbs values that contain truth value WITHIN range", range1
	print "No.of Gibbs values that contain truth value OUT OF range", range2

	f1 = open(file1, "r")
	f2 = open(file2, "r")
	line1 = f1.readline()
	line1 = f1.readline()
	line2 = f2.readline()
	line2 = f2.readline()
	bmean = 0
	bmedian = 0
	tmean = 0
	gmean = 0
	gmedian = 0
	tmedian = 0
	while line1:
		parts1 = line1.split("\t")
		parts2 = line2.split("\t")
		if abs(float(parts1[2])-float(parts1[1])) < abs(float(parts2[2])-float(parts2[1])):
			bmean+=1
		elif abs(float(parts1[2])-float(parts1[1])) > abs(float(parts2[2])-float(parts2[1])):
			gmean+=1
		else:
			tmean+=1

		if abs(float(parts1[3])-float(parts1[1])) < abs(float(parts2[3])-float(parts2[1])):
			bmedian+=1
		elif abs(float(parts1[3])-float(parts1[1])) > abs(float(parts2[3])-float(parts2[1])):
			gmedian+=1
		else:
			tmedian+=1

		line1 = f1.readline()
		line2 = f2.readline()

	print "\n========================MEAN=========================="
	print "Bootstrap mean values that are closer to TRUTH", bmean
	print "Gibbs mean values that are closer to TRUTH", gmean
	print "Bootstrap-Gibbs mean values that are equal to each other", tmean

	print "\n========================MEDIAN========================"
	print "Bootstrap median values that are closer to TRUTH", bmedian
	print "Gibbs median values that are closer to TRUTH", gmedian
	print "Bootstrap-Gibbs median values that are equal to each other", tmedian

	f1.close()
	f2.close()

	#Removing temp files
	os.remove(file1)
	os.remove(file2)

#Temp file names
boot = "bootstrap.sf"
gibb = "gibbs.sf"
truth= "truth.pro"

lines = open('quant_bootstraps.sf').readlines()
open(boot, 'w').writelines(lines[11:])

lines = open('samples.txt').readlines()
open(gibb, 'w').writelines(lines[1:])

df = pd.read_csv(boot,delimiter='\t')
df = df.transpose()
df.columns = range(1,len(df.columns)+1)
df.reset_index(level=0, inplace=True)
df.rename(columns={'index':'transcript'}, inplace=True)
df.to_csv(boot,sep='\t',index=False)
#print df

df = pd.read_csv(gibb,delimiter='\t',header=None,index_col=None)
lst = range(1,len(df.columns))
lst.insert(0, 'transcript')
df.columns = lst
df.to_csv(gibb,sep='\t',index=False)
#print df

df = pd.read_csv('config.pro',delimiter='\t',header=None,index_col=None)
lst = range(3,len(df.columns)+1)
lst.insert(0, 'transcript')
lst.insert(0, 'x')
df.columns = lst

new = pd.DataFrame()
#new['transcript']=df['transcript']
#new['val']=df['10']
#new.to_csv('comparison2',sep='\t',index=False)
new['transcript']=df['transcript']
new['val']=df.take([9], axis=1)
new.to_csv(truth,sep='\t',index=False)

compare(boot,gibb,truth)

#Removing temp files
os.remove(boot)
os.remove(gibb)
os.remove(truth)