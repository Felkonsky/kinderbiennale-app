#include <Adafruit_NeoPixel.h>
#include <stdio.h>

// Setup digital pins for all buttons
#define BTN_1_PIN 38
#define BTN_2_PIN 40
#define BTN_3_PIN 42
#define BTN_4_PIN 44
#define BTN_5_PIN 46
#define BTN_6_PIN 48
#define BTN_7_PIN 50
#define BTN_8_PIN 52

// Setup digital pins for all LEDs (buttons and strip)
#define LED_1_PIN 39
#define LED_2_PIN 41
#define LED_3_PIN 43
#define LED_4_PIN 45
#define LED_5_PIN 47
#define LED_6_PIN 49
#define LED_7_PIN 51
#define LED_8_PIN 53

#define LED_STRIP_PIN 36
#define LED_STRIP_COUNT 83 // Number of LEDs (current strip length)

struct Button {
  const uint8_t btnPin;
  const uint8_t ledPin;
  bool isPressed;
};

struct Button buttons[] = {
  {BTN_1_PIN, LED_1_PIN, false},
  {BTN_2_PIN, LED_2_PIN, false},
  {BTN_3_PIN, LED_3_PIN, false},
  {BTN_4_PIN, LED_4_PIN, false},
  {BTN_5_PIN, LED_5_PIN, false},
  {BTN_6_PIN, LED_6_PIN, false},
  {BTN_7_PIN, LED_7_PIN, false},
  {BTN_8_PIN, LED_8_PIN, false}
};

// Array for the flash animation
uint8_t ledList[] = {LED_1_PIN, LED_2_PIN, LED_3_PIN, LED_4_PIN, LED_5_PIN, LED_6_PIN, LED_7_PIN, LED_8_PIN};

// strip initialization depends on the type
Adafruit_NeoPixel strip(LED_STRIP_COUNT, LED_STRIP_PIN, NEO_GRB + NEO_KHZ800);

const size_t NUMBTNS = sizeof(buttons) / sizeof(buttons[0]);
const uint8_t BRIGHTNESS = 75;
const uint32_t WHITE = strip.Color(255, 255, 255);

bool flashed = false; // LED flash animation ran on first button pressed?
uint8_t sequenceIndex = 0; // How many buttons were pressed already?

void setup() {
  Serial.begin(115200);
  initStrip();
  for (uint8_t i = 0; i < NUMBTNS; i++) {
    pinMode(buttons[i].btnPin, INPUT_PULLUP);
    pinMode(buttons[i].ledPin, OUTPUT);
  }
}

// check the number of buttons pressed: 1 - flash animation, 2 -> send data
void loop(){
  uint8_t i;
  if (sequenceIndex < 2) {
    for (i = 0; i < NUMBTNS; i++) {
      if (digitalRead(buttons[i].btnPin) == LOW && !buttons[i].isPressed) {
        buttons[i].isPressed = true;
        digitalWrite(buttons[i].ledPin, HIGH);
        Serial.write(i+1); // scenario representative
        delay(100);
        sequenceIndex++;
        break;
      }
    }
    if (sequenceIndex == 1 && !flashed) {
      for (i = 0; i < NUMBTNS; i++) {
        sequentialFlash(i); // flash animation
        flashed = true;
        break;
      }
    }
  }
  else if (sequenceIndex > 1) {
    strip.clear(); // turn off led-strip
    strip.show(); // make changes
    delay(20000); // during this time the AI image is shown
    reset(); // Initial state, i.e. deactivate all LED-buttons, activate LED-strip, ...
  }
  delay(100);
}

void reset() {
  sequenceIndex = 0;
  flashed = false;
  for (uint8_t i = 0; i < NUMBTNS; i++) {
    buttons[i].isPressed = false;
    digitalWrite(buttons[i].ledPin, LOW);
  }
  initStrip();
}

void initStrip() {
  strip.begin();
  strip.setBrightness(BRIGHTNESS);
  strip.fill(WHITE);
  strip.show();
}

void sequentialFlash(uint8_t idx) {
  uint8_t i = idx + 1;
  uint8_t j = idx - 1;
  while (true) {
    if (i < 8) {
      digitalWrite(ledList[i], HIGH);
    }
    if (j >= 0) {
      digitalWrite(ledList[j], HIGH);
    }
    delay(150); // adjust to make changes to the animation speed
    if (i < 8) {
      digitalWrite(ledList[i], LOW);
    }
    if (j >= 0) {
      digitalWrite(ledList[j], LOW);
    }
    if (i >= 7 && j <= 0) {
      break;
    }
    else if (j > 0 || i < 7) {
      i++;
      j--;
    }
  }
}
