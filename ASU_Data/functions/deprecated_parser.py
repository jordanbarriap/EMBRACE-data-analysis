import xml.etree.ElementTree as ET
from lxml import etree

class question:
    def __init__(self, name, count):
        self.name = name
        self.count = count
    
    def increment(self, num):
        """
            a helper function to increment the number of each type of function
        """
        self.count += num

# create three question objects
concrete = question('Concrete', 0)
abstract = question('Abstract', 0)
relational = question('Relational', 0)
q_types = [concrete, abstract, relational]

def count_questions(q_type):
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

def count_question_tap():
    tap_c = 0
    print("Count questions using tap")
    for i in root.findall('.//Action'):
        if i.text == "Tap Concrete (C) Button":
            tap_c += 1
            #print(etree.SubElement(i.getparent(), "User_Action_ID").text)
    return tap_c


if __name__=='__main__': 
    
    xml_path = 'ASU_Data/par 007/5 par007 e 10-19-2022T07_13.13.606.xml'
    tree = etree.parse(xml_path)
    root = tree.getroot()

    result_list = []
    # for q_type in q_types:
    #     result_list.append(count_questions(q_type))
    tap_c = count_question_tap()
    print(tap_c)

    print('====================================')
    #print(result_list)