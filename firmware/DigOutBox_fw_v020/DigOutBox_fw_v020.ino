/*
 * Firmware v010 for DigIOBox
 */
#include <Arduino.h>
#include <RCSwitch.h>
#include <Vrekrer_scpi_parser.h>
#include "config.h"

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
void AllOff();

// Interlock variable: True if currently triggered
bool IsInterlocked = true;

// Software lockout active?
bool SoftwareLockoutToggle = false;
int SoftwareLockoutCounter = 0;
unsigned long SoftwareLockoutClock = 0;


void setup() {

  // SCPI Setup
  DigIOBox.RegisterCommand(F("*IDN?"), &Identify);
  DigIOBox.RegisterCommand(F("DOut#?"), &GetDigIO);
  DigIOBox.RegisterCommand(F("DOut#"), &SetDigIO);
  DigIOBox.RegisterCommand(F("ALLDOut?"), &GetAllDigIO);
  DigIOBox.RegisterCommand(F("ALLOFF"), &AllOff);
  DigIOBox.RegisterCommand(F("INTERLOCKState?"), &GetInterlockState);  // returns 1 if interlocked
  DigIOBox.RegisterCommand(F("SWLockout?"), &GetSoftwareLockoutState);  // returns 1 if software is locked

  // Output and LED setups
  for (int it = 0; it < numOfChannels; it++) {
    pinMode(DOut[it], OUTPUT);
    pinMode(LedPins[it], OUTPUT);
  }

  // RF Remote setup
  myRemote.setPulseLength(185);
  myRemote.setRepeatTransmit(5);

  // Start serial console
  Serial.begin(9600);

  // Put the switches into the off position
  AllOff();

  // Interlock setup
  if (EnableInterlock == true) {
    pinMode(InterlockPin, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(InterlockPin), interlock, CHANGE);
    // check interlock status and activate / deactivate remote
    interlock();
  }
  else {
    myRemote.enableReceive(RFInterrupt);
    IsInterlocked = false;
  }
}


void loop() {
  // only work when interlocked is pulled down
  DigIOBox.ProcessInput(Serial, "\n");
  ListenForRemote();
}


void interlock() {
  // Turn all channels off and disable remote
  if (digitalRead(InterlockPin) == HIGH) {
    if (debug == true) {
      Serial.println("Interlock triggered.");
    }

    AllOff();
    myRemote.disableReceive();
    IsInterlocked = true;

  }
  // Turn remote back on.
  else {
    if (debug == true) {
      Serial.println("Interlock not triggered.");
    }

    myRemote.enableReceive(RFInterrupt);
    IsInterlocked = false;
  }
}

void software_lockout() {
  // Lock the software out with the remote
  if (not SoftwareLockoutToggle) {
    SoftwareLockoutToggle = true;
    if (debug == true) {
      Serial.println("Software lockout activated.");
    }
  }
  else {
    if (debug == true) {
      Serial.print("Software lockout counter: ");
      Serial.println(SoftwareLockoutCounter);
    }
    // this is the first click
    if (SoftwareLockoutCounter == 0) {
      SoftwareLockoutCounter++;
      SoftwareLockoutClock = millis();
    }
    // this is the second click
    else {
      // click was not in time
      if (millis() - SoftwareLockoutClock > SoftwareLockoutDoubleClickTime) {
        if (debug == true) {
          Serial.println("Assuming this is the first click.");
        }
        SoftwareLockoutCounter = 1;
        SoftwareLockoutClock = millis();
      }
      // second click -> deactivate SoftwareLockout
      else {
        if (debug == true) {
          Serial.println("Deactivating software lockout.");
        }
        SoftwareLockoutCounter = 0;
        SoftwareLockoutToggle = false;
        SoftwareLockoutClock = 0;
      }
    }
  }
}


void Identify(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  interface.print(F("DigIOBox, Hardware "));
  interface.print(hw_version);
  interface.print(", Firmware ");
  interface.println(fw_version);
}


void GetAllDigIO(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  // ALLDOut?
  // Query all logic states of the available DOut pins
  // Return values are "1" or "0", aranged in a comma separated values list
  for (int it = 0; it < numOfChannels - 1; it++) {  // all but the last
    interface.print(GetChannel(it));
    interface.print(",");
  }
  // print the last
  interface.println(GetChannel(numOfChannels - 1));
}


