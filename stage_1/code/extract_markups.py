import os
import csv
import codecs
import nltk
from nltk.tokenize import sent_tokenize

#get list of files inside a folder
def getFiles(folder_path):
    return os.listdir(folder_path)

#temp function to clean n-gram list..can implement if needed
def cleanCurGrams(cur_gram_list):

    '''

    # remove leading and trailing characters of first and last word in n-gram
    cur_gram_list[0] = cur_gram_list[0].replace(".", "")
    cur_gram_list[-1] = cur_gram_list[-1].replace(".", "")

    '''
    return cur_gram_list

#function to remove leading and trailing garbage characters from string
def cleanString(input_string):
    input_string = input_string.replace(";","")

    input_string = input_string.strip("?().,:\"")
    return input_string

#feature that returns num of words in the list
def getNumWords(cur_gram_list):
    return len(cur_gram_list)

#feature that returns if all words in example start with capital letter
def isStartingCapital(cur_gram_list):
    for cur_gram in cur_gram_list:
        if(len(cur_gram) == 0):
            return 0
        if(cur_gram[0].islower()):
            return 0

    return 1


#feature that returns num of words starting with capital letter in current gram
def numStartingCapitals(cur_gram_list):
    count = 0
    for cur_gram in cur_gram_list:
        if(len(cur_gram) == 0):
            continue
        if(cur_gram[0].isupper()):
            count = count + 1
    return count

#feature that returns if string starts with a prefix
def hasPrefix(cur_gram_string, prefix):
    if(cur_gram_string.lower().startswith(prefix.lower())):
        return 1
    else:
        return 0

#feature that returns if string ends with a suffix
def hasSuffix(cur_gram_string, suffix):
    if(cur_gram_string.lower().endswith(suffix.lower())):
        return 1
    else:
        return 0

def containsStrayCharacters(cur_gram_string):
    input_string = cur_gram_string
    if(len(cur_gram_string) >= 2):
        apostrophe = "'s"
        if(apostrophe in cur_gram_string[-2:]):
            input_string = cur_gram_string[:-2]

    stray_chars =[':','\'', '-','\"',',','(',')','%']

    for stray_char in stray_chars:
        if stray_char in input_string:
            return 1

    return 0

#function to check if two words match
def checkWordMatch(cur_gram_string, candidate_string):
    if(cur_gram_string.lower() == candidate_string.lower()):
        return 1
    else:
        return 0

#function to add features corresponding to adjacent words of an n-gram string
def addAdjacentWordFeatures(feature_row, adjacent_word, position, candidate_adj_words):

    for candidate_word in candidate_adj_words:
        if(checkWordMatch(adjacent_word, candidate_word)):
            feature_row[position+"_"+candidate_word] = 1
        else:
            feature_row[position+"_"+candidate_word] = 0

def addTrailingWordFeatures(feature_row, cur_gram_string, suffixes):

    for suffix in suffixes:
        if(hasSuffix(cur_gram_string, suffix) == 1):
            feature_row["suff_"+suffix] = 1
        else:
            feature_row["suff_"+suffix] = 0

def addLeadingWordFeatures(feature_row, cur_gram_string, prefixes):

    for prefix in prefixes:
        if(hasPrefix(cur_gram_string, prefix) == 1):
            feature_row["pref_"+prefix] = 1
        else:
            feature_row["pref_"+prefix] = 0

def getTagsForSentence(sentence):
	return nltk.pos_tag(sentence.split())


