import petl as etl
import requests
import os.path

from os import path
from petl import *
from plots import *


def createPetlTables():
    arrayUrls = [
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Confirmed_archived_0325.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Deaths_archived_0325.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Recovered_archived_0325.csv']
    arrayTables = []

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


def parseTables(table, headers):

    newTable = [['Country', 'Date', headers[0], headers[1]]]



    for j in range(len(header(table))):
        headerValue = header(table)[j]
        if headerValue == 'Country/Region':
            break


    for i in range(1, len(table)):
        for datecount in range(j + 1, len(header(table))):
            if table[i][datecount] != '':
                if datecount == j + 1:
                    newRow = [table[i][j], reformatDate(table[0][datecount]), int(table[i][datecount]), int(table[i][datecount])]
                else:
                    newRow = [table[i][j], reformatDate(table[0][datecount]),
                              int(table[i][datecount]), int(table[i][datecount]) - int(table[i][datecount-1])]
                print( newRow )
                print(" append " + table[i][j] + " date " + reformatDate(table[0][datecount]))
            else:
                newRow = [table[i][j], reformatDate(table[0][datecount]), 0, 0]
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



def getData():

    if not path.exists('output.csv'):
        header = [ ['Confirmed', 'New Confirmed'], ['Recovered', 'New Recovered'], ['Deaths', 'New Deaths'] ]
        outputTables = []

        tables = createPetlTables()
        for i in range( len(tables) ):
            table = etl.cutout(tables[i], 'Lat', 'Long')
            outputTables.append(parseTables(table, header[i]))

        #join tra le tre tabelle
        firstJoinTable = etl.join(outputTables[2], outputTables[1], key=['Country','Date'])
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