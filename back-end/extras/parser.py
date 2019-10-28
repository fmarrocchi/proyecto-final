import xlrd
import csv
import json
"""
j = {}

with open('./nrc_emotion_lexicon1.csv') as fin:
    reader = csv.DictReader(fin)
    for record in reader:
        j[record['Spanish (es)']] = {k:v for k,v in record.items() if k != 'Spanish (es)'}
            
with open('./output.json','w') as fout:
    json.dump(j,fout,ensure_ascii=False)"""

"""with xlrd.open_workbook('./nrc_emotion_lexicon.xlsx') as wb:
    sh = wb.sheet_by_index(0)  # or wb.sheet_by_name('name_of_the_sheet_here')
    with open('./nrc_emotion_lexicon1.csv', 'w', newline='',encoding='utf-8') as f:   # open('a_file.csv', 'w', newline="") for python 3
        c = csv.writer(f)
        c.writerow(["Spanish (es)","Positive","Negative","Anger","Anticipation","Disgust","Fear","Joy","Sadness","Surprise","Trust"])
        for r in range(1,sh.nrows):
            c.writerow(sh.row_values(r,start_colx=1, end_colx=12))"""


