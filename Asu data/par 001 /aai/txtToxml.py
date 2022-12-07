
import os
import sys

txt_path = ('./') # 需要转化的txt文件夹路径 
xml_path = ('E:\Desktop\\data_txt\\xml_done/') # 输出文件夹路径

def txt_to_xml(indir,outdir): 
    files_list = os.listdir(indir) # 读取文件夹下的文件列表 
    for filename in files_list: 
        used_name = os.path.splitext(filename) # 分离文件名与后缀名 
        if used_name[1] == '.txt': # 根据需要的后缀名修改文件类型，不同的类型剔除 
            new_name = used_name[0] + '.xml' 
            os.rename(filename,new_name ) 
            
    print("文件%s从重命名成功，新的文件名为%s"%(filename, new_name)) 

print('Successfully converted .txt to .xml')

if __name__=='__main__': 
    
    txt_to_xml(txt_path, xml_path)