def getValueForTag(word, tag, pos_flag):

    value_map = {
        'NNP' : 10,
        'NNPS' : 5,
        'WP' : 5,
        'NNS' : 5,
        'NN' : 5,
        'VB' : 9,
        'VBD' : 9,
        'VBG' : 9,
        'VBN' : 9,
        'VBP' : 9,
        'VBZ' : 9,
        'MD' : 9,
        'RB' : 8,
        'RBR' : 8,
        'RBS' : 8,
        'RP' : 8,
        'WRB' : 8,
        'CC' : 7,
        'IN' : 4,
        'UH' : 4,
        'POS' : 3,
        'JJ' : 6,
        'JJR' : 6,
        'JJS' : 6,
        'CD' : 2,
        'DT' : 1,
        'WDT' : 1,
        'PDT' : 1
    }
    for tokens in tag:

        if word in tokens[0]:
            if tokens[1] == 'NNP' and pos_flag == 1:
                return 0
            return value_map.get(tokens[1], 0)
    return 0

def cleanSentence(sentence):
    sentence = sentence.replace('<person>', '')
    sentence = sentence.replace('</person>', '')
    return sentence

def isWordAllCaps(curr_words):
    for word in curr_words:
        if not word.isupper():
            return 0
    return 1

def containsCaps(curr_words):
    for word in curr_words:
        if word.isupper():
            return 1
    return 0

def startWithRelation(curr_word):
    relation_word_list = ["father", "mother", "brother", "general", "president", "vice", "secretary", "detective", "governor", "god", "first", "lord", "cinematographer", "director", "lady", "major", "captain", "miss", "st", "senator", "lt", "dad", "congressman", "sir", "fbi", "gov", "writer/director", "screenwriter", "constable", "prime", "minister", "saint", "secret", "service", "agent", "mafia", "writer", "member"]
    input_word = curr_word.lower()
    if(input_word in relation_word_list):
        return 1
    return 0

def containsArticles(cur_gram_list):
    articles=["a", "an", "the"]
    for cur_gram in cur_gram_list:
        input_word = cur_gram.lower()
        if(input_word in articles):
            return 1
    return 0

def containsPronouns(cur_gram_list):
    pronouns = ["i", "we", "my", "you", "it's", "he", "she", "she's", "he's", "co", "that", "what", "whatever" ,"whatsoever", "which", "who", "whom","whosoever"]
    for cur_gram in cur_gram_list:
        input_word = cur_gram.lower()
        if(input_word in pronouns):
            return 1
    return 0

def containsPrepositions(cur_gram_list, tags, pos_flag):
    for cur_gram in cur_gram_list:
        tag_val = getValueForTag(cur_gram, tags, pos_flag)
        if(tag_val == 4 or tag_val == 7):
            return 1
    return 0



def containsVerb(cur_gram_list, tags, pos_flag):
    '''
    verbs = ["go", "die", "is", "get", "will", "come"]
    for cur_gram in cur_gram_list:
        input_word = cur_gram.lower()
        if(input_word in verbs):
            return 1
    return 0
    '''


    for cur_gram in cur_gram_list:
        tag_val = getValueForTag(cur_gram, tags, pos_flag)
        if(tag_val == 9):
            return 1
    return 0

def containsAdjective(cur_gram_list, tags, pos_flag):
    for cur_gram in cur_gram_list:
        tag_val = getValueForTag(cur_gram, tags, pos_flag)
        if(tag_val == 6):
            return 1
    return 0

def containsAdverb(cur_gram_list, tags, pos_flag):
    for cur_gram in cur_gram_list:
        tag_val = getValueForTag(cur_gram, tags, pos_flag)
        if(tag_val == 8):
            return 1
    return 0

def isLanguage(cur_gram_string):
    languages = ["English", "Spanish", "Italian", "Roman", "Hasidics","Jews", "Viennese", "Kurdish", "Farsi", "Hispanic", "Hebrew", "Latin", "Irish", "Catholic", "Paraguayan", "Kafkaesque", "Sikhs", "Punjabi"]

    for language in languages:
        if(language in cur_gram_string):
            return 1
    return 0

