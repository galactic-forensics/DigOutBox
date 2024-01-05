/*
* Configuration for DigOutBox.
* This file sets the DigOutBox up for your specific system.
*/

// **************************
// DIGOUTBOX HW CONFIGURATION
// **************************

// Initial output for the following serial numbers:
// - llnl001, gfl002

// Channels and remote control buttons
const int numOfChannels = 16;
const int numOfRemoteButtons = 10;

// hard- and firmware versions
const char fw_version[7] = "v0.1.0";
const char hw_version[7] = "v0.1.0";


// **********
// USER SETUP
// **********

// Debug mode, additional comments aside from SCPI commands are sent over serial
const bool debug = false;

// Set delay in ms after valid RF press
const int rf_delay = 500;

// Interlock pin
const int InterlockIn = 3;

// Associate remote buttons with channels, -1 for ALL OFF, -2 for None
const int RFChannels[numOfRemoteButtons] = {
  0,
  1,
  2,
  3,
  4,
  5,
  8,
  9,
  10,
  -1
};

// Define the "off-state" of all channels?
// 0: LOW / 1: HIGH
const int DOutInvert[numOfChannels] = {
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1,
  1
};

// *****************************
// BOARD & REMOTE SPECIFIC SETUP
// *****************************

// Channels: A, B, C, D, E, F, G, H, 1, 2, 3, 4, 5, 6, 7, 8

// Setup of pins for the digital outputs
const int DOut[numOfChannels] = {
  36,
  34,
  32,
  30,
  28,
  26,
  24,
  22,
  52,
  50,
  48,
  46,
  44,
  42,
  40,
  38
};

// Setup of pins for LEDs
const int LedPins[numOfChannels] = {
  37,
  35,
  33,
  31,
  29,
  27,
  25,
  23,
  53,
  51,
  49,
  47,
  45,
  43,
  41,
  39
};

// Interrupt the RF Receiver is connected to (NOT pin number!)
const int RFInterrupt = 0;  // Which interrupt does the R receiver sit on? NOT pin!

// Number of remotes
const int numOfRemotes = 2;

// RF codes for Remotes, number must be defined before
const long RFRemoteCodes[numOfRemoteButtons][numOfRemotes]  {
  {4543795, 349491},
  {4543804, 349500},
  {4543939, 349635},
  {4543948, 349644},
  {4544259, 349955},
  {4544268, 349964},
  {4545795, 351491},
  {4545804, 351500},
  {4551939, 357635},
  {4551948, 357644}

};
