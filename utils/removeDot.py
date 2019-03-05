import re
import os

def main():
	location = "/Users/shebin/Documents/CS_839_Data_Science/CS839/stage_1/marked_docs"
	for filename in os.listdir(location):
		fullName = location + "/" + filename
		changeContents(fullName)
#	changeContents("./129.txt")

def changeContents(filename):
	f = open(filename, "r", encoding = "ISO-8859-1")
	contents = f.read()
	f.close()
	words = contents.split(" ")
	for index, word in enumerate(words):
		if re.search("\<person\>Dr\.", word) or re.search("\<person\>Mr\.", word) or re.search("\<person\>Mrs\.", word):
			words[index] = word.replace(".", "")
			#print(word)
	newContents = " ".join(words)
	newFileName = filename.split(".txt")[0] + "_mod.txt"
	f2 = open(newFileName, "w")
	f2.write(newContents)
	f2.close();

if __name__=="__main__":
	main()
