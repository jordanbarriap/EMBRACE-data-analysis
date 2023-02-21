import xml.etree.ElementTree as ET
import os

class question:
    def __init__(self, name, count):
        self.name = name
        self.count = count
    
    def increment(self, num):
        """
            a helper function to increment the number of each type of function
        """
        self.count += num


def count_questions(root, q_type):
    """
        Count number of questions for each question type in each file
    """
    print("---------------------------------")
    # find all the Abstract elements
    for element in root.iter(q_type.name):
        # there are sub elements
        if (len(element) > 0):
            for sub_element in element:
                q_type.increment(int(sub_element.text))
                print(f"{q_type.name} questions in {sub_element.tag}: {sub_element.text}")
        # there is no sub element
        # else:
        #     # directly grab the number of this type of question
        #     q_type.increment(int(element.text))
        #     print(f"{q_type.name} questions: {element.text}")
    return q_type.count

def process_xml_file():
    # dealing with each xml file under this folder
    for xml_file in dir_list:
        print("NEW FILE")
        tree = ET.parse(dir_path + '/' +xml_file)
        root = tree.getroot()
        
        # create three question objects
        concrete = question('Concrete', 0)
        abstract = question('Abstract', 0)
        relational = question('Relational', 0)
        q_types = [concrete, abstract, relational]

        result_list = []
        for q_type in q_types:
            result_list.append(count_questions(root, q_type))

        print('====================================')
        print(result_list)

if __name__=='__main__': 

    dir_path = 'ASU_Data/par 007'
    dir_list = [file for file in os.listdir(dir_path) if os.path.splitext(file)[1] == '.xml']

    num_file = len(dir_list)
    
    # aggregation counters
    total_concrete = 0
    total_abstract = 0
    total_relational = 0

    process_xml_file()