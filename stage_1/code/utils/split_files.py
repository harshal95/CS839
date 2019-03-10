import glob
import sklearn
import shutil
import sklearn.model_selection

def split_files(intput_path,train_output_path,test_output_path):

    files = glob.glob(intput_path)
    train, test = sklearn.model_selection.train_test_split(files, test_size=0.33)

    for file in train:
        shutil.copy(file, train_output_path + file.split("\\")[1])

    for file in test:
        shutil.copy(file,test_output_path+ file.split("\\")[1])


if __name__=="__main__":
	split_files("../stage_1/set-B/*.txt","../stage_1/set-I/","../stage_1/set-J/")
