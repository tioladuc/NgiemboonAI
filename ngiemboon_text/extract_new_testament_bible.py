from bs4 import BeautifulSoup
import requests
import csv



def prepare_data_for_csv(data, fieldnames):    
    result = []
    for key, value in data.items():
        for index in range(0, len(value)):
            
            for indexS in range(0, len(value[index]['sensecontents'])):
                result.append({'ngiemboon':value[index]['noun'], 'en':value[index]['sensecontents'][indexS]['definition_en']})
                for indexY in range(0, len(value[index]['sensecontents'][indexS]['examples'])):
                    result.append({'ngiemboon':value[index]['sensecontents'][indexS]['examples'][indexY]['dialect'], 'en':value[index]['sensecontents'][indexS]['examples'][indexY]['en']})
            #append({fieldnames[0]:value['noun'], fieldnames[1]: value['sensecontents']['definition_en']})

    return result

def save_data_as_csv(data, fieldnames):
    # Specify the output file name
    filename = 'languages_bible.csv'

    # Open the file in write mode ('w')
    # The newline='' argument prevents extra blank rows in the CSV.
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a DictWriter object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write all the data rows from the list of dictionaries
        writer.writerows(data)




def extract_bible_text(source, from_url=True):
    # Load HTML
    if from_url:
        html = requests.get(source).text
    else:
        with open(source, encoding="utf-8") as f:
            html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    chapter_div = soup.find("div", {"data-testid": "chapter-content"})
    if not chapter_div:
        return {} #raise ValueError("No div with data-testid='chapter-content' found.")

    results = {}
    # Find all span elements with a data-usfm attribute
    for verse_span in chapter_div.find_all("span", attrs={"data-usfm": True}):
        usfm_key = verse_span["data-usfm"]

        # Collect all descendant span text with class ChapterContent_content__RrUqA
        contents = verse_span.find_all("span", class_="ChapterContent_content__RrUqA")
        verse_text = "".join(c.get_text(strip=True) for c in contents)

        # Only store non-empty verses
        if verse_text.strip():
            results[usfm_key] = verse_text

    return results


# Example 1 — from live site
##urlEnglish = "https://www.bible.com/fr/bible/1/MAT.122.KJV" 
##urlDialect = "https://www.bible.com/fr/bible/299/MAT.122.NGBM"
##versesEnglish = extract_bible_text(urlEnglish, from_url=True)
##versesDialect = extract_bible_text(urlDialect, from_url=True)

dictionnaryEnglish = ["https://www.bible.com/fr/bible/1/MAT.[-].KJV",
                      "https://www.bible.com/fr/bible/1/MRK.[-].KJV",
					  
                      "https://www.bible.com/fr/bible/1/LUK.[-].KJV",
                      "https://www.bible.com/fr/bible/1/JHN.[-].KJV",
                      "https://www.bible.com/fr/bible/1/ACT.[-].KJV",
                      "https://www.bible.com/fr/bible/1/ROM.[-].KJV",
                      "https://www.bible.com/fr/bible/1/1CO.[-].KJV",
                      "https://www.bible.com/fr/bible/1/2CO.[-].KJV",
                      "https://www.bible.com/fr/bible/1/GAL.[-].KJV",
                      "https://www.bible.com/fr/bible/1/EPH.[-].KJV",
                      "https://www.bible.com/fr/bible/1/PHP.[-].KJV",
                      "https://www.bible.com/fr/bible/1/COL.[-].KJV",
                      "https://www.bible.com/fr/bible/1/1TH.[-].KJV",
                      "https://www.bible.com/fr/bible/1/2TH.[-].KJV",
                      "https://www.bible.com/fr/bible/1/1TI.[-].KJV",
                      "https://www.bible.com/fr/bible/1/2TI.[-].KJV",
                      "https://www.bible.com/fr/bible/1/TIT.[-].KJV",
                      "https://www.bible.com/fr/bible/1/PHM.[-].KJV",
                      "https://www.bible.com/fr/bible/1/HEB.[-].KJV",
					  
                      "https://www.bible.com/fr/bible/1/JAS.[-].KJV",
                      "https://www.bible.com/fr/bible/1/1PE.[-].KJV",
                      "https://www.bible.com/fr/bible/1/2PE.[-].KJV",
                      "https://www.bible.com/fr/bible/1/1JN.[-].KJV",
                      "https://www.bible.com/fr/bible/1/2JN.[-].KJV",
                      "https://www.bible.com/fr/bible/1/3JN.[-].KJV",
                      "https://www.bible.com/fr/bible/1/JUD.[-].KJV",
                      "https://www.bible.com/fr/bible/1/REV.[-].KJV",
                      ]
dictionnaryDialect = ["https://www.bible.com/fr/bible/299/MAT.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/MRK.[-].NGBM",
					  
                      "https://www.bible.com/fr/bible/299/LUK.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/JHN.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/ACT.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/ROM.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/1CO.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/2CO.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/GAL.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/EPH.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/PHP.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/COL.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/1TH.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/2TH.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/1TI.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/2TI.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/TIT.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/PHM.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/HEB.[-].NGBM",
					  
                      "https://www.bible.com/fr/bible/299/JAS.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/1PE.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/2PE.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/1JN.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/2JN.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/3JN.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/JUD.[-].NGBM",
                      "https://www.bible.com/fr/bible/299/REV.[-].NGBM",
                      ]

globalDataCSV = {}
globalDataCsvBeta = []
i = 0
while i < len(dictionnaryEnglish):
    urlEnglishBase = dictionnaryEnglish[i] 
    urlDialectBase = dictionnaryDialect[i] 
    i += 1
	
    for chapter in range(1, 2000):  
        urlEnglish = urlEnglishBase.replace("[-]", str(chapter))
        urlDialect = urlDialectBase.replace("[-]", str(chapter))
        
        versesEnglish = extract_bible_text(urlEnglish, from_url=True)
        versesDialect = extract_bible_text(urlDialect, from_url=True)
        if( len(versesEnglish) == 0 ):
            break
        print( len(versesEnglish), "=>", len(versesDialect), " ::: ", urlEnglish, "=>", urlDialect)
        
        for k, v in versesDialect.items():
            if(k in versesEnglish):
                globalDataCSV[k] = v + "****" + versesEnglish[k]
                globalDataCsvBeta.append({'ngiemboon': v, 'en': versesEnglish[k]})
            


fieldnames = ['ngiemboon', 'en']
save_data_as_csv(globalDataCsvBeta, fieldnames)
print("FIN")
    