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


def buildPlots(df):
    plotNews(df)
    plotNewDeathsGlobalTrend(df)


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

