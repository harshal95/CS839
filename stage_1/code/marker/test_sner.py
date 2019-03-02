'''
from nltk.tag.stanford import NERTagger
st = NERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
print st.tag('You can call me Billiy Bubu and I live in Amsterdam.'.split())
'''
import nltk
#from nltk.tag.stanford import NERTagger
import nltk.tag.stanford as nlt
from pathlib import Path
st = nlt.StanfordNERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')
text = Path("8.txt").read_text()


for sent in nltk.sent_tokenize(text):
    tokens = nltk.tokenize.word_tokenize(sent)
    tags = st.tag(tokens)
    for tag in tags:
        if tag[1]=='PERSON': print (tag)