def isStopWord(cur_gram_string):
    stop_words = ["Arizona","England", "North","Northern","West","Western","East","Eastern","South","Southern","Ireland", "France","New","York", "Paris", "Eldorado", "California", "Paraguay", "Coast", "Broadway", "Disney", "Tehran","America","Europe", "Southeast", "Chicago", "Silicon Valley", "Ohio", "Gibraltar","Nantucket Island","Australia","Los Angeles","England", "Texas", "Iceland", "Alps", "Manchester", "World", "Oz", "Jersey", "Nevada", "Sydney", "Rushmore", "Spain", "Vietnam", "Washington", "Tbilisi", "Georgia", "Kentucky", "Rock", "Town", "City", "Elks Club", "Central Park", "Plaza Motel", "High", "School", "Grand Central Station", "Hollywood", "Parliament", "Iraq", "Anschluss", "Assisi", "States", "United", "San","Jose","Las","Vegas","London", "Notting Hill", "Okay", "Let's","This", "Oscar", "Academy Award", "Yes", "Seen", "Supposedly", "Between", "Most", "Now", "What's","Nothing","Here's", "Life", "Jr", "Hell", "God","Dad","Written","That", "Today", "Full", "Beauty", "Please", "But","IQ","Plaza", "Motel","Fax","Email","Christmas","Hong Kong","Greenish Village","Will","Just","Ah","If","Get","Oh","Great","Amazing", "Guess", "Die","Generally","Trust","Imagine","Yeah","Yet","Halloween","Mine","There","Better","March","Mild","Plump","Drunken","April","Instead","Plus","Love","Go","Bible","Money", "Online","Web","Chicken","Me","Short","Big","Fear", "Best", "Sad","Come","Down","Rule","Single","Is","Man","No", "Typical","All"]
    for stop_word in stop_words:
        if(stop_word in cur_gram_string):
            return 1
    return 0
