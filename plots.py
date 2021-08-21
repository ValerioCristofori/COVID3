import matplotlib.pyplot as plt
import pandas as pd

def buildPlots(df):


    date_range = df.loc[:, 'Date']

    # graficare andamento di New Confirmed, New Recovered e New Deaths
    # prendi input del paese da graficare
    country = input("Inserisci il nome del paese per vedere l'andamento: ")
    # if not df[df['Country'].str.contains(country)]:
    #     print("Il nome inserito non e' valido!")
    #     exit(-1)
    plt.figure(figsize=(20, 10))
    plt.plot(date_range, df.loc[df['Country'] == country, 'New Confirmed'], label="Andamento dati 'New Confirmed'")
    plt.plot(date_range, df.loc[df['Country'] == country, 'New Recovered'], label="Andamento dati 'New Recovered'")
    plt.plot(date_range, df.loc[df['Country'] == country, 'New Deaths'], label="Andamento dati 'New Deaths'")
    plt.show()


    # graficare andamento di New Deaths rispetto le date
    plt.figure(figsize=(20,10))
    plt.plot(date_range, df.loc[:,'New Deaths'], label="Andamento New Deaths")
    plt.show()