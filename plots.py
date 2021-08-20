import matplotlib.pyplot as plt
import pandas as pd

def buildPlots(dataframe):

    # graficare andamento di New Confirmed, New Recovered e New Deaths
    plt.figure(figsize=(20, 10))
    plt.plot(dataframe, label="Andamento dati")
    plt.show()


    # graficare andamento di New Deaths rispetto le date
    plt.figure(figsize=(20,10))
    plt.plot(dataframe.loc[:,'Date'], dataframe.loc[:,'New Deaths'], label="Andamento New Deaths")
    plt.show()