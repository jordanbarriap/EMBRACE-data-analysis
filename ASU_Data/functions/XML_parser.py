'''
    Calculate the CAR summary within a single file (might contain more than one book)
    It's based on the Tap/Decrement actions
'''
from lxml import etree
import csv

class counter:
    '''
        A counter for each book that counts CAR questions
    '''
    def __init__(self, book_name):

        self.book_name = book_name

        # There are three types of questions
        self.concrete = 0
        self.abstract = 0
        self.relational = 0

def get_books(root):
    '''
        get the book(s) appeared in a single file file
    '''
    book_list = []


    for i in root.findall('.//Book_Title'):
        if i.text is not None and i.text not in book_list:
            book_list.append(i.text)
    return book_list

def confirm_context(element):
    ancestor = element.getparent().getparent().getparent()
    
    if ancestor.tag == 'User_Action':
        selection_child =  ancestor.find('Selection')
        # locate this User_Action element
        if selection_child is not None and selection_child.text == 'TapParentQuestionTypeEvent':
            return True

def count_q(counter, ancestor):
    '''
        In the context containing 'TapParentQuestionTypeEvent' action, we toggle the counter based on Tap/Decrement
    '''
    action_subelement = ancestor.find('Action')
    for q_type in ['Concrete', 'Abstract', 'Relational']:
        if action_subelement.text == f'Tap {q_type} ({q_type[0]}) Button':
            if q_type == 'Concrete':
                counter.concrete += 1
            elif q_type == 'Abstract':
                counter.abstract += 1
            else:
                counter.relational += 1
        elif action_subelement.text == f'Decrement {q_type} ({q_type[0]}) Count':
            if q_type == 'Concrete':
                counter.concrete -= 1
            elif q_type == 'Abstract':
                counter.abstract -= 1
            else:
                counter.relational -= 1


if __name__=='__main__': 

    xml_path = 'ASU_Data/par 007/5 par007 e 10-19-2022T07_13.13.606.xml'
    tree = etree.parse(xml_path)
    root = tree.getroot()

    book_list = get_books(root)

    counter_list = []
    for book in book_list:
        # create a counter for each book in the book_list
        counter_list.append(counter(book))
    
    for counter in counter_list:
        for i in root.findall('.//Book_Title'):
                # once find an element about this book which is also within the context containg 'TapParentQuestionTypeEvent'
                if i.text == counter.book_name and confirm_context(i):
                        # we count this snippit
                        count_q(counter, i.getparent().getparent().getparent())
    
    # set up the csv file structure before writing contents to it
    with open('ASU_Data/functions/summary.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Concrete', 'Abstract', 'Relational'])

    for counter in counter_list:
        row = [counter.book_name, counter.concrete, counter.abstract, counter.relational]
        with open('ASU_Data/functions/summary.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)
        #print(f'{counter.book_name}: {counter.concrete}, {counter.abstract}, {counter.relational}')


    