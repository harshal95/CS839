import nltk
import re

def getFileContents(filename):
	f = open(filename, "r", encoding = "ISO-8859-1")
	return f.read()

def generateNLTKTags(contents):
	lines = contents.split("\n")
	sentences = []
	for line in lines:
		line_tokens = line.split(".")
		for index, sentence in enumerate(line_tokens):
			line_tokens[index] = sentence.strip()
		sentences = list(filter(None, sentences))
		sentences.extend(line_tokens)
	#print(sentences)
	features = []
	for sentence in sentences:
		tags = getTagsForSentence(sentence)
		words = sentence.split()
		for word in words:
			current_word = word.split()
			current = []
			current.append(word)
			current.append(getValueForTag(word, tags))
			next_word = getNextWordInSentence(word, sentence)
			if next_word:
				current.append(getValueForTag(next_word, tags))
				next_next_word = getNextWordInSentence(next_word, sentence)
				if next_next_word:
					current.append(getValueForTag(next_next_word, tags))
				else:
					current.append(0)
			else:
				current.append(0)
				current.append(0)
			features.append(current)
	print(features)

def getPreviousWordInSentence(word, sentence):
	index = sentence.index(word)
	return sentence[:index].split(" ")[-1]

def getNextWordInSentence(word, sentence):
	index = sentence.index(word) + len(word) + 1
	return sentence[index:].split(" ")[0]

def getTagsForSentence(sentence):
	return nltk.pos_tag(sentence.split())

def getValueForTag(word, tag):
	value_map = {
		'NNP' : 10,
		'NNPS' : 5,
		'NNS' : 5,
		'NN' : 5,
		'VB' : 9,
		'VBD' : 9,
		'VBG' : 9,
		'VBN' : 9,
		'VBP' : 9,
		'VBZ' : 9,
		'RB' : 8,
		'CC' : 7,
		'IN' : 4,
		'POS' : 3,
		'JJ' : 6,
		'JJR' : 6,
		'JJS' : 6,
	}
	for tokens in tag:
		if tokens[0] == word:
			return value_map.get(tokens[1], 0)
	return 0

def main():
	contents = getFileContents("./134_mod.txt")
	generateNLTKTags(contents)

if __name__ == "__main__":
	main()


# Tags:
# NNP - 10
# NNPS - 5
# NNS - 5
# NN - 5
# VB - 9
# VBD - 9
# VBG - 9
# VBN - 9
# VBP - 9
# VBZ - 9
# RB - 8
# CC - 7
# IN - 4
# POS - 3
# JJ - 6
# JJR - 6
# JJS - 6
