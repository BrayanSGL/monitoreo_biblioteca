#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <DHT.h>

#define DHTPIN 5
#define DHTTYPE DHT11
const int ledPin = 16;  // Número de pin del LED

char ssid[] = "Martin Router King";  // Nombre de la red Wi-Fi
const char* password = "RYbd2023";  // Contraseña de la red Wi-Fi
const char* mqtt_server = "broker.emqx.io";  // Dirección del servidor MQTT
const char* temperatura_topic = "sensores/temperatura_UD7744";  // Tema MQTT para la temperatura
const char* humedad_topic = "sensores/humedad_UD7744";  // Tema MQTT para la humedad

WiFiClient espClient; // Cliente Wi-Fi
PubSubClient mqttClient(espClient); // Cliente MQTT
DHT dhtSensor(DHTPIN, DHTTYPE); // Sensor DHT11

void setup_wifi() {
  delay(10);
  Serial.println();
  Serial.print("Conectando a ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  // Esperar a que el cliente se conecte a la red Wi-Fi
  while (WiFi.status() != WL_CONNECTED) {
    digitalWrite(ledPin, LOW);
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("Conectado a la red WiFi");
  Serial.println("Dirección IP: ");
  Serial.println(WiFi.localIP());

  // Parpadear el LED para indicar la conexión exitosa a Wi-Fi
  digitalWrite(ledPin, HIGH);  // Encender el LED
  delay(500);
  digitalWrite(ledPin, LOW);  // Apagar el LED
  delay(500);
  digitalWrite(ledPin, HIGH);  // Encender el LED
}

void reconnect() {
  // Esperar a que el cliente se conecte al servidor MQTT
  while (!mqttClient.connected()) {
    Serial.print("Conectando al servidor MQTT...");
    String clientId = "ESP8266Client-";
    clientId += String(random(0xffff), HEX);

    if (mqttClient.connect(clientId.c_str())) {
      Serial.println("conectado");
    } else {
      Serial.print("fallo, rc=");
      Serial.print(mqttClient.state());
      Serial.println(" intentando nuevamente en 5 segundos");
      delay(5000);
    }
  }
}

void setup() {
  pinMode(ledPin, OUTPUT);  // Configurar el pin del LED como salida
  Serial.begin(115200); // Iniciar puerto serie
  dhtSensor.begin(); // Iniciar sensor DHT11
  setup_wifi(); // Iniciar conexión Wi-Fi
  mqttClient.setServer(mqtt_server, 1883); // Iniciar servidor MQTT
}

void loop() {
  // Verificar si el cliente está conectado al servidor MQTT
  if (!mqttClient.connected()) {
    reconnect();
  }
  mqttClient.loop(); // Mantener la conexión MQTT

  float temperatura = dhtSensor.readTemperature(); // Leer temperatura
  float humedad = dhtSensor.readHumidity(); // Leer humedad

  // Verificar si se pudo leer la temperatura y la humedad
  if (isnan(temperatura) || isnan(humedad)) {
    Serial.println("Error al leer los datos del sensor DHT11");
    return;
  }

  // Publicar temperatura y humedad en el servidor MQTT
  // Cadena para almacenar la temperatura [6] = 4 digitos + punto decimal + caracter nulo
  char temperaturaStr[6];
  // dtostrf(valor, ancho, precision, cadena) se usa para convertir un valor de punto flotante a una cadena         
  dtostrf(temperatura, 4, 2, temperaturaStr);
  mqttClient.publish(temperatura_topic, temperaturaStr); // Publicar temperatura

  char humedadStr[6];
  dtostrf(humedad, 4, 2, humedadStr);
  mqttClient.publish(humedad_topic, humedadStr);

  delay(5000); // Intervalo entre lecturas y publicaciones de datos
}
