import csv
import os
import datetime
import argparse
import sys

# set's required lists
wordlist = []
formatedlist = []
file_output = []
month_check = ['January', 'February', 'March', 'April', 'May', 'June',
               'July', 'August', 'September', 'October', 'November', 'December']

# Arguments/flags
parser = argparse.ArgumentParser(
    description='This is a CSV searching script')
parser.add_argument('-i', '--input', action='store',
                    default=False, help='CSV input file name', required=True)
parser.add_argument('-o', '--output', action='store', default=False,
                    help='Output CSV file name (will have timestamp)', required=False)
parser.add_argument('-w', '--wordlist', action='store',
                    default=False, help='Input wordlist name', required=False)
parser.add_argument('-d', '--days', action='store', default=False,
                    help='Limit search to the most recent "d" days', required=False)
parser.add_argument('-m', '--month', action='store', default=False,
                    help='Limit search to a certain month', required=False)
parser.add_argument('-y', '--year', action='store', default=False,
                    help='Limit search to a certain year', required=False)
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
    filw_wordlist = (args.wordlist)
else:  # if dictionary is not a txt file then display and error message and quit
    print('\n--------------------------------------------------------------\nERROR: Please make sure you chose a TXT file for a dictionary\n--------------------------------------------------------------')
    sys.exit()

if args.days is False:  # if the days argument is blank set it to ' ' which means it will show any days
    date_days = ' '
# check to make sure the the input was an integer
elif len(args.days) is 2 or len(args.days) is 1 and args.days.isdigit():
    date_days = (args.days)
else:  # if days isnt an integer then error message and quit
    print('\n-----------------------------------------------------------\nERROR: Please make sure you input a whole number for a day\n-----------------------------------------------------------')
    sys.exit()

if args.month is False:  # if the month argument is blank set it to ' ' which means it will show any month
    date_month = ' '
# set to a title to ignore case, if that month exists in the month_check
# list then use it
elif args.month.title() in month_check:
    date_month = (args.month.title())
else:  # if months is not a month then error message and quit
    print('\n-------------------------------------------------\nERROR: Please make sure you input a proper month\n-------------------------------------------------')
    sys.exit()

if args.year is False:
    date_year = ' '  # if the year is blank set it to ' ' which means it will show any month
# if the year input is 2 (07) numbers long than 20+input (2007) if
# date_year (2088)> current year then 19+input (1988)
elif len(args.year) is 2 and args.year.isdigit():
    date_year = ('20' + args.year)
    if int(date_year) > datetime.datetime.now().year:
        date_year = ('19' + args.year)
# if the year input is 4()  #if the year input is 4 numbers long than use it
elif len(args.year) is 4 and args.year.isdigit():
    date_year = (args.year)
else:  # if years is not a year then error message and quit
    print('\n-------------------------------------------------\nERROR: Please make sure you input a proper year\n-------------------------------------------------')
    sys.exit()
# TODO:10 Need to figure out a better way to do dates for searching
# if date_days is not ' ':
#     date_new = (datetime.timedelta(days=int(date_days)))
#     date_temp = str(datetime.date.today() - date_new)
#     date_back = datetime.datetime.strptime(date_temp, '%Y-%m-%d')
#     print(date_back)
#     date_month = date_back.strftime('%B')
#     date_year = date_back.strftime('%Y')
#     date_day = date_back.strftime('%d')
#     print(date_day)

# Checks the CSV against the worldist
with open(file_input, 'r', newline='') as input_in, open('OutWithDupes.csv', 'w', newline='') as input_out, open(file_wordlist, 'r', newline='') as word_file:  # opens csv and declares output csv
    input_reader = csv.reader(
        input_in, dialect="excel")  # declares csv reader
    # declares csv writer, lines end with new line, delimiter is now ~ so
    # commas can exist
    input_writer = csv.writer(
        input_out, lineterminator='\n', delimiter='~')
    wordlist_reader = csv.reader(word_file)  # declares csv reader
    for row in wordlist_reader:
        # extends the lines in the wordlist into a usable tuple
        wordlist.extend(row)
    wordlist_len = len(wordlist)  # finds length of wordlist and saves as a var
    # pulls the header line so that it can be saved
    headers = next(input_reader)
    for row in input_reader:  # for every row in the csv
        for col in row:  # for every column in said row
            for X in range(wordlist_len):  # for as long as we have words
                # if word X matches something in that column (sent to lower so
                # we don't need to worry about case)
                if wordlist[X].lower() in col.lower():
                    # write that row to the out csv
                    input_writer.writerow(row)

