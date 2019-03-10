import os

if __name__=="__main__":

    folder_path = "../all_docs"
    dest_path = "../selected_docs"
    files = os.listdir(folder_path)

    for i, file in enumerate(files):
        if(i == 325):
            break

        os.rename(folder_path+"/"+file, dest_path + "/" + str(i+1) +".txt")


