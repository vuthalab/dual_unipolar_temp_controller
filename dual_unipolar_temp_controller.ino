#include <analogShield.h>

#define UNO_ID "DUAL_TEMP_CO_0\r\n"

#define ZEROV 32768 //Zero volts

struct Params {
  unsigned int enable0;
  unsigned int set_temp0;
  float prop_gain0;
  float pi_pole0;
  float pd_pole0;

  unsigned int enable1;
  unsigned int set_temp1;
  float prop_gain1;
  float pi_pole1;
  float pd_pole1;
  
};

struct Logger {
  unsigned int act_temp0;
  unsigned int act_temp1;

  unsigned int gate_voltage0;
  unsigned int gate_voltage1;

  int error_signal0;
  int error_signal1;
  
};

Params params;
Logger logger;

float toVoltage(unsigned int bits) {
  return ((float)(bits-ZEROV))/6553.6; // Convert a number of bits 0<b<65536 to a voltage -5V<V<5V 
}

unsigned int toBits(float voltage) {
  return voltage*6553.6+ZEROV; // Convert a voltage -5V<V<5V to a number of bits 0<b<65536
}

void setup() {
  SPI.setClockDivider(SPI_CLOCK_DIV2);
  /* Open serial communications, initialize output ports: */
  Serial.begin(115200);

  logger.gate_voltage0 = ZEROV;
  logger.gate_voltage1 = ZEROV;

  params.set_temp0 = ZEROV;
  params.set_temp1 = ZEROV;

  analog.write(params.set_temp0, params.set_temp1,
               logger.gate_voltage0,logger.gate_voltage1,
               true);
}

// note heating thermistor makes the voltage negative
void loop() {
  if(Serial.available())
    parseSerial();
  
  logger.act_temp0 = analog.read(0, false);
  logger.act_temp1 = analog.read(2, false);

  logger.error_signal0 = analog.read(0, false) - ZEROV;
  logger.error_signal1 = analog.read(2, true) - ZEROV;
  
  analog.write(params.set_temp0, params.set_temp1,
               logger.gate_voltage0,logger.gate_voltage1,
               true);
}


void parseSerial() {
  char byte_read = Serial.read();
  if(byte_read == 'g') {
    // get params, send the entire struct in one go
    Serial.write((const uint8_t*)&params, sizeof(Params));
  
  }
  if(byte_read == 'l') {
    // send the logger data
    Serial.write((const uint8_t*)&logger, sizeof(Logger));
  
  }
  if(byte_read == 'i') {
    // return ID
    Serial.write(UNO_ID);
  
  }
  if(byte_read == 's') {
    // read in size(Params) bytes
    Params params_temp;
    int bytes_read = Serial.readBytes((char *) &params_temp, sizeof(Params));
    // check for validity of parameters
    params = params_temp;
  }
}


