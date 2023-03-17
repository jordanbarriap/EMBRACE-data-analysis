'''
    There are two types of actions: Tap (increment) and decrement
    Different books have different counters!
'''

from lxml import etree
import os
import csv

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
    '''
        Return:
            A tuple (if we're in the correct context, which context it is)
    '''
    ancestor = element.getparent().getparent().getparent()
    
    if ancestor.tag == 'User_Action':
        selection_child =  ancestor.find('Selection')
        # locate this User_Action element
        if selection_child is not None and (selection_child.text == 'TapParentQuestionTypeEvent' or selection_child.text == 'QuestionAsked'):
            return (True, 1 if selection_child.text == 'TapParentQuestionTypeEvent' else 2)
    return (False,0)

def count_q(counter, ancestor, context):
    '''
        In the context containing 'TapParentQuestionTypeEvent' selection, we toggle the counter based on Tap/Decrement
        In the context containing 'QuestionAsked' selection, we increment the corrsponding question number based on the text in the action tag

        parameters:
            counter: a counter for a specific book
            ancestor: the 'User_Action' element that contains the 'TapParentQuestionTypeEvent' subelement
    '''
    if context == 1:
        # 'TapParentQuestionTypeEvent' selection
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
    elif context == 2:
        # 'QuestionAsked' selection
        action_subelement = ancestor.find('Action')
        if action_subelement.text == '(C)':
            counter.concrete += 1
        elif action_subelement.text == '(A)':
            counter.abstract += 1
        elif action_subelement.text == '(R)':
            counter.relational += 1


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
                if i.text == counter.book_name and confirm_context(i)[0]:
                        # we count it
                        count_q(counter, i.getparent().getparent().getparent(), confirm_context(i)[1])
        


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

    # set up the csv file structure before writing contents to it
    with open('ASU_Data/functions/summary.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Concrete', 'Abstract', 'Relational', 'Concrete Proportion', 'Abstract Proportion', 'Relational Proportion'])

    for counter in counter_list:

        title = counter.book_name
        # print(title)

        # a list containing the number of existed CAR questions
        PQ_number = []

        # grab the number of CAR questions existed in this book
        with open('ASU_Data/functions/CAR_questions.csv', 'r') as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)  # skip header row
            for row in csv_reader:
                # locate the row
                if row[0] == title:
                    print(f'Found : {title}')
                    PQ_number = [int(x) for x in row[1:]]  # convert strings to integers
                    break
        
        concrete = counter.concrete
        abstract = counter.abstract
        relational = counter.relational

        #print(f'{title} : {PQ_number}')

        row = [title, concrete, abstract, relational, round(concrete/PQ_number[0], 4), round(abstract/PQ_number[1], 4), round(relational/PQ_number[2], 4)]
        with open('ASU_Data/functions/summary.csv', 'a', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(row)
        