with open('OutWithDupes.csv', 'r', newline='') as input_sort:  # opens csv
    input_sort_reader = csv.reader(
        input_sort, delimiter='~')  # declares csv reader

    # print(input_sort)
    # attempts to sort but only 1 column WIP
    sortedlist = sorted(input_sort, key=lambda col: col[1])
    # print(sortedlist)
    # replace all , with : while delimiter is ~ so we can bring it back
    # together properly
    sortedlist = [w.replace(',', '~', 1)for w in sortedlist]
    print(row[2])
#    for row in sortedlist:
#        row[2] = datetime.datetime.strptime(row[2]+0 row[2], '%B, %d %Y')
# TODO:0 Find a way to make the dates prettier and change to 2016-08-04 Which I can then transform back
    # replace all , with : while delimiter is ~ so we can bring it back
    # together properly
    sortedlist = [x.replace(',', '')for x in sortedlist]
    print(sortedlist)
    # replace all previous ~ delimiters with commas, leaving us with a CSV
    # with the commas removed!!
    sortedlist = [y.replace('~', ',')for y in sortedlist]
    print(sortedlist)
# Formatting
with open('OutWithDupes.csv', 'w', newline='') as input_sorted:  # opens csv
    input_sort_writer = csv.writer(
        input_sorted, lineterminator='\n', escapechar=' ', quoting=csv.QUOTE_NONE)  # declares csv writer
    headers.insert(1, 'Weekday')
    for i in sortedlist:  # for the items in sortedlist
        # removes some formatting issues of \n showing up messing up the
        # formatting
        formatedlist.append(i.strip())
    for row in formatedlist:  # for every row in the formated list
        input_sort_writer.writerow([row])  # write out in a new row
        # processing finished, now a csv, cat'ing the output csv file will show
        # extra spaces that do not show up in the excel version. these are
        # needed as escape characters.

# Filters out dates
with open('OutWithDupes.csv', 'r', newline='') as date_in, open('OutDateSort.csv', 'w', newline='') as date_out:
    date_reader = csv.reader(date_in)
    date_writer = csv.writer(date_out)
    for row in date_reader:
        datekey = (row[2])
        if date_year is not ' ':
            if date_year in datekey:
                date_writer.writerow(row)
        elif date_month is not ' ':
            if date_month in datekey:
                date_writer.writerow(row)
        else:
            date_writer.writerow(row)

# # Removes duplicates based on rows 2-5 (recipient, sender, subject and
# filename)
# opens csv, declares name of the no duplicate file
with open('OutDateSort.csv', 'r', newline='') as dup_in, open(file_output, 'w', newline='') as dup_out:
    dup_reader = csv.reader(dup_in)  # declares csv reader
    dup_writer = csv.writer(dup_out)  # declares csv writer
    dup_writer.writerow(headers)
    entries = set()  # makes entries equal to a dictionary set which allows us to search based on multiple keywords
    for row in dup_reader:  # for every row in the reader
        # Using recipient, sender, subject and filename
        key = (row[3], row[4], row[5], row[6])
        if key not in entries:  # if the key is not found in that line
            dup_writer.writerow(row)  # write to the output file
            entries.add(key)  # and add to the key
#TODO: add a row at the end and figure out whhich keyword the row hit off of

#Clean-up and renaming
os.remove('OutWithDupes.csv')  # Clean-up temp files
os.remove('OutDateSort.csv')
now = datetime.datetime.now()
now_string = str(now.strftime("%Y-%m-%d_"))
os.replace(file_output, now_string + file_output)
