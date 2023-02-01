'''
    Convert the txt file in the directory to a XML file
'''
import os

dir_path = 'ASU_Data/par 001/'
txt_path = 'ASU_Data/par 001/x par001 x 10-16-2021T05_10.40.862.txt'

# Batch convert txt files under a directory
def txt_to_xml(dir_path): 
    files_list = os.listdir(dir_path) 
    for filename in files_list: 
        used_name = os.path.splitext(filename) 
        if used_name[1] == '.txt':
            new_name = used_name[0] + '.xml' 
            os.rename(dir_path + filename, dir_path + new_name) 

# convert one txt file to a XML file
def txt_to_xml_single(filepath): 
    filename = os.path.basename(filepath)
    used_name = os.path.splitext(filename) 
    if used_name[1] == '.txt':
        new_path = filepath[:-3] + 'xml' 
        os.rename(filepath, new_path) 

if __name__=='__main__': 
    txt_to_xml(dir_path)
