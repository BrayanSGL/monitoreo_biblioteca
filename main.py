from setup import CSV_PATH, HOST, PORT, PASSWORD
from csv_reader import CSVReader
from statistics_calculator import StatisticsCalculator
from redis_conector import RedisConector

import time

class Main: 
    def __init__(self):
        self.is_running = True

    def main(self):
        # crear instancias
        csv_reader = CSVReader(CSV_PATH)
        statistics_calculator = StatisticsCalculator(CSV_PATH)
        redis_conector = RedisConector(HOST, PORT, PASSWORD)
        redis_conector.connect()
        redis_conector.create_time_series('temp')
        redis_conector.create_time_series('hume')
        #teperatura
        redis_conector.create_time_series('temp_mean')
        redis_conector.create_time_series('temp_std')
        redis_conector.create_time_series('temp_max')
        redis_conector.create_time_series('temp_min')
        #humedad
        redis_conector.create_time_series('hume_mean')
        redis_conector.create_time_series('hume_std')
        redis_conector.create_time_series('hume_max')
        redis_conector.create_time_series('hume_min')

        
        try:

            while self.is_running:
                statistics_calculator.load_statistics()
                csv_reader.open_file()

                #tempetura real time
                data_type_t, value_t, timestamp_t = csv_reader.get_temperatura()
                redis_conector.add_data_time_series(data_type_t, value_t)
                #humedad real time
                data_type_h, value_h, timestamp_h = csv_reader.get_humedad()
                redis_conector.add_data_time_series(data_type_h, value_h)

                
                mean_temperature, std_temperature, max_temperature, min_temperature = statistics_calculator.calculate_statistics_temperature()
                mean_humidity, std_humidity, max_humidity, min_humidity = statistics_calculator.calculate_statistics_humidity()

                redis_conector.add_data_time_series('temp_mean', mean_temperature)
                redis_conector.add_data_time_series('temp_std', std_temperature)
                redis_conector.add_data_time_series('temp_max', max_temperature)
                redis_conector.add_data_time_series('temp_min', min_temperature)

                redis_conector.add_data_time_series('hume_mean', mean_humidity)
                redis_conector.add_data_time_series('hume_std', std_humidity)
                redis_conector.add_data_time_series('hume_max', max_humidity)
                redis_conector.add_data_time_series('hume_min', min_humidity)

                print(data_type_t, value_t, timestamp_t)
                print(data_type_h, value_h, timestamp_h)
                print(mean_temperature, std_temperature, max_temperature, min_temperature)
                print(mean_humidity, std_humidity, max_humidity, min_humidity)
                
                time.sleep(3)

        finally:
            csv_reader.close_file()
            redis_conector.close_connection()

    
if __name__ == "__main__":
    Main().main()