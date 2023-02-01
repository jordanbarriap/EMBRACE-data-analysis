import xml.etree.ElementTree as ET

xml_path = 'ASU_Data/par 001/x par001 x 10-16-2021T05_10.40.862.xml'
tree = ET.parse(xml_path)
root = tree.getroot()

num_concrete = 0
num_abstract = 0
num_relational = 0

def increment(q_type, num):
    if q_type == 'Concrete':
        global num_concrete
        num_concrete += num
    elif q_type == 'Abstract':
        global num_abstract
        num_abstract += num
    else:
        global num_relational
        num_relational += num

def count_questions(q_type):
    print("---------------------------------")
    # find all the Abstract elements
    for element in root.iter(q_type):
        # there are sub elements
        if (len(element) > 0):
            for sub_element in element:
                increment(q_type, int(sub_element.text))
                print(f"{q_type} questions in {sub_element.tag}: {sub_element.text}")
        # there is no sub element
        else:
            # directly grab the number of this type of question
            increment(q_type, int(element.text))
            print(f"{q_type} questions: {element.text}")



q_types = ['Concrete', 'Abstract', 'Relational']
# count the number of questions for each question type
for q_type in q_types:
    count_questions(q_type)

print('====================================')
print(f"Number of concrete questions: {num_concrete}")
print(f"Number of abstract questions: {num_abstract}")
print(f"Number of relational questions: {num_relational}")
