from collections import ChainMap
import pandas as pd
import xmltodict


def xml_to_csv(action, filename):

    input_list = []
    context = []
    df1 = pd.DataFrame(action)
    df2 = df1.drop(columns=['Input','Context'])

    for i in df1['Input']:
        if i != 'NULL':
            input_list.append(i)

    for d in df1['Context']:
        study_context = list(d.values())
        context_items = dict(ChainMap(*study_context))
        context.append(context_items)

    df3 = pd.DataFrame(input_list)
    df4 = pd.DataFrame(context)
    final_df = pd.concat([df2,df3,df4], axis=1)

    final_df.to_csv(filename + ".csv", header=True, index=False)


if __name__ == '__main__':

    with open('input.xml', 'r') as f:
        data = f.read()

    d = xmltodict.parse(data)
    df = pd.DataFrame(d)

    types = df['Study']
    user_action = types['User_Action']
    system_action = types['System_Action']
    

    user_action_df = xml_to_csv(user_action, "User_Action")
    system_action_df = xml_to_csv(system_action, "System_Action")
    


