from lxml import etree
import os

class question:
    def __init__(self, name, count):
        self.name = name
        self.count = count

def count_question(root, q_type):
    '''
        parameter(s):  a quesetion object 'q_type'
        Modifying the count attribute directly
    '''
    name = q_type.name
    for i in root.findall('.//Action'):
        if i.text == f'Tap {name} ({name[0]}) Button':
            q_type.count += 1
        elif i.text == f'Decrement {name} ({name[0]}) Count':
            q_type.count -= 1

def process_xml_file(q_types):
    '''
        Dealing with each xml file under this folder
    '''
    # A list containing 3 counters for CAR questions
    aggregate_count = []

    for xml_file in dir_list:
        # parse each xml file
        tree = etree.parse(dir_path + '/' + xml_file)
        root = tree.getroot()
        
        # Modify the counter of each type of question
        for q_type in q_types:
            count_question(root, q_type)
        
    for q_type in q_types:
        aggregate_count.append(q_type.count)
    return aggregate_count


if __name__=='__main__': 

    dir_path = 'ASU_Data/par 007'
    dir_list = [file for file in os.listdir(dir_path) if os.path.splitext(file)[1] == '.xml']

    # create three question objects for this user (count all the files)
    concrete = question('Concrete', 0)
    abstract = question('Abstract', 0)
    relational = question('Relational', 0)
    q_types = [concrete, abstract, relational]

    # each file will modify the global counter
    aggregate_count = process_xml_file(q_types)
    print(aggregate_count)