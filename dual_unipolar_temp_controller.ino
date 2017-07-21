#include <analogShield.h>

#define UNO_ID "DUAL_TEMP_CO_0\r\n"
#define GATE_VOLTAGE_MIN 1.5
#define GATE_VOLTAGE_MAX 3.0

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

  unsigned int gate_voltage0;
  unsigned int gate_voltage1;

  int error_signal0;
  int error_signal1;

  float accumulator0;
  float accumulator1;

  float dt_seconds;
  
};

Params params;
Logger logger;

bool top_clip0, top_clip1;
bool bot_clip0, bot_clip1;

unsigned long current_time;

float accumulator_small0;
float accumulator_small1;
float prop_term0;
float prop_term1;

unsigned int n_accum0;

#define N_ACCUM_MAX 100

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

  logger.accumulator0 = 0.0;
  logger.accumulator1 = 0.0;
  
  accumulator_small0 = 0.0;
  accumulator_small1 = 0.0;
  prop_term0 = 0.0;
  prop_term1 = 0.0;

  analog.write(params.set_temp0, params.set_temp1,
               logger.gate_voltage0,logger.gate_voltage1,
               true);

   current_time = micros();  

   top_clip0 = false;
   top_clip1 = false;
   bot_clip0 = false;
   bot_clip1 = false;

   n_accum0 = 0;
}

// note heating thermistor makes the voltage negative
void loop() {
  float previous_time = current_time;
  current_time = micros();
  logger.dt_seconds = ((float)(current_time - previous_time))*1e-6;
  
  if(Serial.available())
    parseSerial();

  logger.error_signal0 = analog.read(0, true) - ZEROV;
  logger.error_signal1 = analog.read(2, true) - ZEROV;
  
  if(params.enable0) {
    float error_signal_0_float = ((float) logger.error_signal0)*5.0/ZEROV;
    accumulator_small0 += error_signal_0_float*logger.dt_seconds;
    n_accum0 += 1;
    if(n_accum0 > N_ACCUM_MAX) {
      n_accum0 = 0;
      logger.accumulator0 += accumulator_small0*params.prop_gain0*params.pi_pole0;
      accumulator_small0 = 0;
    }

    prop_term0 = 0.99*prop_term0 + 0.01*(error_signal_0_float*params.prop_gain0);
    
    float gv0 = logger.accumulator0 + prop_term0;
    
    if (gv0 > GATE_VOLTAGE_MAX) {
      top_clip0 = true;
      gv0 = GATE_VOLTAGE_MAX;
      logger.accumulator0 = gv0;
    }
    else {
      top_clip0 = false;
    }
    
    if (gv0 < GATE_VOLTAGE_MIN) {
      bot_clip0 = true;
      gv0 = GATE_VOLTAGE_MIN;
      logger.accumulator0 = gv0;
    }
    else {
      bot_clip0 = false;
    }
    
    logger.gate_voltage0 = toBits(gv0);
   
  }
  else{
    logger.gate_voltage0 = toBits(GATE_VOLTAGE_MIN);
    logger.accumulator0 = 0.0;
  }

  if(params.enable1) {
    float error_signal_1_float = (float) logger.error_signal1;    
  }
  else{
    logger.gate_voltage1 = toBits(GATE_VOLTAGE_MIN);
    logger.accumulator1 = 0.0;
    
  }
  
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


