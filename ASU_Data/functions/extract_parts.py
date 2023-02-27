from lxml import etree

def extract_file(root, f):
    # iterate thru all the elements
    for element in root.iter():
        # CAR labels
        if element.tag == 'Input' and len(element) > 0 and  element[0].tag == 'Concrete':
            f.write("\n<Input>\n")
            for i in element:
                f.write(f'  <{i.tag}> {i.text}  </{i.tag}>\n')
            
            f.write("</Input>\n\n")
        
        # tap/decrement events
        if element.text == 'TapParentQuestionTypeEvent':
            action_element = element.getparent().find('Action')
            f.write(f'  <{action_element.tag}> {action_element.text}  </{action_element.tag}>\n')
            book_title_element = element.getparent().find('Context')[0].find('Book_Title')
            f.write(f'  <{book_title_element.tag}> {book_title_element.text} </{book_title_element.tag}>\n\n')
        
        # CAR labels with language separation
        if element.tag == 'QuestionTypeCounts':
            f.write("\n<QuestionTypeCounts>\n")
            for i in element:
                f.write(f'   <{i.tag}>\n')
                for sub_i in i:
                    f.write(f"   <{sub_i.tag}> {sub_i.text} </{sub_i.tag}>\n")
                f.write(f'</{i.tag}>\n')
            f.write("</QuestionTypeCounts>\n\n")


def extract_folder():
    pass


if __name__=='__main__': 
    xml_path = 'ASU_Data/par 007/5 par007 e 10-19-2022T07_13.13.606.xml'
    folder_path = 'ASU_Data/par 007'

    tree = etree.parse(xml_path)
    # root for one single xml file
    root = tree.getroot()


    f = open('ASU_Data/functions/test.xml', "a")
    extract_file(root, f)
    f.close()