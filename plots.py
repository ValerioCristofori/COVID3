import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

from datetime import datetime
import numpy as np
import pandas as pd

def buildPlots(df):

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

    # Ogni 7 giorni inserisco la label nell'asse x
    fmt_half_year = mdates.DayLocator(interval=7)
    ax.xaxis.set_major_locator(fmt_half_year)

    plt.legend()
    plt.title("Andamento di %s " %(country), color="black")
    plt.grid(color="grey")
    plt.ylabel("Totale", color="black")
    plt.xlabel("Data", color="black")

    plt.show()
