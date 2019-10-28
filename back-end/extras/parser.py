import xlrd
import csv
import json
"""
j = {}

with open('C:/Users/scrap/Documents/Proyecto final/ProyGH/proyecto-final/back-end/extras/nrc_emotion_lexicon.csv') as fin:
    reader = csv.DictReader(fin)
    for record in reader:
        j[record['Spanish (es)']] = {k:v for k,v in record.items() if k != 'Spanish (es)'}
            
with open('C:/Users/scrap/Documents/Proyecto final/ProyGH/proyecto-final/back-end/extras/output.json','w') as fout:
    json.dump(j,fout,ensure_ascii=False)"""

with xlrd.open_workbook('C:/Users/scrap/Documents/Proyecto final/ProyGH/proyecto-final/back-end/extras/nrc_emotion_lexicon.xlsx') as wb:
    sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
    with open('C:/Users/scrap/Documents/Proyecto final/ProyGH/proyecto-final/back-end/extras/nrc_emotion_lexicon.csv', 'w', newline='') as f:   # open('a_file.csv', 'w', newline="") for python 3
        c = csv.writer(f)
        for r in range(1,sh.nrows):
            c.writerow(sh.row_values(r))


