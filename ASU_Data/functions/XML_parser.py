'''
    There are three types of questions
    There are two types of actions: Tap (increment) and decrement
'''
from lxml import etree

class question:
    def __init__(self, name, count):
        self.name = name
        self.count = count

def count_question(q_type):
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


if __name__=='__main__': 

    xml_path = 'ASU_Data/par 007/5 par007 e 10-19-2022T07_13.13.606.xml'
    tree = etree.parse(xml_path)
    root = tree.getroot()

    # create three question objects
    concrete = question('Concrete', 0)
    abstract = question('Abstract', 0)
    relational = question('Relational', 0)
    q_types = [concrete, abstract, relational]

    aggregate_count = []
    for q_type in q_types:
        count_question(q_type)
        aggregate_count.append(q_type.count)
    print(aggregate_count)