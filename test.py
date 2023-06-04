#Verificar si hay un nuevo dato en el csv que esta en el directorio
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class MyHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == 'ruta/al/archivo.csv':
            # Aquí puedes colocar el código que deseas ejecutar cuando se modifique el archivo CSV
            print("Se ha cargado un nuevo dato al archivo CSV")

# Ruta al archivo CSV que deseas monitorear
ruta_archivo_csv = 'data.csv'

# Crear un observador y vincularlo con el manejador de eventos
observer = Observer()
event_handler = MyHandler()
observer.schedule(event_handler, path=ruta_archivo_csv, recursive=False)

# Iniciar el observador
observer.start()

try:
    # Mantener el script en ejecución para continuar monitoreando cambios
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    # Detener el observador si se presiona Ctrl+C
    observer.stop()

# Esperar a que el observador se detenga por completo
observer.join()

