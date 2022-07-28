import tscribe
import csv

# REMEMBER TO CHANGE HERE
# change json file name and save_as every time we convert a new file
tscribe.write("aws_output2.json", format='csv', save_as='aws_output2.csv')

rows = []

# REMEMBER TO CHANGE HERE
with open('aws_output2.csv') as csv_file:
    csv_reader = csv.reader(csv_file)

    # append each row as a list to a bigger list
    line = 0
    for row in csv_reader:
        if line != 0:
            row.pop(0)
            rows.append(row)
        line += 1

sentences = dict()

# convert every inner list into an item inside of a big dictionary, and use the start time as keys
for row in rows:
    sentences[row[0]] = row

# sort the keys 
time_keys = sorted(sentences.keys())

output_list = []

for key in time_keys:
    output_list.append(sentences[key])

# REMEMBER TO CHANGE HERE
# opening the csv file in 'w+' mode
file = open('aws_output2.csv', 'w+', newline ='')
# writing the data into the file
with file:   
    write = csv.writer(file)
    write.writerows(output_list)