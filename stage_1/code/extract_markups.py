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

#function to create rows of features from words in a file
def createFeatureRows(words):
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
                feature_row['class'] = 1
            else:
                feature_row['class'] = 0

            #remove overlapping person tags and replace class label as 0
            #Ex- <person>Mark Craven.</person> <person>Craven</person> is not a valid trigram. But valid bigram and unigram respectively.
            for i in range(len(cur_gram_list)):
                if '<person>' in cur_gram_list[i] or '</person>' in cur_gram_list[i]:
                    cur_gram_list[i] = cur_gram_list[i].replace('<person>','')
                    cur_gram_list[i] = cur_gram_list[i].replace('</person>', '')
                    feature_row['class'] = 0

            #TODO: add various features for the current row(use feature_row dictionary)

            #join n_gram wordlist into a single string separated by spaces
            cur_gram_string = ' '.join(cur_gram_list)


            cur_gram_string = cleanString(cur_gram_string)

            feature_row['input'] = cur_gram_string
            csv_rows.append(feature_row)

    return csv_rows





#caller function to create feature rows for each file
def getExamples(file, folder_path):
    file_path = folder_path + "/"+ file

    words = []

    file_ptr = open(file_path, "r")

    for line in file_ptr:
        for word in line.split():
            words.append(word)

    file_ptr.close()

    return createFeatureRows(words)





if __name__ == "__main__":

    #path to marked up docs and output path to create csv files
    #TODO: separate training and test csv files,docs
    input_folder_path = "train_markedup_docs"
    files = getFiles(input_folder_path)

    output_file_path = "datasets/train.csv"
    csv_file = open(output_file_path, 'w')

    #field names of the training dataset
    #TODO: Find a better way to represent feature names if possible
    field_names = ['input', 'class']

    csv_writer = csv.DictWriter(csv_file, fieldnames=field_names)
    csv_writer.writeheader()

    #writes features rows to csv output file
    for file in files:
        csv_rows = getExamples(file, input_folder_path)
        csv_writer.writerows(csv_rows)

    csv_file.close()