from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import json
import pandas as pd

driver = webdriver.Chrome('chromedriver.exe')

def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()

#Until now, the code was to show the progress o the program

def getNamePhone(site):
    driver.get(site)
    test = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.XPATH, '//*[@id="__REDUX_STATE__"]'))).get_attribute("innerHTML")
    jsondata = str(test).replace("\\u0022", '"')
    newDictionary = json.loads(jsondata)
    uuid = list(newDictionary['stores'].keys())[0]
    nome = newDictionary['stores'][uuid]['data']['title']
    endereco = newDictionary['stores'][uuid]['data']['location']['streetAddress']
    telefone = newDictionary['stores'][uuid]['data']['phoneNumber']
    return nome, telefone, endereco

df = pd.read_excel('links_uber.xlsx', index_col=None, header=None) #reading the excel file with the links

lista = []

total = len(df.index)

printProgressBar(0, total, prefix = 'Progress:', suffix = 'Complete', length = 50)
for index, row in df.iterrows():
    lista.append(list(getNamePhone(row[0])))
    lista[index].append(str(row[0]))
    printProgressBar(index + 1, total, prefix='Progress:', suffix='Complete', length=50)

driver.quit()
df=pd.DataFrame(lista,columns=['Nome', 'Tel','Endereço', 'Link'])
#creating the excel file with all the things that we returned
df.sort_values('Nome', inplace=True)

df.to_excel("Telefones_uber.xlsx", index=False) #creating the excel file with all the things that we returned
