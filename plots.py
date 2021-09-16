import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

from datetime import datetime
import numpy as np
import pandas as pd

color_grid = "grey"
color_label = "black"
min_date = 0
max_date = 0

def minMaxDate(df):
    # trovo la prima e l'ultima data
    global min_date, max_date
    min_date = df.iloc[1]["Date"]
    max_date = df.iloc[len(df)-1]["Date"]


def checkDate(date):
    # controllo se la data in input sta nell'intervallo
    if max_date < date or date < min_date:
        raise NameError('Date Error')


def groupDateForMonths(ax, months):
    # ogni 7 giorni inserisco la label nell'asse x
    fmt_half_year = mdates.MonthLocator(interval=months)
    ax.xaxis.set_major_locator(fmt_half_year)


def plotNews(df):
    # graficare andamento di New Confirmed, New Recovered e New Deaths
    # prendo l'input del paese da graficare
    country = input("Inserisci il nome del paese per vedere l'andamento di New Confirmed, New Deaths, New Recovered: ")
    # if not df[df['Country'].str.contains(country)]:
    #     print("Il nome inserito non e' valido!")
    #     exit(-1)
    df_country = df[df['Country'] == country]
    x = df_country.loc[:, 'Date']

    fig, ax = plt.subplots()

    ax.plot( x, df_country.loc[:, 'New Confirmed'], "-g", label="New Confirmed")
    ax.plot( x, df_country.loc[:, 'New Recovered'], "-b", label="New Recovered")
    ax.plot( x, df_country.loc[:, 'New Deaths'], "-r", label="New Deaths")

    # per diminuire il numero di date sull'asse x
    # scrivo la data ogni due mesi
    groupDateForMonths(ax, 2)

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

    # sommo le New Deaths raggruppando per l'attributo Date
    y = df.groupby(["Date"])["New Deaths"].sum()
    fig, ax = plt.subplots()

    ax.plot(x, y, "-b", label="New Deaths")
    groupDateForMonths(ax, 2)

    plt.legend()
    plt.title("Andamento dei Nuovi Morti globali ", color="black")
    plt.grid(color=color_grid)
    plt.ylabel("Totale", color=color_label)
    plt.xlabel("Data", color=color_label)

    plt.show()

def plotBar(df):
    date = input("Inserisci la data nella forma %YYYY/%mm/%dd per confrontare New Confirmed, New Deaths e New Recovered di ogni paese: ")
    try:
        checkDate(date)
    except NameError:
        print("La data inserita non rientra nel range possibile")
        exit(-1)
    df_date = df[df['Date'] == date]

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
    #print(x)
    #print(y1)
    #print(y2)
    #print(y3)

    x_ticks_labels = x
    fig, (ax1, ax2, ax3) = plt.subplots(3,1, constrained_layout=True)
    x_pos = np.arange(len(x))

    ax1.bar(x_pos, y1, color = 'g', label="New Confirmed")
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(x_ticks_labels, fontsize=5, rotation=90)
    ax1.title.set_text('New Confirmed')
    ax1.set_ylabel("New Confirmed")
    ax1.legend()

    ax2.bar(x_pos, y2, color = 'b', label="New Recovered")
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(x_ticks_labels, fontsize=5, rotation=90)
    ax2.set_ylabel("New Recovered")
    ax2.legend()

    ax3.bar(x_pos, y3, color = 'r', label="New Deaths")
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(x_ticks_labels, fontsize=5, rotation=90)
    ax3.title.set_text('New Deaths')
    ax3.set_ylabel("New Deaths")
    ax3.legend()

    plt.show()

def movingAverage(df):
    # costruire e graficare le medie mobili a 7, 14, 21, 28 giorni

    # sommo i New Confirmed raggruppando per l'attributo Date
    df_sum = df.groupby(["Date"])["New Confirmed"].sum()

    # creazione 4 grafici di medie mobili

    plt.title("Media mobile globale finestra 7 giorni", color="black", loc="right")
    plt.ylabel("New Confirmed", color=color_label)
    plt.xlabel("Data", color=color_label)
    # calcolo la rolling average con la seguente funzione
    df_sum.rolling(window=7).mean().plot()
    plt.grid(color=color_grid)
    plt.show()

    plt.title("Media mobile globale finestra 14 giorni", color="black", loc="right")
    plt.ylabel("New Confirmed", color=color_label)
    plt.xlabel("Data", color=color_label)
    df_sum.rolling(window=14).mean().plot()
    plt.grid(color=color_grid)
    plt.show()

    plt.title("Media mobile globale finestra 21 giorni", color="black", loc="right")
    plt.ylabel("New Confirmed", color=color_label)
    plt.xlabel("Data", color=color_label)
    df_sum.rolling(window=21).mean().plot()
    plt.grid(color=color_grid)
    plt.show()

    plt.title("Media mobile globale finestra 28 giorni", color="black", loc="right")
    plt.ylabel("New Confirmed", color=color_label)
    plt.xlabel("Data", color=color_label)
    df_sum.rolling(window=28).mean().plot()
    plt.grid(color=color_grid)
    plt.show()


def parseDate(dateToParse):
    # Parse della data dalla forma YYYY/mm/dd alla forma m/d/YY
    tokens = dateToParse.split("/")
    year = tokens[0][2:4]
    month = tokens[1]
    day = tokens[2]
    if month[0] == "0":
        month = month[1]
    if day[0] == "0":
        day = day[1]
    return month + "/" + day + "/" + year

def buildScatter(df):
    dateToParse = input("Inserisci la data nella forma %YYYY/%mm/%dd per vedere la situazione globale di Confirmed: ")
    try:
        checkDate(dateToParse)
    except NameError:
        print("La data inserita non rientra nel range possibile")
        exit(-1)
    date = parseDate(dateToParse)
    x = []
    y = []
    area = []
    np.random.seed(19680801)
    colors = np.random.rand(279)
    df_date = df.filter(items=[ 'Country/Region', 'Long', 'Lat', date])
    #print(df_date)
    #creo array per salvare i valori di ogni punto dato da longitudine e latitudine
    for row in range(0, len(df_date)):
        x.append( df_date.iloc[row]['Long'])
        y.append( df_date.iloc[row]['Lat'])
        area.append( df_date.iloc[row][date]*0.001) #0.001 per diminuire la scala e rendere il grafico leggibile
    fig, axs = plt.subplots()

    axs.scatter( x, y, area, c=colors, label="Confirmed")

    plt.title("Situazione globale infetti in data %s" % date, color="black")
    plt.grid(color=color_grid)
    plt.ylabel("Latitudine", color=color_label)
    plt.xlabel("Longitudine", color=color_label)

    plt.show()


def buildPlots(df):
    #
    minMaxDate(df)
    plotNews(df)
    plotNewDeathsGlobalTrend(df)
    plotBar(df)
    movingAverage(df)
