/*
 * Simple SCPI test for identiy and result set and get
 */
#include "Arduino.h"
#include "RCSwitch.h"
#include "Vrekrer_scpi_parser.h"

SCPI_Parser DigIOBox;
RCSwitch myRemote = RCSwitch();

// Functions for SCPI Communication
void Identify(SCPI_C commands, SCPI_P parameters, Stream& interface);
void GetAllDigIO(SCPI_C commands, SCPI_P parameters, Stream& interface);
void GetDigIO(SCPI_C commands, SCPI_P parameters, Stream& interface);
void SetDigIO(SCPI_C commands, SCPI_P parameters, Stream& interface);

// General functions
void ListenForRemote();
int GetChannel(int ch);
void SetChannel(int ch, int state);

// digital output pins
const int numOfPins = 2;
const int DOut[numOfPins] = {53, 54};  // Output pin assignment
const int LedPins[numOfPins] = {52, 53};  // Where are the LEDs?

// RF setup
const int rf_delay = 500;  // delay after remote key press (msec)
const int RFCodes[2]  {
  4543795,
  4543804
};  // Set up the RF codes for buttons on the remote
const int RFChannels[2] = {0, 1};  // Channels associated with RF codes

// version of program
const char fw_version[7] = "v0.1.0";


void setup() {
  
    // SCPI Setup
    DigIOBox.RegisterCommand(F("*IDN?"), &Identify);
    DigIOBox.RegisterCommand(F("DOut#?"), &GetDigIO);
    DigIOBox.RegisterCommand(F("DOut#"), &SetDigIO);
    DigIOBox.RegisterCommand(F("ALLDOut?"), &GetAllDigIO);

    // Output and LED setups
    for (int it = 0; it < numOfPins; it++) {
        pinMode(DOut[it], OUTPUT);
        pinMode(LedPins[it], OUTPUT);
    }

    // RF Remote setup
    myRemote.enableReceive(0);  // define interrupt remote is on
    myRemote.setPulseLength(185);
    myRemote.setRepeatTransmit(5);

    // Start serial console
    Serial.begin(9600);
}


void loop() {
    DigIOBox.ProcessInput(Serial, "\n");
    ListenForRemote();
}


void Identify(SCPI_C commands, SCPI_P parameters, Stream& interface) {
    interface.print(F("DigIOBox "));
    interface.println(fw_version);
}


void GetAllDigIO(SCPI_C commands, SCPI_P parameters, Stream& interface) {
    // ALLDOut?
    // Query all logic states of the available DOut pins
    // Return values are "1" or "0", aranged in a comma separated values list
    for (int it=0; it<numOfPins - 1; it++) {  // all but the last
        interface.print(GetChannel(it));
        interface.print(",");
    }
    // print the last
    interface.println(GetChannel(numOfPins - 1));
}


void GetDigIO(SCPI_C commands, SCPI_P parameters, Stream& interface) {
    // DOut<index>?
    // Queries the logic state of DOut[index] pin
    // Return values are "1" or "0"
    // Examples:
    //    DO4?      (Queries the state of DOut[4] pin)
    //    DOut1000?    (This does nothing as DOut[1000] does not exists)

    //Get the numeric suffix/index (if any) from the commands
    String header = String(commands.Last());

    header.toUpperCase();

    int suffix = -1;

    sscanf(header.c_str(),"%*[DO]%u", &suffix);

    //If the suffix is valid, print the pin's logic value to the interface
    if ( (suffix >= 0) && (suffix < numOfPins) ) {
        interface.println(GetChannel(suffix));
    }
}


void SetDigIO(SCPI_C commands, SCPI_P parameters, Stream& interface) {
    // DOut<index> state
    // Sets the logic state of DOut[index] pin
    // Valid states are : "HIGH", "LOW", "ON", "OFF", "1" and "0"
    // and any lowercase/uppercase combinations
    // Examples:
    //    DOut4 1  (Sets DOut[4] to HIGH)
    //    DO0 1    (Sets DOut[0] to HIGH)

    //Get the numeric suffix/index (if any) from the commands
    String header = String(commands.Last());
    header.toUpperCase();
    int suffix = -1;

    sscanf(header.c_str(),"%*[DO]%u", &suffix);

    //If the suffix is valid,
    //use the first parameter (if valid) to set the digital Output
    String first_parameter = String(parameters.First());
    first_parameter.toUpperCase();
    if ( (suffix >= 0) && (suffix < numOfPins) ) {
        if (first_parameter == "1") {
            SetChannel(suffix, 1);
        }
        else if (first_parameter == "0"){
            SetChannel(suffix, 0);
        }
    }
}


void ListenForRemote() {
    if (myRemote.available()) {
        int received_value = myRemote.getReceivedValue();
        Serial.println(received_value);
        for (int it = 0; it < sizeof(RFCodes); it++) {
            if (received_value == RFCodes[it]){
                ToggleChannel(RFChannels[it]);
            }
        }
        delay(rf_delay);
        myRemote.resetAvailable();
    }
}


int GetChannel(int ch) {
    // Get the status of a channel, return 0 if off, otherwise on
    if (digitalRead(DOut[ch]) == HIGH) {
        return 1;
    }
    else {
        return 0;
    }

}


void SetChannel(int ch, int state) {
    // Set a given channel with the given state
    if ((state == 0) || (state == 1)) {
        digitalWrite(DOut[ch], state);
        digitalWrite(LedPins[ch], state);
    }
}


void ToggleChannel(int ch) {
    // Toggle a channel
    SetChannel(ch, not GetChannel(ch));
}