'''
def isStopWord(cur_gram_string):
    stop_words = ["on", "whereas", "north", "boy", "christmas", "eve", "new", "year", "oscar", "academy", "called", "if", "thanksgiving", "better", "oh", "time", "i", "tight", "poor", "get", "mild", "live", "plump", "instead", "just", "small", "will", "halloween", "love", "ivy", "go", "down", "get", "come", "actually", "but", "best", "let", "big", "the", "sure", "please", "yes", "that", "this", "now", "most", "between","here", "there","okay","beside", "most", "what"]
    for stop_word in stop_words:
        if stop_word.lower() in cur_gram_string.lower():
            return 1
    return 0
'''
#function to create rows of features from words in a file
def createFeatureRows(sentence_words, preceeding_adj_words, succeeding_adj_words, suffixes, prefixes, file_path):
    n_grams = [1,2,3]
    csv_rows = []


    #consider words of sizes in n_grams
    for n in n_grams:
        #pick each sentence from list of sentences for a file
        for sentence in sentence_words:
            numwords = len(sentence)
            tags = getTagsForSentence(cleanSentence(' '.join(sentence)))
            for index in range(numwords - n + 1):
                cur_gram_list = sentence[index : index+n]
                feature_row = {}

                #if an n_gram is surrounded by markup, then class label is 1
                if '<person>' in cur_gram_list[0] and '</person>' in cur_gram_list[-1]:
                    cur_gram_list[0] = cur_gram_list[0].replace('<person>','')
                    cur_gram_list[-1] = cur_gram_list[-1].replace('</person>','')
                    feature_row["class"] = 1
                else:
                    feature_row["class"] = 0

                #remove overlapping person tags and replace class label as 0
                #Ex- <person>Mark Craven.</person> <person>Craven</person> is not a valid trigram. But valid bigram and unigram respectively.
                for i in range(len(cur_gram_list)):
                    if '<person>' in cur_gram_list[i] or '</person>' in cur_gram_list[i]:
                        cur_gram_list[i] = cur_gram_list[i].replace('<person>','')
                        cur_gram_list[i] = cur_gram_list[i].replace('</person>', '')
                        feature_row["class"] = 0

                #TODO: add various features for the current row(use feature_row dictionary)



                #join n_gram wordlist into a single string separated by spaces
                cur_gram_string = ' '.join(cur_gram_list)

                not_clean_string = cur_gram_string

                cur_gram_string = cleanString(cur_gram_string)

                for i, cur_gram in enumerate(cur_gram_list):
                    cur_gram_list[i] = cleanString(cur_gram_list[i])


                feature_row["input"] = cur_gram_string
                feature_row["num_words"] = getNumWords(cur_gram_list)
                feature_row["all_start_capital"] = isStartingCapital(cur_gram_list)
                feature_row["num_start_capital"] = numStartingCapitals(cur_gram_list)

                #logic for adding features related to next and prev words
                next_word = ""
                prev_word = ""

                if(index + n) < numwords:
                    next_word = sentence[index + n]


                if(index - 1 >= 0):
                    prev_word = sentence[index - 1]

                addAdjacentWordFeatures(feature_row, next_word, "next", succeeding_adj_words)
                addAdjacentWordFeatures(feature_row, prev_word, "prev", preceeding_adj_words)


                #logic for adding prefix and suffix features

                addTrailingWordFeatures(feature_row, cur_gram_string, suffixes)
                addLeadingWordFeatures(feature_row, cur_gram_string, prefixes)

                #logic for checking if word surrounded by parantheses
                string_with_para = not_clean_string.strip("?.,\"")
                if(string_with_para.startswith("(") and string_with_para.endswith(")")):
                    feature_row["surr_para"] = 1
                else:
                    feature_row["surr_para"] = 0

                feature_row["starts_relation"] = startWithRelation(cur_gram_list[0])
                feature_row["contains_stray"] = containsStrayCharacters(cur_gram_string)
                feature_row["all_caps"] = isWordAllCaps(cur_gram_list)
                feature_row["contains_caps"] = containsCaps(cur_gram_list)

                pos_flag = 0
                if feature_row["starts_relation"] == 1 or feature_row["contains_stray"] == 1 or feature_row["all_caps"] == 1:
                    pos_flag = 1

                next_word_pos = getValueForTag(next_word, tags, pos_flag)
                if(getNumWords(cur_gram_list) == 1):

                    feature_row["n1_word_tag"] = getValueForTag(cur_gram_list[0], tags, pos_flag)
                    '''
                    if next_word_pos == 10:
                        feature_row["n1_word_tag"] = 0
                    '''
                    feature_row["n2_word_tag"] = 0
                    feature_row["n3_word_tag"] = 0
                elif(getNumWords(cur_gram_list) == 2):
                    feature_row["n1_word_tag"] = getValueForTag(cur_gram_list[0], tags, pos_flag)
                    feature_row["n2_word_tag"] = getValueForTag(cur_gram_list[1], tags, pos_flag)
                    '''
                    if next_word_pos == 10:
                        feature_row["n1_word_tag"] = 0
                        feature_row["n2_word_tag"] = 0
                    '''
                    feature_row["n3_word_tag"] = 0
                elif(getNumWords(cur_gram_list) == 3):
                    feature_row["n1_word_tag"] = getValueForTag(cur_gram_list[0], tags, pos_flag)
                    feature_row["n2_word_tag"] = getValueForTag(cur_gram_list[1], tags, pos_flag)
                    feature_row["n3_word_tag"] = getValueForTag(cur_gram_list[2], tags, pos_flag)

                else:
                    feature_row["n1_word_tag"] = 0
                    feature_row["n2_word_tag"] = 0
                    feature_row["n3_word_tag"] = 0

                if next_word:

                    feature_row["next_word_tag"] = getValueForTag(next_word, tags, pos_flag)
                else:
                    feature_row["next_word_tag"] = 0
                if prev_word:
                    feature_row["prev_word_tag"] = getValueForTag(prev_word, tags, pos_flag)
                else:
                    feature_row["prev_word_tag"] = 0



                if next_word:
                    feature_row["next_capital_start"] = isStartingCapital([next_word])
                else:
                    feature_row["next_capital_start"] = 0

                if prev_word:
                    feature_row["prev_capital_start"] = isStartingCapital([prev_word])
                else:
                    feature_row["prev_capital_start"] = 0


                feature_row["contains_articles"] = containsArticles(cur_gram_list)
                feature_row["contains_pronouns"] = containsPronouns(cur_gram_list)
                feature_row["contains_prepositions"] = containsPrepositions(cur_gram_list,tags, pos_flag)
                feature_row["contains_adjectives"] = containsAdjective(cur_gram_list, tags, pos_flag)
                feature_row["contains_adverbs"] = containsAdverb(cur_gram_list, tags, pos_flag)


                #feature_row["is_location"] = isLocation(cur_gram_string)


                feature_row["is_language"] = isLanguage(cur_gram_string)
                feature_row["is_stop_word"] = isStopWord(cur_gram_string)

                csv_rows.append(feature_row)

    return csv_rows





