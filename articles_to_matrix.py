#!/usr/bin/python
import re
import codecs
from math import sqrt

def pearson(v1,v2):
	# simple sums
	sum1 = sum(v1)
	sum2 = sum(v2)
	
	# sums of the squares
	sum1Sq = sum([pow(v,2) for v in v1])
	sum2Sq = sum([pow(v,2) for v in v2])
	
	# sum of the products
	pSum = sum([v1[i] * v2[i] for i in range(len(v1))])
	
	# Calculate r (Pearson score)
	num = pSum - (sum1 * sum2 / len(v1))
	den=sqrt((sum1Sq - pow(sum1,2) / len(v1)) * (sum2Sq-pow(sum2,2)/len(v1)))
	if den ==0: return 0
	
	return 1.0 - num/den
	
	
def kcluster(rows,distance=pearson,k=4):
  # Determine the minimum and maximum values for each point
  ranges=[(min([row[i] for row in rows]),max([row[i] for row in rows])) 
  for i in range(len(rows[0]))]

  # Create k randomly placed centroids
  clusters=[[random.random()*(ranges[i][1]-ranges[i][0])+ranges[i][0] 
  for i in range(len(rows[0]))] for j in range(k)]
  
  lastmatches=None
  for t in range(100):
    print 'Iteration %d' % t
    bestmatches=[[] for i in range(k)]
    
    # Find which centroid is the closest for each row
    for j in range(len(rows)):
      row=rows[j]
      bestmatch=0
      for i in range(k):
        d=distance(clusters[i],row)
        if d<distance(clusters[bestmatch],row): bestmatch=i
      bestmatches[bestmatch].append(j)

    # If the results are the same as last time, this is complete
    if bestmatches==lastmatches: break
    lastmatches=bestmatches
    
    # Move the centroids to the average of their members
    for i in range(k):
      avgs=[0.0]*len(rows[0])
      if len(bestmatches[i])>0:
        for rowid in bestmatches[i]:
          for m in range(len(rows[rowid])):
            avgs[m]+=rows[rowid][m]
        for j in range(len(avgs)):
          avgs[j]/=len(bestmatches[i])
        clusters[i]=avgs
      
  return bestmatches	
  
def readfile(filename):
	lines=[line for line in file(filename)]	
	# first line is the column titles
	colnames = lines[0].strip().split('\t')[1:]
	rownames=[]
	data=[]
	for line in lines[1:]:
		p=line.strip().split('\t')
		# first column in each row is rowname
		rownames.append(p[0])
		# the data for this row is the remainder of the row
		data.append([float(x) for x in p[1:]])
	return rownames, colnames,data

def countwords(txt):
	""" return a dictionary containing the word-frequencies in txt"""
	words = {}

	pattern = re.compile("[a-zA-Z][a-zA-Z0-9]*")	
	for word in pattern.findall(txt):
		words[word.lower()] = words.get(word,0)+1	  
	
	# i'd rather do this in the prior step
	# but i need to be able to eliminate dupes
	# which may or may not be more expensive than
	# going this route.  need to benchmark it.
	for key,word in words.items():
		apcount.setdefault(key,0)
		apcount[key]+=1
	
	return words
		
def readArticles(filename):
	articles = {}
	for line in file(filename):
		id,txt = line.split('\t')
#		print "%s-%s" % (id,txt.strip())
		countedwords=countwords(txt)
		articles[id]=countedwords
	return articles
	
	

def buildWordlist(articles):
	wordlist = []
	stopwords=['a','the','but','of','to','for','who','to','and']
	print 'article length is %s' %len(articles)
	for val in articles.values():
		[wordlist.append(wd) for wd in val.keys() if wd not in wordlist and wd not in stopwords]
	wordlist.sort()
	return wordlist
	
def buildWordlist2(articles):
	wordlist = []
	stopwords = ['a', 'am', 'and', 'are', 'as', 'be', 'but', 'by', 'for', 'hr', 'i', 'if', 'in', 'is', 'must', 'of', 'our', 'the', 'this', 'to', 'who']
	print 'article length is %s' %len(articles)
	
	# I had trouble splitting out the following comprehension so its ugly.  big to-do is to clean
	# this up using comprehensions and not for loops
	for val in articles.values():
		[wordlist.append(wd) for wd in val.keys() if wd not in wordlist and wd not in stopwords and float(apcount[wd])/len(articles)>.04]
	wordlist.sort()
	return wordlist	


def writeMatrix(outputFilename,articles,wordlist):
	out=codecs.open(outputFilename,'wb','utf-8')
	# print the header text
	out.write('docid')
	for word in wordlist: out.write('\t%s' % word)
	out.write('\n')

	# now for each article, print the article id followed
	# by a tab, followed by the word frequencies
	for k,v in articles.iteritems():
		out.write('%s' % k)
		for word in wordlist:
			if word in articles[k]:
				out.write('\t%d' % articles[k][word])

			else:
				out.write('\t0')
			
		out.write('\n')

articleText = 'sample_jo.txt'	
#articleText = 'small_jo.txt'
#articleText = 'articles.txt'	
apcount={}


articles = readArticles(articleText)

wordlist = buildWordlist2(articles)
print "%s words in wordlist" % len(wordlist)
if len(wordlist) <50:
	None
	print wordlist
	#print apcount
	#print articles


	# write the matrix itself
writeMatrix('neilwords.txt',articles,wordlist)

