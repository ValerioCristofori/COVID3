import petl as etl
import requests
import re

from os import path
from petl import *
from plots import *

arrayUrls = [
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv']
index_date = 0
index_country_name = 0



def createPetlTables():
    arrayTables = []
    # creazione di tre file temporanei
    with requests.Session() as s:
        for i in range(len(arrayUrls)):
            filename = 'temp'+str(i)+'.csv'
            req = s.get(arrayUrls[i])
            url_content = req.content
            csv_file = open(filename, 'wb')
            csv_file.write(url_content)
            arrayTables.append(etl.fromcsv(filename))


    return arrayTables

'''
Ritorna la data formattata come yyyy/mm/dd
'''
def reformatDate(date):
    tokens = date.split("/")
    month = tokens[0]
    day = tokens[1]
    if len(month) == 1:
        month = '0' + month
    if len(day) == 1:
        day = '0' + day
    return '20' + tokens[2] + '/' + month + '/' + day


def getIndexHeader(table):
    global index_country_name
    global index_date
    for i in range(len(header(table))):
        headerValue = header(table)[i]
        # cerco la l'ultima colonna prima delle date
        if headerValue == 'Country/Region':
            break
    index_country_name = i

    for j in range(len(header(table))):
        headerValue = header(table)[j]
        match = re.search(r'(\d+/\d+/\d+)', headerValue)
        # cerco la l'ultima colonna prima delle date
        if match:
            break
    index_date = j

def parseTables(table, headers):

    newTable = [['Country', 'Date', headers[0], headers[1]]]

    for i in range(1, len(table)):
        for datecount in range(index_date, len(header(table))):
            if table[i][datecount] != '':
                if datecount == index_date:
                    last_value = int(table[i][datecount])
                    newRow = [table[i][index_country_name], reformatDate(table[0][datecount]), int(table[i][datecount]), int(table[i][datecount])]
                else:
                    # controllo se la entry ha valore minore di quella precedente
                    sub = int(table[i][datecount]) - last_value
                    if sub < 0:
                        # il dataset risulta inesatto
                        # la entry successiva ha valori minori di quella precedente
                        # value sono i 'confirmed' o 'deaths' o 'recovered' totali
                        value = last_value
                        # new value e' il valore dei rispettivi nuovi
                        newValue = 0

                        last_value = int(table[i][datecount-1])
                    else:
                        value = int(table[i][datecount])
                        last_value = value
                        newValue = sub

                    newRow = [table[i][index_country_name], reformatDate(table[0][datecount]),
                              value, newValue]

                print( newRow )
            else:
                newRow = [table[i][index_country_name], reformatDate(table[0][datecount]), 0, 0]
                print(newRow)
            newTable.append(newRow)
    # eliminare tutti i duplicati dati dalle regioni differenti dello stesso paese
    result = etl.rowreduce( newTable, key=['Country','Date'], reducer=doublesumbar, header=['Country', 'Date', headers[0], headers[1]])

    # ordino la tabella per country
    etl.sort(result, key=['Country', 'Date'])

    return result

def doublesumbar(key, rows):
    row2 = 0
    row3 = 0
    for row in rows:
        row2 = row2 + int(row[2])
        row3 = row3 + int(row[3])
    return [key[0], key[1], row2, row3]

def peltToPandas(datasetResult):
    dataframe = pd.DataFrame(datasetResult)
    return dataframe


def getDataframeScatter(table):
    if not path.exists('output_scatter.csv'):
        dataframe = peltToPandas(table)
        dataframe.to_csv('output_scatter.csv', index=False)
        lines = open('output_scatter.csv', 'r').readlines()
        del lines[0]
        open('output_scatter.csv', 'w').writelines(lines)
        dataframe = pd.read_csv('output_scatter.csv')
    else:
        dataframe = pd.read_csv('output_scatter.csv')
    return dataframe


def getData():

    header = [['Confirmed', 'New Confirmed'], ['Deaths', 'New Deaths'], ['Recovered', 'New Recovered']]
    outputTables = []

    tables = createPetlTables()
    getIndexHeader(tables[0])

    if not path.exists('output.csv'):

        for i in range( len(tables) ):
            outputTables.append(parseTables(tables[i], header[i]))

        #join tra le tre tabelle
        firstJoinTable = etl.join(outputTables[1], outputTables[2], key=['Country','Date'])
        datasetResult = etl.join(outputTables[0], firstJoinTable, key=['Country', 'Date'])

        dataframe = peltToPandas(datasetResult)
        dataframe.to_csv('output.csv', index=False)
        # cancello la prima riga del file caricandolo in memoria direttamente
        # la prima riga 0,1,2,3 e' dovuta alla trasformazione in petl table
        lines = open('output.csv', 'r').readlines()
        del lines[0]
        open('output.csv', 'w').writelines(lines)
        dataframe = pd.read_csv('output.csv')
    else:
        dataframe = pd.read_csv('output.csv')


    buildPlots(dataframe)
    dataframeScatter = getDataframeScatter(tables[0])
    buildScatter(dataframeScatter)