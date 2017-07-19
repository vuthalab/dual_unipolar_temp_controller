#include <analogShield.h>

struct Params {
  float act_temp0;
  float act_temp1;

  float set_temp0;
  float set_temp1;

  float gate_voltage0;
  float gate_voltage1;
  
} params;

unsigned int zerov = 32768; //Zero volts

float toVoltage(unsigned int bits) {
  return ((float)(bits)-32768)/6553.6; // Convert a number of bits 0<b<65536 to a voltage -5V<V<5V 
}

float toBits(float voltage) {
  return voltage*6553.6+32768; // Convert a voltage -5V<V<5V to a number of bits 0<b<65536
}

void setup() {
  SPI.setClockDivider(SPI_CLOCK_DIV2);
  /* Open serial communications, initialize output ports: */
  Serial.begin(115200);

  params.gate_voltage0 = 0.0;
  params.gate_voltage1 = 0.0;

  params.set_temp0 = 0.0;
  params.set_temp1 = 0.0;

  analog.write(toBits(params.set_temp0), toBits(params.set_temp1),
               toBits(params.gate_voltage0),toBits(params.gate_voltage1),
               true);
}

// note heating thermistor makes the voltage negative
void loop() {
  // put your main code here, to run repeatedly:
  params.act_temp0 = toVoltage(analog.read(0, true));
  params.act_temp1 = toVoltage(analog.read(2, true));

  analog.write(toBits(params.set_temp0), toBits(params.set_temp1),
               toBits(params.gate_voltage0),toBits(params.gate_voltage1),
               true);

  
  Serial.print("\n\n");
  Serial.print(params.act_temp0);
  Serial.print("\n");
  Serial.print(params.act_temp1);
}
