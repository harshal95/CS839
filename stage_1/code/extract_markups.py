import os
import csv

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

    input_string = input_string.strip("().,")
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

#function to create rows of features from words in a file
def createFeatureRows(words, candidate_adjacent_words, suffixes, prefixes):
    n_grams = [1,2,3]
    csv_rows = []
    numwords = len(words)

    #consider words of sizes in n_grams
    for n in n_grams:
        for index in range(numwords - n + 1):
            cur_gram_list = words[index : index+n]
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
                next_word = words[index + n]


            if(index - 1 >= 0):
                prev_word = words[index - 1]

            addAdjacentWordFeatures(feature_row, next_word, "next", candidate_adjacent_words)
            addAdjacentWordFeatures(feature_row, prev_word, "prev", candidate_adjacent_words)


            #logic for adding prefix and suffix features

            addTrailingWordFeatures(feature_row, cur_gram_string, suffixes)
            addLeadingWordFeatures(feature_row, cur_gram_string, prefixes)

            string_with_para = not_clean_string.strip(".,")
            if(string_with_para.startswith("(") and string_with_para.endswith(")")):
                feature_row["surr_para"] = 1
            else:
                feature_row["surr_para"] = 0



            csv_rows.append(feature_row)

    return csv_rows





#caller function to create feature rows for each file
def getExamples(file, folder_path, candidate_adjacent_words, suffixes, prefixes):
    file_path = folder_path + "/"+ file

    words = []

    file_ptr = open(file_path, "r")

    for line in file_ptr:
        for word in line.split():
            words.append(word)

    file_ptr.close()

    return createFeatureRows(words, candidate_adjacent_words, suffixes, prefixes)





if __name__ == "__main__":

    #path to marked up docs and output path to create csv files
    #TODO: separate training and test csv files,docs
    input_folder_path = "train_markedup_docs"
    files = getFiles(input_folder_path)

    output_file_path = "datasets/train.csv"
    csv_file = open(output_file_path, 'w')

    #field names of the training dataset
    #TODO: Find a better way to represent feature names if possible
    field_names = ["input", "num_words", "all_start_capital", "num_start_capital","surr_para"]

    candidate_adj_words = ["is", "are", "said", "was", "by", "from"]
    suffixes = ["Sr", "Sr.", "Jr", "Jr.", "'s"]
    prefixes = ["Mr", "Mr.", "Mrs", "Mrs."]

    for adj_word in candidate_adj_words:
        field_names.append("next_"+adj_word)
        field_names.append("prev_"+adj_word)

    for suffix in suffixes:
        field_names.append("suff_"+suffix)

    for prefix in prefixes:
        field_names.append("pref_"+prefix)



    field_names.append('class')



    csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
    csv_writer.writeheader()

    #writes features rows to csv output file
    for file in files:
        csv_rows = getExamples(file, input_folder_path, candidate_adj_words, suffixes, prefixes)
        csv_writer.writerows(csv_rows)

    csv_file.close()