/*
* Configuration for DigOutBox.
* This file sets the DigOutBox up for your specific system.
*/

// **************************
// DIGOUTBOX HW CONFIGURATION
// **************************

// In debug mode, additional comments aside from SCPI comms are sent over serial
const bool debug = true;

// Channels and remote control buttons
const int numOfChannels = 16;
const int numOfRemoteButtons = 10;


// **********
// USER SETUP
// **********

// Set delay in ms after valid RF press
const int rf_delay = 500;

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

// What is the off-state of the channels?
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

// Setup of the digital outputs and LED channels (pins)
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
};  // Output pin assignment
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
};  // Where are the LEDs?

// Interrupt the RF Receiver is connected to (NOT pin number!)
const int RFInterrupt = 0;  // Which interrupt does the R receiver sit on? NOT pin!

// Number of remotes
const int numOfRemotes = 2;

// RF codes for Remotes, number must be defined before
const long RFRemoteCodes[numOfRemoteButtons][numOfRemotes]  {
  {4543795, 0},
  {4543804, 0},
  {4543939, 0},
  {4543948, 0},
  {4544259, 0},
  {4544268, 0},
  {4545795, 0},
  {4545804, 0},
  {4551939, 0},
  {4551948, 0}

};

