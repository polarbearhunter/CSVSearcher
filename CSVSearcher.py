import csv
import os
import datetime
import argparse

wordlist=[]
entries = set()
start_date = ()
now = datetime.datetime.now()
comp_now = now.date()
now_string = str(now.strftime("%Y-%m-%d_"))

# Arguments/flags
parser = argparse.ArgumentParser(
    description='This is a CSV searching script')
parser.add_argument('-i', '--input', action='store',
                    default=False, help='CSV input file name', required=True)
parser.add_argument('-o', '--output', action='store', default=False,
                    help='Output CSV file name (will have timestamp)', required=False)
parser.add_argument('-w', '--wordlist', action='store',
                    default=False, help='Input wordlist name', required=False)
parser.add_argument('-d', '--date', action='store', default=False,
                    help='Search from this date forward MM/DD/YYYY', required=False)
args = parser.parse_args()

# Ensure proper formating for flags and deal with blanks
if args.input.lower().endswith('.csv'):  # set to lower to ignore case, if the file ends with .csv use that name
    file_input = (args.input)
else:  # If not a csv then error message and quit
    print('\n-------------------------------------------------------\nERROR: Please make sure you chose a CSV file for input\n-------------------------------------------------------')
    sys.exit()

if args.output is False:  # if the output argument is blank set it to 'Output.csv' which means it will write as timestamp_Output.csv
    file_output = ('Output.csv')
# set to lower to ignore case, if the file ends with .csv then use that file
elif args.output.lower().endswith('.csv'):
    file_output = (args.output)
else:  # otherwise add .csv to the end
    file_output = (args.output + '.csv')

if args.wordlist is False:  # if the wordlist argument is blank look locally for a wordlist.txt
    file_wordlist = ('wordlist.txt')
# set to lower to ignore case, if the files ends with .txt then use that file
elif args.wordlist.lower().endswith('.txt'):
    file_wordlist = (args.wordlist)
else:  # if dictionary is not a txt file then display and error message and quit
    print('\n--------------------------------------------------------------\nERROR: Please make sure you chose a TXT file for a dictionary\n--------------------------------------------------------------')
    sys.exit()

if args.date is False:
    start_date = now.replace(year=1000)
else:
    start_date =(datetime.datetime.strptime(args.date, '%m/%d/%Y').date())

print(start_date)

with open(file_input, 'r', newline='') as input, open(file_output, 'w', newline='') as out, open(file_wordlist, 'r', newline='') as word_file:  # opens csv and declares output csv
    reader = csv.reader(
        input, dialect="excel")  # declares csv reader
    # declares csv writer, lines end with new line, delimiter is now ~ so
    # commas can exist
    writer = csv.writer(
        out, lineterminator='\n', delimiter=',')
    wordlist_reader = csv.reader(word_file)  # declares csv reader
    for row in wordlist_reader:
            # extends the lines in the wordlist into a usable tuple
        wordlist.extend(row)
    wordlist_len = len(wordlist)  # finds length of wordlist and saves as a var
    # pulls the header line so that it can be saved
    headers = next(reader)
    headers.insert(8, 'Keyword')
    writer.writerow(headers)
    for row in reader:  # for every row in the csv
        for col in row:  # for every column in said row
            for X in range(wordlist_len):  # for as long as we have words
                # if word X matches something in that column (sent to lower so
                # we don't need to worry about case)
                check_row_5 = wordlist[X] in row[5].lower()
                check_row_4 = wordlist[X] in row[4].lower()
                if check_row_4 or check_row_5:
                    cur_row = []
                    comp_date = datetime.datetime.strptime(row[1], '%A, %B %d, %Y').date()
                    cur_row.append(row[0])
                    cur_row.append(comp_date)
                    cur_row.append(row[2])
                    cur_row.append(row[3])
                    cur_row.append(row[4])
                    cur_row.append(row[5])
                    cur_row.append(row[6])
                    cur_row.append(row[7])
                    cur_row.append(wordlist[X])
                    key = (row[2], row[3], row[4], row[5])
                    if key not in entries:  # if the key is not found in that line
                        if comp_date > start_date:
                            writer.writerow(cur_row)  # write to the output file
                            entries.add(key)  # and add to the key

#:DONE:10 Find a way to limit search by date. using start_date until current date. Not sure how to check, but removed a ton of code by reworking it
#:DONE:0 clean up the way that we search in wordlist so that it doesn't include col(0,1,2,3) search only by 4,5 Or is this done?
#:TODO:0 find some way that the trigger word is bolded so you can see it EG trigger word is sin, found in crosSINg

#Clean-up and renaming

now_string = str(now.strftime("%Y-%m-%d_"))
os.replace(file_output, now_string + file_output)
