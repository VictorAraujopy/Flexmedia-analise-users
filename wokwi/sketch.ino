#include <WiFi.h>
#include <HTTPClient.h>
#include <WiFiClientSecure.h> 

const char* ssid = "Wokwi-GUEST";
const char* password = "";
const char* apiHost = "https://35s4mdw1-5000.brs.devtunnels.ms//api/dados_sensor";

const int pinoPIR = 13;
const int pinoLED = 12;
const int pinoBotao = 14; 

unsigned long tempoInicio = 0;
bool emAtendimento = false;
bool satisfacaoRegistrada = false; 

void conectarWifi() {
  Serial.print("Conectando Wifi...");
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println(" Conectado!");
}

void enviarDadosAPI(int satisfacao, int duracao) {
  if (WiFi.status() == WL_CONNECTED) {
    
    WiFiClientSecure client;
    client.setInsecure(); // 
    client.setTimeout(10000); 
    HTTPClient http;
    
    Serial.print("Conectando em: ");
    Serial.println(apiHost);

    // Tenta iniciar a conexão
    if (http.begin(client, apiHost)) { 
      http.addHeader("Content-Type", "application/json");

      String json = "{\"valor_sensor\": 1,";
      json += "\"satisfacao\": " + String(satisfacao) + ",";
      json += "\"tempo_duracao\": " + String(duracao) + "}";

      Serial.println("Enviando JSON...");
      
      int httpCode = http.POST(json);

      if (httpCode == 200) {
        Serial.println("✅ SUCESSO: Dados salvos no banco!");
      } else {
        Serial.print("❌ ERRO HTTP: ");
        Serial.println(httpCode);
        if (httpCode == -1) Serial.println("⚠️ DICA: Verifique se a URL do Ngrok mudou ou se ele está fechado.");
      }
      http.end();
    } else {
      Serial.println("❌ Erro: Não foi possível alcançar o servidor (URL errada?)");
    }
  } else {
    conectarWifi();
  }
}

void setup() {
  Serial.begin(115200);
  pinMode(pinoPIR, INPUT);
  pinMode(pinoLED, OUTPUT);
  pinMode(pinoBotao, INPUT_PULLUP); 
  
  conectarWifi();
  Serial.println("\n--- SISTEMA PRONTO (HTTPS SEGURO) ---");
}

void loop() {
  int leituraPIR = digitalRead(pinoPIR);
  int leituraBotao = digitalRead(pinoBotao);
  
  // Lógica de Movimento
  if (leituraPIR == HIGH) {
    digitalWrite(pinoLED, HIGH);

    if (!emAtendimento) {
      emAtendimento = true;
      tempoInicio = millis();
      satisfacaoRegistrada = false;
      Serial.println("[SENSOR] Visitante detectado.");
    }

    // Botão de Satisfação (Memória)
    if (leituraBotao == LOW && !satisfacaoRegistrada) {
      satisfacaoRegistrada = true;
      Serial.println(">>> Satisfação registrada!");
    }
  }
  // Fim do Movimento
  else {
    digitalWrite(pinoLED, LOW);

    if (emAtendimento) {
      unsigned long tempoTotal = (millis() - tempoInicio) / 1000;
      Serial.println("[SENSOR] Visita finalizada. Enviando...");
      
      enviarDadosAPI(satisfacaoRegistrada ? 1 : 0, tempoTotal);

      emAtendimento = false;
      satisfacaoRegistrada = false;
    }
  }
  
  delay(100);
}