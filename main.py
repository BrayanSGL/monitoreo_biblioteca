from setup import CSV_PATH, HOST, PORT, PASSWORD
from csv_reader import CSVReader
from statistics_calculator import StatisticsCalculator
from redis_conector import RedisConector

import time

class Main: 
    def __init__(self):
        pass

    def main(self):
        # crear instancias
        csv_reader = CSVReader(CSV_PATH)
        #time_series_db = TimeSeriesDatabase('localhost', 6379)
        statistics_calculator = StatisticsCalculator(CSV_PATH)
        #grafana_connector = GrafanaConnector('localhost', 3000)
        redis_conector = RedisConector(HOST, PORT, PASSWORD)
        redis_conector.connect()
        redis_conector.create_time_series('temp')
        redis_conector.create_time_series('hume')
        
        try:

            while True:
                statistics_calculator.load_statistics()
                csv_reader.open_file()
                data_type, value, timestamp = csv_reader.get_data()

                #redis_conector.add_data_time_series(data_type, value)

                print(data_type, value, timestamp)
                
                mean_temperature, std_temperature, max_temperature, min_temperature = statistics_calculator.calculate_statistics_temperature()
                mean_humidity, std_humidity, max_humidity, min_humidity = statistics_calculator.calculate_statistics_humidity()

                print(mean_temperature, std_temperature, max_temperature, min_temperature)
                print(mean_humidity, std_humidity, max_humidity, min_humidity)
                
                time.sleep(3)

        finally:
            csv_reader.close_file()
            redis_conector.close_connection()

    
if __name__ == "__main__":
    Main().main()