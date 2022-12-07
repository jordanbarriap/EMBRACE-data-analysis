
import os
import sys

txt_path = ('./') 
xml_path = ('E:\Desktop\\data_txt\\xml_done/') 

def txt_to_xml(indir,outdir): 
    files_list = os.listdir(indir) 
    for filename in files_list: 
        used_name = os.path.splitext(filename) 
        if used_name[1] == '.txt'
            new_name = used_name[0] + '.xml' 
            os.rename(filename,new_name ) 
            
    print((filename, new_name)) 

print('Successfully converted .txt to .xml')

if __name__=='__main__': 
    
    txt_to_xml(txt_path, xml_path)
