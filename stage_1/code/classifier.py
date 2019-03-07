import sklearn
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pandas as pd
from sklearn.externals import joblib
import glob
import sklearn
import shutil
import sklearn.model_selection
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn import svm
from sklearn import tree
from sklearn.metrics import precision_recall_fscore_support
from sklearn.model_selection import StratifiedKFold
from sklearn.ensemble import RandomForestClassifier


class Classifiers(object):
    def __init__(self, train_file,test_file):
        self.train_data_frame = pd.read_csv(train_file,encoding='ISO-8859-1')
        self.test_data_frame = pd.read_csv(test_file)
        n_splits = 10
        self.stratiKsplit = StratifiedKFold(n_splits, random_state=1) # random state?

        #exclude n-grams
        del self.train_data_frame['input']
        del self.test_data_frame['input']
     
        label_col = 'class'
        self.actual_train_data_label = self.train_data_frame[label_col].values
        self.actual_test_data_label = self.test_data_frame[label_col].values
        del self.train_data_frame[label_col]
        del self.test_data_frame[label_col]
        self.train_data = self.train_data_frame.values
        self.test_data = self.test_data_frame.values
        self.stratiKsplit.get_n_splits(self.train_data_frame, self.actual_train_data_label)

    def decisionTree(self):
        decTree = DecisionTreeClassifier()
        accuracy = 0
        scores = []
        pred = []
        precision_list = []
        recall_list = []
        fscore_list = []
        for train_index, test_index in self.stratiKsplit.split(self.train_data, self.actual_train_data_label):
            #Build a decision tree classifier from the training set (x, y).
            #x :The training input samples
            #y: The target values (actual class labels)

            decTree.fit(self.train_data[train_index],self.actual_train_data_label[train_index])

            #predict lables for samples in test fold (test_index.
            predicted_label = decTree.predict(self.train_data[test_index])

            #now compute precision,recall and fscore using original actual train data label against predicted label
            # F-score  is a measure of a test's accuracy
            #Support :The number of occurrences of each label in actual_train_data_label
            #average = macro ->the recall, precision and f1 for all classes are computed individually and then their mean is returned. 
            precision,recall,fscore,support = precision_recall_fscore_support(self.actual_train_data_label[test_index], predicted_label, average='macro')
            precision_list.append(precision)
            recall_list.append(recall)
            fscore_list.append(fscore)
        # Should we take Max or take average? Note : we are passing average as macro.
        print("DecisionTree Classifier")
        print("\nMax Precision: "+ str(max(precision_list))+ "\nMax Recall: " + str(max(recall_list))+ "\nMax fscore: "+ str(max(fscore_list)) + "\n")


    def linearRegression(self):
        
        print ('Learning using Linear Regression')
        linReg = LinearRegression()

        precision_list = []
        recall_list = []
        fscore_list = []
        accuracy = 0
        scores = []
        pred = []

        for train_index, test_index in self.stratiKsplit.split(self.train_data, self.actual_train_data_label):
            #Build a decision tree classifier from the training set (x, y).
            #x :The training input samples
            #y: The target values (actual class labels)

            linReg.fit(self.train_data[train_index],self.actual_train_data_label[train_index])

            #predict lables for samples in test fold (test_index.
            predicted_label = linReg.predict(self.train_data[test_index])

            threshold = round(np.mean(predicted_label), 2)
            predicted_label = np.where(predicted_label > threshold, 1, 0)

            #now compute precision,recall and fscore using original actual train data label against predicted label
            # F-score  is a measure of a test's accuracy
            #Support :The number of occurrences of each label in actual_train_data_label
            #average = macro ->the recall, precision and f1 for all classes are computed individually and then their mean is returned. 
            precision,recall,fscore,support = precision_recall_fscore_support(self.actual_train_data_label[test_index], predicted_label, average='macro')

            precision_list.append(precision)
            recall_list.append(recall)
            fscore_list.append(fscore)
        # Should we take Max or take average? Note : we are passing average as macro.
        print("Linear Regression Classifier")
        print("\nMax Precision: "+ str(max(precision_list))+ "\nMax Recall: " + str(max(recall_list))+ "\nMax fscore: "+ str(max(fscore_list)) + "\n")

    def randomForest(self):
        #randForest = RandomForestClassifier(random_state=1)
        randForest = RandomForestClassifier()

        accuracy = 0
        precision_list = []
        recall_list = []
        fscore_list = []
        for train_index, test_index in self.stratiKsplit.split(self.train_data, self.actual_train_data_label):
            #Build a decision tree classifier from the training set (x, y).
            #x :The training input samples
            #y: The target values (actual class labels)

            randForest.fit(self.train_data[train_index],self.actual_train_data_label[train_index])

            #predict lables for samples in test fold (test_index.
            predicted_label = randForest.predict(self.train_data[test_index])

            #now compute precision,recall and fscore using original actual train data label against predicted label
            # F-score  is a measure of a test's accuracy
            #Support :The number of occurrences of each label in actual_train_data_label
            #average = macro ->the recall, precision and f1 for all classes are computed individually and then their mean is returned. 
            precision,recall,fscore,support = precision_recall_fscore_support(self.actual_train_data_label[test_index], predicted_label, average='macro')

            precision_list.append(precision)
            recall_list.append(recall)
            fscore_list.append(fscore)
        # Should we take Max or take average? Note : we are passing average as macro.
        print("Random Forest Classifier")
        print("\nMax Precision: " + str(max(precision_list)) + "\nMax Recall: " + str(max(recall_list)) + "\nMax fscore: " + str(max(fscore_list)) + "\n")


    def logisticRegression(self, penalty='l2', max_iter=10, *kwargs):
        #logReg = LogisticRegression(C = 100.0,random_state = 1)
        logReg = LogisticRegression()

        accuracy = 0
        precision_list = []
        recall_list = []
        fscore_list = []

        print ('Learning using Logistic Regression')
        for train_index, test_index in self.stratiKsplit.split(self.train_data, self.actual_train_data_label):
            #Build a decision tree classifier from the training set (x, y).
            #x :The training input samples
            #y: The target values (actual class labels)

            logReg.fit(self.train_data[train_index],self.actual_train_data_label[train_index])

            #predict lables for samples in test fold (test_index.
            predicted_label = logReg.predict(self.train_data[test_index])

    
            #now compute precision,recall and fscore using original actual train data label against predicted label
            # F-score  is a measure of a test's accuracy
            #Support :The number of occurrences of each label in actual_train_data_label
            #average = macro ->the recall, precision and f1 for all classes are computed individually and then their mean is returned. 
            precision,recall,fscore,support = precision_recall_fscore_support(self.actual_train_data_label[test_index], predicted_label, average='macro')

            precision_list.append(precision)
            recall_list.append(recall)
            fscore_list.append(fscore)
        # Should we take Max or take average? Note : we are passing average as macro.
        print("\nMax Precision: " + str(max(precision_list)) + "\nMax Recall: " + str(max(recall_list)) + "\nMax fscore: " + str(max(fscore_list)) + "\n")

    def logisticRegression_on_test_set(self):
        logReg = LogisticRegression(C = 100.0, random_state=1)
        logReg.fit(self.train_data,self.actual_train_data_label)
        predicted_label = logReg.predict(self.test_data)
        precision, recall, fscore ,support = precision_recall_fscore_support(self.actual_test_data_label, predicted_label, average='macro')
        print(" Logistic Regression on Test Set\n")
        print("Precision on Test Set: "+ str(precision) +
        "\nRecall on Test Set: "+ str(recall) +
        "\nFScore on Test Set: "+ str(fscore))
   
        
if __name__ == "__main__":
    train_file_path = "../datasets/train.csv"
    test_t_file_path = "../datasets/test.csv"
    clf = Classifiers(train_file_path,test_t_file_path)

    clf.decisionTree()
    clf.linearRegression()
    clf.logisticRegression()
    clf.randomForest()
    clf.logisticRegression_on_test_set()

