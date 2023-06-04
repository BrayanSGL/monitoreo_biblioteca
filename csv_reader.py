from datetime import datetime
import csv

class CSVReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.file = None
    
    def open_file(self):
        self.file = open(self.file_path, "r")

    def close_file(self):
        if self.file:
            self.file.close()

    def read_file(self):
        if self.file:
            reader = csv.reader(self.file)
            for row in reader:
                data_type, value, timestamp = self.decode_data(row)
                print(data_type, value, timestamp)
                # Aquí puedes realizar la decodificación de acuerdo a tus necesidades
                # y enviar los datos a la base de datos y a la calculadora de estadísticas
    
    def get_humedad(self):
        if self.file:
            self.file.seek(0)  # Reiniciar la posición del archivo al inicio
            lines = self.file.readlines()
            if len(lines) > 0:
                last_line = lines[-1]
                last_line = last_line.split(",")
                last_line[-1] = last_line[-1].replace("\n", "")
                data_type, value, timestamp = self.decode_data(last_line)
                return data_type, value, timestamp
        return 0, 0, 0

    def get_temperatura(self):
        if self.file:
            self.file.seek(0)  # Reiniciar la posición del archivo al inicio
            lines = self.file.readlines()
            if len(lines) > 1:
                antepenultimate_line = lines[-2]
                antepenultimate_line = antepenultimate_line.split(",")
                antepenultimate_line[-1] = antepenultimate_line[-1].replace("\n", "")
                data_type, value, timestamp = self.decode_data(antepenultimate_line)
                return data_type, value, timestamp
        return 0, 0, 0
    
    def decode_data(self, data):
        data_type = data[0]
        value = float(data[1])
        timestamp = datetime.fromisoformat(data[2].replace("Z", "+00:00"))
        timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return data_type, value, timestamp
