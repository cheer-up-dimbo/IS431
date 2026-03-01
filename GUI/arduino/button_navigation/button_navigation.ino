// BoxBunny GUI navigation buttons
// Pins:
//   BTN1 -> D2  (UP)
//   BTN2 -> D4  (ENTER)
//   BTN3 -> D7  (DOWN)
// Wiring:
//   One leg of each pushbutton to GND, the other leg to the pin.
//   Uses INPUT_PULLUP, so pressed state is LOW.

const uint8_t BTN1_PIN = 2;
const uint8_t BTN2_PIN = 4;
const uint8_t BTN3_PIN = 7;

const unsigned long DEBOUNCE_MS = 40;

struct ButtonState {
  uint8_t pin;
  const char* message;
  bool stableLevel;
  bool lastReading;
  unsigned long lastChangeMs;
};

ButtonState buttons[] = {
  {BTN1_PIN, "BTN1_PRESS", HIGH, HIGH, 0},
  {BTN2_PIN, "BTN2_PRESS", HIGH, HIGH, 0},
  {BTN3_PIN, "BTN3_PRESS", HIGH, HIGH, 0}
};

void setup() {
  Serial.begin(115200);

  for (ButtonState &btn : buttons) {
    pinMode(btn.pin, INPUT_PULLUP);
    bool reading = digitalRead(btn.pin);
    btn.stableLevel = reading;
    btn.lastReading = reading;
    btn.lastChangeMs = millis();
  }
}

void loop() {
  unsigned long now = millis();

  for (ButtonState &btn : buttons) {
    bool reading = digitalRead(btn.pin);

    // Reading changed: reset debounce timer
    if (reading != btn.lastReading) {
      btn.lastReading = reading;
      btn.lastChangeMs = now;
    }

    // If reading is stable long enough, commit state change
    if ((now - btn.lastChangeMs) >= DEBOUNCE_MS && reading != btn.stableLevel) {
      btn.stableLevel = reading;

      // Trigger only on button press edge (HIGH -> LOW)
      if (btn.stableLevel == LOW) {
        Serial.println(btn.message);
      }
    }
  }
}
