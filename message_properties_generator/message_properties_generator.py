import csv
'''
Example spreadsheet: https://docs.google.com/spreadsheets/d/1afrIzI2mG9L6f8nogGRo913M767LKUTaKcWwN0-WeBY/edit?usp=sharing
Fill the spreadsheet with keys/translations, then download as a tsv file.
Copy file to root folder of this project and run this script.
Make sure the correct filename is used in the script.
The output is a list of keys/translations that can be copied to message.properties in cms
'''
def main():
    tsv_file = open("translations.tsv")
    read_tsv = csv.reader(tsv_file, delimiter="\t")

    rows = []

    for row in read_tsv:
        print(row)
        rows.append(row)


    keys = rows[0]
    for i in range(1,len(rows)):
        locale_row = rows[i]
        locale = locale_row[0]
        print(locale)
        for j in range(1, len(keys)):
            print(f'{keys[j]}= {locale_row[j]}')
        print('\n\n')
    tsv_file.close()

if __name__ == "__main__":
    main()
