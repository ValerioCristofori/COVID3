import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

from datetime import datetime
import numpy as np
import pandas as pd

color_grid = "grey"
color_label = "black"


def groupDateForDays(ax, days):
    # Ogni 7 giorni inserisco la label nell'asse x
    fmt_half_year = mdates.DayLocator(interval=days)
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

    groupDateForDays(ax, 7)

    plt.legend()
    plt.title("Andamento di %s " %(country), color="black")
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
    groupDateForDays(ax, 7)

    plt.legend()
    plt.title("Andamento dei Nuovi Morti globali ", color="black")
    plt.grid(color=color_grid)
    plt.ylabel("Totale", color=color_label)
    plt.xlabel("Data", color=color_label)

    plt.show()


def buildPlots(df):
    plotNews(df)
    plotNewDeathsGlobalTrend(df)
