import nltk
from nameparser.parser import HumanName
from pathlib import Path
from os import fdopen, remove
import re
import os



def extract_human_names(source_file):
    text = Path(source_file).read_text()
    tokens = nltk.tokenize.word_tokenize(text)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            #print ("leaf:",leaf[0])
            #print ("break")
            person.append(leaf[0])
        #print ("person_list",person)
        #print ("-------")
        '''
        if len(person) > 1:
            print ("append")
        '''
        for part in person:
            name += part + ' '
            #if name[:-1] not in person_list:
        person_list.append(name[:-1])
        name = ''
        person = []

    return (person_list)


def add_markup(source_file):
    names = extract_human_names('./selected_docs/'+source_file)
    print ("o name:",names)
    names = list(set(names))
    names.sort(key = lambda x:len(x), reverse=True)

    print ("name_list:",names)
    text =''

    temp_dst_path = "./temp_docs/"+source_file
    with open(temp_dst_path,'w') as new_file:
        with open('./selected_docs/'+source_file) as old_file:
            for line in old_file:
                    replace_line = line
                    for name in names:
                        replace_tex ='<person>'+name+'</person>'
                        seacrh_text = name
                        #replace_line = re.sub(r'\b'+seacrh_text+r'\b', replace_tex, replace_line, 1)
                        replace_line = replace_line.replace(seacrh_text,replace_tex)
                        #print (replace_line)
                        #replace_line = replace_line.replace(name,replace_tex)
                    new_file.write(replace_line)


    #this case is to handle <person><person>John</person> Dolittle</person>
    #so remove incorrect markups
    dest_path = "./marked_docs/"+source_file
    with open(dest_path,'w') as new_file:
        with open(temp_dst_path) as old_file:
            for line in old_file:
                    replace_line = line
                    o = line
                    for name in names:
                        replace_tex ='<person>'+name+' '
                        seacrh_text = '<person><person>'+name+'</person>'
                        search_text_2 = '<person>'+name+'</person></person>'
                        replace_tex_2 = name+'</person>'
                        replace_line = replace_line.replace(seacrh_text,replace_tex)
                        replace_line = replace_line.replace(search_text_2,replace_tex_2)
                        #replace_line = re.sub(r'\b'+seacrh_text+r'\b', replace_tex, replace_line, 1)
                        #print (replace_line)
                        #replace_line = replace_line.replace(name,replace_tex)
                    if o != replace_line:
                        print ("new_replace",replace_line)
                    new_file.write(replace_line)


if __name__=="__main__":
  
    src_path = "./selected_docs"
    files = os.listdir(src_path)

    for i, file in enumerate(files):
        add_markup(file)



