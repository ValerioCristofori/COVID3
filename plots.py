import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

from datetime import datetime
import numpy as np
import pandas as pd

color_grid = "grey"
color_label = "black"
min_date = '2020/01/22'
max_date = '2020/03/23'

def groupDateForMonths(ax, months):
    # Ogni 7 giorni inserisco la label nell'asse x
    fmt_half_year = mdates.MonthLocator(interval=months)
    ax.xaxis.set_major_locator(fmt_half_year)


def plotNews(df):

    # graficare andamento di New Confirmed, New Recovered e New Deaths
    # prendi input del paese da graficare
    country = input("Inserisci il nome del paese per vedere l'andamento: ")
    # if not df[df['Country'].str.contains(country)]:
    #     print("Il nome inserito non e' valido!")
    #     exit(-1)
    df_country = df[df['Country'] == country]
    x = df_country.loc[:, 'Date']

    fig, ax = plt.subplots()

    ax.plot( x, df_country.loc[:, 'New Confirmed'], "-g", label="New Confirmed")
    ax.plot( x, df_country.loc[:, 'New Recovered'], "-b", label="New Recovered")
    ax.plot( x, df_country.loc[:, 'New Deaths'], "-r", label="New Deaths")

    groupDateForMonths(ax, 1)

    plt.legend()
    plt.title("Andamento di %s " % country, color="black")
    plt.grid(color=color_grid)
    plt.ylabel("Totale", color=color_label)
    plt.xlabel("Data", color=color_label)

    plt.show()

def plotNewDeathsGlobalTrend(df):
    # gli elementi dell'asse x sono le date
    for row in range(1, len(df)):
        if df.iloc[row]["Date"] == df.iloc[0]["Date"]:
            break

    x = df.loc[0:row-1, 'Date'].tolist()

    y = []
    for j in range(0, len(x)):
        tot = 0
        for i in range(j, len(df), len(x)):
            if df.iloc[i]['Date'] == x[j]:
                tot = tot + df.iloc[i]['New Deaths']
        y.append(tot)
    fig, ax = plt.subplots()

    ax.plot(x, y, "-b", label="New Deaths")
    groupDateForMonths(ax, 1)

    plt.legend()
    plt.title("Andamento dei Nuovi Morti globali ", color="black")
    plt.grid(color=color_grid)
    plt.ylabel("Totale", color=color_label)
    plt.xlabel("Data", color=color_label)

    plt.show()

def plotBar(df):
    date = input("Inserisci la data nella forma %YYYY/%mm/%dd: ")
    df_date = df[df['Date'] == date]
    print(df_date)

    # popolo x con i paesi e le y con new confirmed, new recovered e new deaths
    x = []
    y1 = []
    y2 = []
    y3 = []

    for row in range(0, len(df_date)):
        x.append(df_date.iloc[row]['Country'])
        y1.append(df_date.iloc[row]['New Confirmed'])
        y2.append(df_date.iloc[row]['New Recovered'])
        y3.append(df_date.iloc[row]['New Deaths'])
    print(x)
    print(y1)
    print(y2)
    print(y3)

    # se commento la parte dei subplots viene un grafico con tutti e tre i valori insieme sulla stessa colonna

    fig, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4)
    ax1.plot(x, y1, "-g", label="New Confirmed")
    ax2.plot(x, y2, "-b", label="New Recovered")
    ax3.plot(x, y3, "-r", label="New Deaths")

    plt.bar(x, y1, label="New Confirmed")
    plt.bar(x, y2, label="New Recovered")
    plt.bar(x, y3, label="New Deaths")
    x_pos = np.arange(len(x))
    plt.xticks(x_pos, x)

    plt.title("Andamento globale in data %s" % date, color="black", loc="right")
    plt.ylabel("Totale", color=color_label)
    plt.xlabel("Paese", color=color_label)

    plt.legend()

    plt.show()

def movingAverage(df):

    # costruire e graficare le medie mobili a 7, 14, 21, 28 giorni
    # inserisco una data: costruisco un array di dati (quali dati? deaths? confirmed?)

    # simple moving average = somma dei data points recenti e li divido per il periodo di tempo
    # pandas.Series.rolling()

    # per le righe con stessa data sommo i confirmed, mi interessa solo quello, nient'altro
    # l'array contiene, per ogni giorno, tutti i new confirmed nel mondo
    # array.rolling(window = x).mean().plot() e ottengo la rolling average
    # posso fare 4 grafici diversi per le 4 finestre diverse, basta chiamare ^ l'ultima funzione 4 volte con 4 x diverse

    # window = input ("Inserisci la finestra temporale: ")
    # potrebbe servire se voglio un solo grafico, oppure lascio 4 grafici con valore statico come ho fatto
    # print(df)
    df_sum = df.groupby(["Date"])["New Confirmed"].sum()
    # print(df_sum)

    ##### su questo c'ho perso tempo: il risultato e' un bel grafico ma non so se serve!

    # ho le righe con data e somma di new confirmed
    # x = []
    # y = []
    #
    # for row in df_sum.iteritems():
    #     x.append(row[0])
    #     y.append(row[1])
    # #
    # print(x)
    # print(y)

    # fig, ax = plt.subplots()
    # ax.plot(x, y, "-g", label="New Confirmed")

    ##########

    # creazione 4 grafici di medie mobili

    plt.title("Media mobile globale finestra 7 giorni", color="black", loc="right")
    plt.ylabel("New Confirmed", color=color_label)
    plt.xlabel("Data", color=color_label)
    df_sum.rolling(window=7).mean().plot()
    plt.show()

    plt.title("Media mobile globale finestra 14 giorni", color="black", loc="right")
    plt.ylabel("New Confirmed", color=color_label)
    plt.xlabel("Data", color=color_label)
    df_sum.rolling(window=14).mean().plot()
    plt.show()

    plt.title("Media mobile globale finestra 21 giorni", color="black", loc="right")
    plt.ylabel("New Confirmed", color=color_label)
    plt.xlabel("Data", color=color_label)
    df_sum.rolling(window=21).mean().plot()
    plt.show()

    plt.title("Media mobile globale finestra 28 giorni", color="black", loc="right")
    plt.ylabel("New Confirmed", color=color_label)
    plt.xlabel("Data", color=color_label)
    df_sum.rolling(window=28).mean().plot()
    plt.show()


def buildPlots(df):
    plotNews(df)
    plotNewDeathsGlobalTrend(df)
    plotBar(df)
    movingAverage(df)


def buildScatter(df):
    date = input("Inserisci la data nella forma %m/%d/%YY: ")
    # if not df[df['Country'].str.contains(country)]:
    #     print("Il nome inserito non e' valido!")
    #     exit(-1)
    x = []
    y = []
    area = []
    np.random.seed(19680801)
    colors = np.random.rand(279)
    df_date = df.filter(items=[ 'Country/Region', 'Long', 'Lat', date])
    print(df_date)
    for row in range(0, len(df_date)):
        x.append( df_date.iloc[row]['Long'])
        y.append( df_date.iloc[row]['Lat'])
        area.append( df_date.iloc[row][date])
    fig, axs = plt.subplots()

    axs.scatter( x, y, area, c=colors, label="Confirmed")

    plt.title("Situazione globale infetti in data %s" % date, color="black")
    plt.grid(color=color_grid)
    plt.ylabel("Latitudine", color=color_label)
    plt.xlabel("Longitudine", color=color_label)

    plt.show()

