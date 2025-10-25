from bs4 import BeautifulSoup
import requests
import csv
#import deep_translator

# In virtual environment
# pip install deep_translator
from deep_translator import GoogleTranslator
Translator = GoogleTranslator(source='fr', target='en') # Translator.translate(text)

# pip install googletrans==4.0.0-rc1
# from deep_translator import Translator


def extract_span_text_from_class(span_info, class_name):
    if span_info.find("span", class_=class_name) :
        return span_info.find("span", class_=class_name).get_text().replace('\xa0', ' ').strip()
    return ""

def extract_span_text_from_attribut_value(span_info, attrib_name, attrib_value):
    if span_info.find("span", {attrib_name:attrib_value}) :
        return span_info.find("span", {attrib_name:attrib_value}).get_text().replace('\xa0', ' ').strip()
    return ""

def extract_noun(line_dictionnary):
    base_pattern = line_dictionnary.find("span", class_="mainheadword").find("a")
    if base_pattern :
        return base_pattern.get_text()
    return ""

def extract_pronounciation(line_dictionnary):
    return extract_span_text_from_class(line_dictionnary, "pronunciation")

def extract_synonym(line_dictionnary):
    list_synonym = extract_span_text_from_class(line_dictionnary, "synonym")
    if list_synonym == "":
        return []
    return extract_span_text_from_class(line_dictionnary, "synonym").split(';')

def extract_sharedgrammaticalinfo_partofspeech(line_dictionnary):
    base_pattern_partofspeech = line_dictionnary.find("span", class_="sharedgrammaticalinfo")
    
    if base_pattern_partofspeech :
        return extract_span_text_from_class(base_pattern_partofspeech, "partofspeech")
    return ""

def extract_sharedgrammaticalinfo_morphtypes(line_dictionnary):
    base_pattern_morphtypes = line_dictionnary.find("span", class_="sharedgrammaticalinfo")
    if base_pattern_morphtypes :
        return extract_span_text_from_class(base_pattern_morphtypes, "morphtypes")
    return ""

def extract_sensecontent(line_dictionnary):
    resultat = []
    for sense in line_dictionnary.find_all("span", class_="sensecontent"):
        definition_fr = extract_span_text_from_class(sense, "definitionorgloss")
        definition_en = extract_span_text_from_class(sense, "definitionorgloss_1")
        array_example = []
        
        if definition_en == "":
            definition_en = Translator.translate(definition_fr)
                
        for example in sense.find_all("span", class_="examplescontent"):
            example_ngiemboon = extract_span_text_from_attribut_value(example, "lang", "nnh")
            example_fr = extract_span_text_from_attribut_value(example, "lang", "fr")
            example_en = extract_span_text_from_attribut_value(example, "lang", "en")

            if example_en == "":
                example_en = Translator.translate(example_fr)

            array_example.append({"dialect":example_ngiemboon, "fr":example_fr, "en":example_en})
            
        resultat.append({"definition_fr":definition_fr, "definition_en":definition_en, "examples":array_example})
    return resultat


def extract_dictionnary_text(source, from_url=True):
    results = []

    # --- Load HTML ---
    if from_url:
        html = requests.get(source).text
    else:
        with open(source, encoding="utf-8") as f:
            html = f.read()

    # --- Check for the 'no entries' message ---
    if "No entries exist starting with this letter." in html:
        #print("⚠️ No entries found in this page.")
        return []

    # --- Parse HTML ---
    soup = BeautifulSoup(html, "html.parser")

    for line_dictionnary in soup.find_all("div", class_="post"):        
        noun = extract_noun(line_dictionnary)
        pronounciation = extract_pronounciation(line_dictionnary)
        synonym = extract_synonym(line_dictionnary)
        
        sharedgrammaticalinfo_partofspeech = extract_sharedgrammaticalinfo_partofspeech(line_dictionnary)
        sharedgrammaticalinfo_morphtypes = extract_sharedgrammaticalinfo_morphtypes(line_dictionnary)
        sensecontents = extract_sensecontent(line_dictionnary)
                
        results.append({"noun":noun, "pronounciation":pronounciation, "synonym": synonym, "sharedgrammaticalinfo_partofspeech": sharedgrammaticalinfo_partofspeech, "sharedgrammaticalinfo_morphtypes": sharedgrammaticalinfo_morphtypes, "sensecontents": sensecontents})

    return results

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
    filename = 'languages.csv'

    # Open the file in write mode ('w')
    # The newline='' argument prevents extra blank rows in the CSV.
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        # Create a DictWriter object
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header row
        writer.writeheader()

        # Write all the data rows from the list of dictionaries
        writer.writerows(data)

letters = ['a','b','c','e','ɛ','f','g','h','j','k','l','m','n','ŋ','o','ɔ','p','s','t','u','v','w','y','z']
endOfPagingText = "No entries exist starting with this letter."

urlBase = "https://www.webonary.org/ngiemboon/browse/?letter=[letter]&key=nnh&totalEntries=89&lang=en&pagenr=[page]"
data = {}

for letter in letters:
    urlLetter = urlBase.replace("[letter]", letter)

    for page in range(1, 100):
        url = urlLetter.replace("[page]", str(page))
        print(url)
        temp = extract_dictionnary_text(url, True)
        #print(len(temp))
        if len(temp)==0:
            break;
        data[url] = temp

fieldnames = ['ngiemboon', 'en']
prepared_data = prepare_data_for_csv(data, fieldnames)
save_data_as_csv(prepared_data, fieldnames)
print(prepared_data)
print("FIN")
    