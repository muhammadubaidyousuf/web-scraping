#Developer ubaid ahmed
#Email ubaidahmedmeo@gmail.com
# -----------------------------------------------------------------------------------
from requests_html import HTMLSession
import csv, time, datetime, random
import pandas as pd

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"}
date = datetime.datetime.now().strftime("%Y-%m-%d")

# Keywords file
inputfile = '' #Input keyword file
CSV = []
count = 0
with open(inputfile) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    #skip first row
    next(csv_reader)
    for keywords in csv_file:
        keywords = keywords.replace(" ", "+")
        url = f'https://www.google.com/search?q=allintitle:{keywords}'
        try:
            session = HTMLSession()
            r = session.get(url, headers=headers)
            about = r.html.find('#result-stats')
            if about:
                for ab in about:
                    results = ab.text.split(' ', 2)
                    if "About" in results:
                        results = ab.text.split(' ', 2)[1]
                        print(count, keywords, results)
                        append_csv = {"Keywords":keywords, "Total Result":results}
                        CSV.append(append_csv)
                        count += 1
                    else:
                        results = ab.text.split(' ', 2)[0]
                        print(count, keywords, results)
                        append_csv = {"Keywords":keywords, "Total Result":results}
                        CSV.append(append_csv)
                        count += 1
            else:
                append_csv = {"Keywords":keywords, "Total Result":"search result not found!"}
                CSV.append(append_csv)
                print(f"{count} {keywords} : search result not found!")
        except:
            append_csv = {"Keywords":keywords, "Total Result":"search result not found!"}
            CSV.append(append_csv)
            print("search result not found!")
# save file 
df = pd.DataFrame(CSV)
df.to_csv(f"{date} Total {count} result.csv")