void GetDigIO(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  // DOut<index>?
  // Queries the logic state of DOut[index] pin
  // Return values are "1" or "0"
  // Examples:
  //  DO4?    (Queries the state of DOut[4] pin)
  //  DOut1000?  (This does nothing as DOut[1000] does not exists)

  //Get the numeric suffix/index (if any) from the commands
  String header = String(commands.Last());

  header.toUpperCase();

  int suffix = -1;

  sscanf(header.c_str(),"%*[DO]%u", &suffix);

  //If the suffix is valid, print the pin's logic value to the interface
  if ( (suffix >= 0) && (suffix < numOfChannels) ) {
    interface.println(GetChannel(suffix));
  }
}


void SetDigIO(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  // DOut<index> state
  // Sets the logic state of DOut[index] pin
  // Valid states are : "HIGH", "LOW", "ON", "OFF", "1" and "0"
  // and any lowercase/uppercase combinations
  // Examples:
  //  DOut4 1  (Sets DOut[4] to HIGH)
  //  DO0 1  (Sets DOut[0] to HIGH)

  // do nothing if software is locked out
  if (not SoftwareLockoutToggle) {
    //Get the numeric suffix/index (if any) from the commands
    String header = String(commands.Last());
    header.toUpperCase();
    int suffix = -1;

    sscanf(header.c_str(),"%*[DO]%u", &suffix);

    //If the suffix is valid,
    //use the first parameter (if valid) to set the digital Output
    String first_parameter = String(parameters.First());
    first_parameter.toUpperCase();
    if ( (suffix >= 0) && (suffix < numOfChannels) ) {
      if (first_parameter == "1") {
        SetChannel(suffix, 1);
      }
      else if (first_parameter == "0"){
        SetChannel(suffix, 0);
      }
    }
  }
}


void ListenForRemote() {
  if (myRemote.available()) {
    // read remote value
    long received_value = myRemote.getReceivedValue();
    int channel = -3;  // no channel
    // Read channel to be triggered
    for (int it = 0; it < numOfRemoteButtons; it++) {
      for (int rt = 0; rt < numOfRemotes; rt++) {
        if (received_value == RFRemoteCodes[it][rt]){
          channel = RFChannels[it];
         break;
        }
      }
     if (channel != -3) {
       break;
     }
    }

    if (debug == true) {
      Serial.print("Valid RF Remote code received: ");
      Serial.print(received_value);
      Serial.print(" / Channel associated: ");
      Serial.println(channel);
    }

    // Now toggle if required
    if (channel == -1) {
      AllOff();
    }
    else if (channel == -2) {
      software_lockout();
      delay(rf_delay);
    }
    else if ((channel > -1) && (channel < numOfChannels)) {
      ToggleRFChannel(channel);
      delay(rf_delay);
    }

    // Reset remote connection
    myRemote.resetAvailable();
  }
}


int GetChannel(int ch) {
  // Get the status of a channel, return 0 if off, otherwise on
  // In order to invert actual channels, we read the LED state here!
  if (digitalRead(LedPins[ch]) == HIGH) {
    return 1;
  }
  else {
    return 0;
  }

}

void GetSoftwareLockoutState(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  // Get the state of the SoftwareLockoutToggle. return 0 if off, 1 if on.
  if (SoftwareLockoutToggle) {
    interface.println(1);
  }
  else {
    interface.println(0);
  }

}

void GetInterlockState(SCPI_C commands, SCPI_P parameters, Stream& interface) {
  // Get the state of the SoftwareLockoutToggle. return 0 if off, 1 if on.
  if (IsInterlocked) {
    interface.println(1);
  }
  else {
    interface.println(0);
  }

}

void SetChannel(int ch, int state) {
  // only set a channel if not interlocked
  if (IsInterlocked == false) {
    // Set a given channel with the given state
    if ((state == 0) || (state == 1)) {
      // states to set
      int out_state = state;
      // check if inverted
      if (DOutInvert[ch] == 1) {
        out_state = not out_state;
      }

      // write the states out
      digitalWrite(DOut[ch], out_state);
      digitalWrite(LedPins[ch], state);  // LED is always the actual state
    }
  }
}


// Turn all channels off
void AllOff() {
  for (int it = 0; it < numOfChannels; it++) {
    SetChannel(it, 0);
  }
}


// Function to toggle via the RF remote. Triggers Channel and LED
void ToggleRFChannel(int ch) {
  // Toggle a channel
  SetChannel(ch, not GetChannel(ch));
}
