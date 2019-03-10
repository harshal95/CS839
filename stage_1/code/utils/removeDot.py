import re
import os

source = "train_markedup_docs"
dest = "cleaned_markedup_docs"
def main():
	
	for filename in os.listdir(source):
		#fullName = location + "/" + filename
		changeContents(filename)

def changeContents(filename): 
	f = open(source + "/" +filename, "r", encoding = "ISO-8859-1")
	contents = f.read()
	f.close()
	words = contents.split(" ")
	for index, word in enumerate(words):
		if re.search("\<person\>Dr\.", word) or re.search("\<person\>Mr\.", word) or re.search("\<person\>Mrs\.", word) or re.search("Jr\.\</person\>", word) or re.search("Sr\.\</person\>", word):
			words[index] = word.replace(".", "")
			#print(word)
	newContents = " ".join(words)
	newFileName = filename.split(".txt")[0] + ".txt"
	f2 = open(dest + "/" + newFileName, "w")
	f2.write(newContents)
	f2.close();

if __name__=="__main__":
	main()
