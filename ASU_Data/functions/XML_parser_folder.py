'''
    There are two types of actions: Tap (increment) and decrement
    Different books have different counters!
'''

from lxml import etree
import os

class counter:
    '''
        A counter for each book that has three question objects for CAR questions
    '''
    def __init__(self, book_name):

        self.book_name = book_name

        #  There are three types of questions
        self.concrete = 0
        self.abstract = 0
        self.relational = 0

def get_books():
    '''
        Iterate thru all the files to get a list of all the books this user reads

        return: 
            a list of all the book this user reads
    '''
    book_list = []

    for xml_file in dir_list:
        # parse each xml file
        tree = etree.parse(dir_path + '/' + xml_file)
        root = tree.getroot()

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

        parameters:
            counter: a counter for a specific book
            ancestor: the 'User_Action' element that contains the 'TapParentQuestionTypeEvent' subelement
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


def process_xml_file(counter_list):
    '''
        Dealing with each xml file under this folder and modify counter_list in-place

        parameter: 
            counter_list: a list containing all the counters for all the books
    '''
    # A list containing 3 counters for CAR questions
    #aggregate_count = []

    for xml_file in dir_list:
        # parse each xml file
        tree = etree.parse(dir_path + '/' + xml_file)
        root = tree.getroot()

        # send books(counters) one by one
        for counter in counter_list:
            for i in root.findall('.//Book_Title'):
                # for an element about this book which is also within the context we want to find
                if i.text == counter.book_name and confirm_context(i):
                        # we count it
                        count_q(counter, i.getparent().getparent().getparent())
        


if __name__=='__main__': 

    dir_path = 'ASU_Data/par 007'
    dir_list = [file for file in os.listdir(dir_path) if os.path.splitext(file)[1] == '.xml']

    # get a set of books
    book_list = get_books()

    counter_list = []
    for book in book_list:
        # create a counter for each book in the book_list
        counter_list.append(counter(book))

    process_xml_file(counter_list)
    for counter in counter_list:
        print(f'{counter.book_name}: {counter.concrete}, {counter.abstract}, {counter.relational}')