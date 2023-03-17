from lxml import etree


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
        for i in root.findall('.//Selection'):
            if i.text == 'QuestionAsked':
                pass

