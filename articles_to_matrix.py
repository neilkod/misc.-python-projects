#!/usr/bin/python
import re
import codecs


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
	stopwords=['a','the','but','of','to','for','who']
	print 'article length is %s' %len(articles)
	for val in articles.values():
		[wordlist.append(wd) for wd in val.keys() if wd not in wordlist and wd not in stopwords]
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

wordlist = buildWordlist(articles)
print "%s words in wordlist" % len(wordlist)
if len(wordlist) <200:
	None
	#print wordlist
	#print apcount




# so now, we have all of the article ids and we have all of the words
# lets build a matrix
writeMatrix('neilwords.txt',articles,wordlist)

	