#caller function to create feature rows for each file
def getExamples(file, folder_path, preceeding_adj_words, succeeding_adj_words, suffixes, prefixes):
    file_path = folder_path + "/"+ file


    file_ptr = codecs.open(file_path, "r", encoding='utf-8', errors='ignore')

    file_contents = file_ptr.read()

    file_contents = file_contents.replace('\n',' ')

    sentences = sent_tokenize(file_contents)

    sentences_words = []

    for sentence in sentences:
        words = []
        for word in sentence.split():
            words.append(word)
        sentences_words.append(words)

    file_ptr.close()

    return createFeatureRows(sentences_words, preceeding_adj_words, succeeding_adj_words, suffixes, prefixes, file_path)


def generate_test_train_files(input_folder_path,output_file_path):

    files = getFiles(input_folder_path)

    csv_file = codecs.open(output_file_path, 'w',encoding='utf-8')

    #field names of the training dataset
    #TODO: Find a better way to represent feature names if possible
    field_names = ["input", "num_words","all_start_capital", "num_start_capital","surr_para","n1_word_tag","n2_word_tag","n3_word_tag","prev_word_tag","next_word_tag","all_caps", "next_capital_start", "prev_capital_start", "contains_stray","contains_caps", "starts_relation","contains_articles", "contains_pronouns", "contains_prepositions", "contains_adjectives", "contains_adverbs", "is_language", "is_stop_word"]

    preceding_adj_words = ["a", "an", "the", "by", "from", "at", "in", "on"]
    succeeding_adj_words = ["is", "says", "said", "was"]
    #candidate_adj_words = ["a", "an", "the", "is", "are", "said", "was", "by", "from","at","in", "on"]
    suffixes = ["Sr", "Sr.", "Jr", "Jr.", "'s"]
    prefixes = ["Mr", "Mr.", "Mrs", "Mrs.", "Lt"]

    for adj_word in succeeding_adj_words:
        field_names.append("next_"+adj_word)


    for adj_word in preceding_adj_words:
        field_names.append("prev_" + adj_word)

    for suffix in suffixes:
        field_names.append("suff_"+suffix)

    for prefix in prefixes:
        field_names.append("pref_"+prefix)

    field_names.append('class')

    csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
    csv_writer.writeheader()

    #writes features rows to csv output file
    for file in files:
        csv_rows = getExamples(file, input_folder_path, preceding_adj_words, succeeding_adj_words, suffixes, prefixes)
        csv_writer.writerows(csv_rows)

    csv_file.close()





if __name__ == "__main__":
    train_input_folder_path = "../set-I"
    test_input_folder_path = "../set-J"
    train_output_file_path = "../datasets/train.csv"
    test_output_file_path = "../datasets/test.csv"
    generate_test_train_files(train_input_folder_path,train_output_file_path)
    generate_test_train_files(test_input_folder_path,test_output_file_path)