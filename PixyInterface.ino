// Code for dual CC patch
//
// This code will utilize 2 CC patches and
// allow them to gather data based on each other
// This will take the raw patch data, manipulate it, and output
// the data in a more precise data set for getting the
// distance and the direction of crew member

#include <Pixy2.h>
#include "ConstructPixy.h"
#include <esp_now.h>
#include <WiFi.h>
#include "array_send.h"

Pixy2 pixy;       // initialize pixy camera construction
CalculateData data;  // initialize pixy data functions

// data values to grab each patch from pixy
unsigned long rate;
bool camDetection;
uint32_t Freq=0;

/************************************
* SETUP
*************************************/
void setup() {
  Serial.begin(115200);
  delay(500);
  setCpuFrequencyMhz(160);
  delay(500);
  Freq = getCpuFrequencyMhz();
  Serial.print("CPU Freq = ");
  Serial.print(Freq);
  Serial.println(" MHz");
  delay(500);
  WiFi.mode(WIFI_STA);  //set up wifi as station
  delay(500);
  
  // initialize ESP
  if (esp_now_init() != ESP_OK) {
    Serial.println("ERROR initializing ESP-NOW");
    return;
  }

  //register call back function
  esp_now_register_send_cb(OnDataSent);
  //Scan_for_slave();

  
  // if (esp_now_add_peer(&slave) != ESP_OK) {
  //   Serial.println("Failed to add peer");
  //   return;
  // }
  Serial.println("INITIALIZING PIXY");
  pixy.init();
  delay(500);
  rate = millis();

  // setting up signatures
  for (int i; i < CREW; i++) {
    patch[i].sig = signatures[i];
  }
  
}

/****************************
* LOOP
*****************************/
void loop() {
  int i;
  int j;
  int count = 0;
  unsigned long timePassed = millis();  // reset timePassed to 0

  // reset patch count and detection
  data.resetPatchCount();
  camDetection = false;
  
  //
  // get blocks for one second
  //
  while ((timePassed - rate) < 1000) {
    pixy.ccc.getBlocks();
    if (pixy.ccc.numBlocks) {

      //iterates through all blocks detected
      for (i = 0; i < pixy.ccc.numBlocks; i++) {
        // Serial.print("Signature: ");
        // Serial.println(sig);
        // pixy.ccc.blocks[i].print();
        // compile patch data per frame by signature and assign to patch data arrays
        // uint8_t curIdx = pixy.ccc.blocks[i].m_index;
        int curSig = pixy.ccc.blocks[i].m_signature;
        for (j = 0; j < CREW; j++) {
          count = patch[j].count;

          if (curSig == patch[j].sig) {
            //patch[j].height[count] = (uint8_t)pixy.ccc.blocks[i].m_height;
            //patch[j].width[count] = pixy.ccc.blocks[i].m_width;
            patch[j].index = pixy.ccc.blocks[i].m_index;
            patch[j].angle[count] = pixy.ccc.blocks[i].m_angle;
            patch[j].x[count] = pixy.ccc.blocks[i].m_x;
            patch[j].y[count] = pixy.ccc.blocks[i].m_y;
            patch[j].detected = true;
            camDetection = true;

            if (count < (MINFRAMES - 1)) {
              patch[j].count++;
            }
            break;
          }
        }
      }
    }
    timePassed = millis();  // increment timePassed in loop
  }

  // prepare data for transmission
  for (j = 0; j < CREW; j++) {
    data.left_or_right(j);
    // data.patchToData(j);
  }

  // data.printPatchData(1);
  if (!slaveFound) {
    Scan_for_slave();
  }

  //there was a block detected and there's a slave to receive
  if (camDetection && slaveFound) {
    // data.printData();
    esp_err_t result = esp_now_send(slave.peer_addr, (uint8_t*)data.cm, sizeof(data.cm));
    if (result != ESP_OK) {
      Serial.print("\n");
      Serial.println("\nERROR: SOMETHING WENT WRONG\n");
    }
  }
  

  rate = millis();  // reset rate for clock
}
