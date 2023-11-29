#define CHANNEL 1

esp_now_peer_info_t slave;

bool slaveFound = 0;

/************************************
* scan for a slave in AP mode
*************************************/
void Scan_for_slave() {
  Serial.println("Scanning for slave.....\n");
  int8_t results = WiFi.scanNetworks();
  slaveFound = 0;
  memset(&slave, 0, sizeof(slave));

  if (!results) {
    Serial.println("No WiFi devices found in AP mode");
    return;
  }

  /* scan through each wifi access point in the area */
  for (int i = 0; i < results; i++) {
    String SSID = WiFi.SSID(i);
    String BSSIDstr = WiFi.BSSIDstr(i);

    //slave to be found
    if (SSID.indexOf("Hub") == 0) {
      Serial.println(".......found the slave");
      slaveFound = 1;
      //save mac address into slave.peer_addr
      int mac[6];
      if (6 == sscanf(BSSIDstr.c_str(), "%x:%x:%x:%x:%x:%x", &mac[0], &mac[1], &mac[2], &mac[3], &mac[4], &mac[5])) {
        for (int j = 0; j < 6; j++) {
          slave.peer_addr[j] = (uint8_t)mac[j];
        }
      }

      //record slave parameters
      slave.channel = CHANNEL;
      slave.encrypt = 0;
      break;  //slave found so break out of for loop
    }
  }

  if (esp_now_add_peer(&slave) != ESP_OK) {
    Serial.println("Failed to add peer");
  }

  WiFi.scanDelete();
}

/************************************
* callback send function
*************************************/
void OnDataSent(const uint8_t* mac_addr, esp_now_send_status_t status) {
  /* Print who the data was sent to */
  char macStr[18];
  snprintf(macStr, sizeof(macStr), "%02x:%02x:%02x:%02x:%02x:%02x",
           mac_addr[0], mac_addr[1], mac_addr[2], mac_addr[3], mac_addr[4], mac_addr[5]);
  Serial.print("\nLast Packet Sent to: ");
  Serial.println(macStr);

  if (status != ESP_NOW_SEND_SUCCESS) {
    Serial.println("Delivery Fail");
    slaveFound = 0;
    return;
  }
  Serial.println("Delivery Success");

  //Serial.println(status == ESP_NOW_SEND_SUCCESS ? "Delivery Success" : "Delivery Fail");
}
