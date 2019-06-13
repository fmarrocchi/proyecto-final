import xlrd
import csv
import json

"""j = {}

with open('C:/Users/scrap/Documents/Proyecto final/Proyecto/nrc_emotion_lexicon.csv') as fin:
    reader = csv.DictReader(fin)
    for record in reader:
        j[record['Spanish (es)']] = {k:v for k,v in record.items() if k != 'Spanish (es)'}
            
with open('C:/Users/scrap/Documents/Proyecto final/Proyecto/output.json','w') as fout:
    json.dump(j,fout)"""

"""with xlrd.open_workbook('C:/Users/scrap/Documents/Proyecto final/Proyecto/NRC-Emotion-Lexicon.xlsx') as wb:
    sh = wb.sheet_by_index(1)  # or wb.sheet_by_name('name_of_the_sheet_here')
    with open('C:/Users/scrap/Documents/Proyecto final/Proyecto/nrc_emotion_lexicon.csv', 'w', newline='') as f:   # open('a_file.csv', 'w', newline="") for python 3
        c = csv.writer(f)
        for r in range(sh.nrows):
            c.writerow(sh.row_values(r))"""


