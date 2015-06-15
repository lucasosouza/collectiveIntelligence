# generatefeedvector.py
import feedparser
import re

#Returns title and dictionary of word counts for an RSS feed
def getWordCounts(url):
	# Parse the feed
	page=feedparser.parse(url)
	if 'title' in page.feed: #adjusted to account for blogs out of the described pattern
		wordCount={}

		# Loop over all entries
		for entry in page.entries:
			if 'summary' in entry: summary = entry.summary
			else: summary=entry.description

			# Extract a list of words
			words=getWords(entry.title+' '+summary)
			for word in words:
				wordCount.setdefault(word,0)
				wordCount[word]+=1

		print page.feed.title
		return page.feed.title, wordCount

	return None, None

def getWords(html):
	# Remove all the HTML tags
	txt=re.compile(r'<[^>]+').sub('',html)

	# Split words by all non-alpha characters
	words=re.compile(r'[^A-Z^a-z]+').split(txt)

	# Convert to lowercase
	return [word.lower() for word in words if word]

# Loop through feedlist and get wordcount for each
occurrencesCount={}
wordCounts={}
feedList=[]
for feedurl in file('feedlist.txt'):
	feedList.append(feedurl)
	title, wordCount = getWordCounts(feedurl)
	if title:
		wordCounts[title]=wordCount
		for word, count in wordCount.items():
			occurrencesCount.setdefault(word,0)
			if count > 1:
				occurrencesCount[word]+=1

wordList = []
for word, ocurrences in occurrencesCount.items():
	frac=float(ocurrences)/len(feedList)
	if frac>0.1 and frac<0.5: wordList.append(w)

out = file('blogdata.txt', 'w')
out.write('Blog')
for word in wordList: out.write('\t%s' % word)
out.write('\n')
for blog, wordCount in wordCounts.items():
	#deal with unicode outside the ascii range
	blog = blog.encode('ascii', 'ignore')
	out.write(blog)
	for word in wordList:
		if word in wordCount: out.write('\t%d' % wordCount[word])
		else: out.write('\t0')
	out.write('\n')
