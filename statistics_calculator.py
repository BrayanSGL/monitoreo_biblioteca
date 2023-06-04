import numpy as np
import pandas as pd


class StatisticsCalculator:
    def __init__(self, path_data):
        self.path_data = path_data
        self.columns_names = ['data_type', 'value', 'timestamp']

    def load_statistics(self):
        self.table = pd.read_csv(self.path_data, names=self.columns_names, sep=',', header=None)
        self.table = self.table.dropna()  # Eliminamos los valores nulos
        #en la tabla solo nos interesa la columna de los valores col 1 y su tipo col 0
        self.table = self.table.drop(columns=['timestamp'])  # Eliminamos la columna de timestamp
        #print(self.table.tail(5))#imprimimos los primeros 5 valores de la tabla


    def calculate_statistics_temperature(self):
        # Filtramos solo los valores de temperatura
        temperature = self.table.loc[self.table['data_type'] == 'temp']
        
        if temperature.empty:
            # No hay valores de temperatura en el DataFrame
            self.mean_temperature = np.nan
            self.std_temperature = np.nan
            self.max_temperature = np.nan
            self.min_temperature = np.nan
        else:
            # Calculamos las estadísticas
            statistics = temperature['value'].describe()
            self.mean_temperature = round(statistics['mean'], 2)
            self.std_temperature = round(statistics['std'], 2)
            self.max_temperature = round(statistics['max'], 2)
            self.min_temperature = round(statistics['min'], 2)

        return self.mean_temperature, self.std_temperature, self.max_temperature, self.min_temperature
    
    def calculate_statistics_humidity(self):
        # Filtramos solo los valores de temperatura
        humidity = self.table.loc[self.table['data_type'] == 'hume']
        
        if humidity.empty:
            # No hay valores de temperatura en el DataFrame
            self.mean_humidity = np.nan
            self.std_humidity = np.nan
            self.max_humidity = np.nan
            self.min_humidity = np.nan
        else:
            # Calculamos las estadísticas
            statistics = humidity['value'].describe()
            self.mean_humidity = round(statistics['mean'], 2)
            self.std_humidity = round(statistics['std'], 2)
            self.max_humidity = round(statistics['max'], 2)
            self.min_humidity = round(statistics['min'], 2)

        return self.mean_humidity, self.std_humidity, self.max_humidity, self.min_humidity
    

