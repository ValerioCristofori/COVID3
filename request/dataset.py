import csv

import petl
import requests
from petl import *


def createPetlTables():
    arrayUrls = [
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Confirmed_archived_0325.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Deaths_archived_0325.csv',
        'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/archived_data/archived_time_series/time_series_19-covid-Recovered_archived_0325.csv']
    arrayTables = []

    with requests.Session() as s:
        for url in arrayUrls:
            req = s.get(url)
            url_content = req.content
            csv_file = open('temp.csv', 'wb')
            csv_file.write(url_content)

            arrayTables.append(petl.fromcsv('temp.csv'))
    return arrayTables


def parseTables(table, headers):

    newTable = [['Country', 'Date',headers[0], headers[1]]]

    # ordino la tabella per country
    petl.sort(newTable, key='Country/Region')

    for j in range ( len(header(table)) ):
        if header(table)[j] == 'Country/Region':
            break
    lastCountryName = ''
    for i in range( 1, len(table) ):
        # togliere i duplicati relativi piu' regioni di una stessa country
        if (table[i][j] != lastCountryName):
            # se il country name della nuova entry non e' stato gia' visto
            for datecount in range(j + 1, len(header(table))):
                if table[i][datecount] != '':
                    if datecount == j + 1:
                        newRow = [table[i][j], table[0][datecount], table[i][datecount], table[i][datecount]]
                    else:
                        newRow = [table[i][j], table[0][datecount],
                                  str(int(table[i][datecount]) + int(table[i][datecount - 1])), table[i][datecount]]
                    newTable.append(newRow)
        else:
            # e' una regione di una country gia' vista
            for datecount in range(j + 1, len(header(table))):
                if table[i][datecount] != '':
                    headerDate = table[0][datecount]
                    value = table[i][datecount]
                    headerCountryName = table[i][j]
                    # cerco nella tabella da creare per il country name e la data
                    for newRowIndex in newTable:
                        if newRowIndex[0] == headerCountryName and newRowIndex[1] == headerDate:
                            newRowIndex[2] = str( int(newRowIndex[2]) + int(value) )
                            newRowIndex[3] = str(int(newRowIndex[3]) + int(value))
        lastCountryName = table[i][j]

    return newTable

def getData():

    header = [ ['Confirmed', 'New Confirmed'], ['Recovered', 'New Recovered'], ['Deaths', 'New Deaths'] ]
    outputTables = []

    tables = createPetlTables()
    for i in range( len(tables) ):
        table = petl.cutout(tables[i], 'Lat', 'Long')
        outputTables.append(parseTables(table, header[i]))

    #join tra le tre tabelle
    firstJoinTable = petl.join(outputTables[0], outputTables[1], key=['Country','Date'])
    datasetResult = petl.join(outputTables[2], firstJoinTable, key=['Country', 'Date'])

    print(datasetResult)