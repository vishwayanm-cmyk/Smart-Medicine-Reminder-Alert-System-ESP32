/*
 * ─────────────────────────────────────────────────────────────
 *  Face Tracking Camera — Arduino Uno
 *  Servo X (pan / horizontal) → Pin 9
 *  Servo Y (tilt / vertical)  → Pin 10
 *
 *  Protocol: receives "angleX,angleY\n" over Serial (9600 baud)
 *  Both servos initialise to 90° on startup
 * ─────────────────────────────────────────────────────────────
 */

#include <Servo.h>

// ── Pin definitions ──────────────────────────────────────────
#define PIN_SERVO_X   9
#define PIN_SERVO_Y  10

// ── Servo limits & initial position ─────────────────────────
#define SERVO_MIN    0
#define SERVO_MAX  180
#define SERVO_INIT  90

// ── Serial baud rate (must match Python side) ────────────────
#define BAUD_RATE 9600

// ── Smoothing: lerp factor 0.0–1.0
//    Lower = smoother but slower response
//    Higher = faster but may jitter
//    Set to 1.0 to disable smoothing entirely
#define LERP_FACTOR 0.2f

// ── Objects ──────────────────────────────────────────────────
Servo servoX;   // horizontal / pan
Servo servoY;   // vertical   / tilt

// Current (smoothed) angles stored as floats for lerp precision
float currentX = SERVO_INIT;
float currentY = SERVO_INIT;

// Target angles received from Python
int targetX = SERVO_INIT;
int targetY = SERVO_INIT;

// Serial input buffer
String inputBuffer = "";


// ═════════════════════════════════════════════════════════════
//  SETUP
// ═════════════════════════════════════════════════════════════
void setup() {
  Serial.begin(BAUD_RATE);
  inputBuffer.reserve(32);    // pre-allocate to avoid heap fragmentation

  // Attach servos
  servoX.attach(PIN_SERVO_X);
  servoY.attach(PIN_SERVO_Y);

  // Move both servos to the initial 90° position
  servoX.write(SERVO_INIT);
  servoY.write(SERVO_INIT);

  Serial.println("READY");    // optional handshake message to Python
}


// ═════════════════════════════════════════════════════════════
//  LOOP
// ═════════════════════════════════════════════════════════════
void loop() {

  // ── 1. Read incoming serial data ─────────────────────────
  while (Serial.available() > 0) {
    char c = (char)Serial.read();

    if (c == '\n') {
      // Full message received — parse it
      parseCommand(inputBuffer);
      inputBuffer = "";           // clear buffer for next message
    } else {
      inputBuffer += c;
    }
  }

  // ── 2. Smooth lerp toward target angles ──────────────────
  currentX = lerp(currentX, (float)targetX, LERP_FACTOR);
  currentY = lerp(currentY, (float)targetY, LERP_FACTOR);

  // ── 3. Write to servos ───────────────────────────────────
  servoX.write((int)currentX);
  servoY.write((int)currentY);

  delay(15);   // ~66 Hz update rate; keeps servo PWM stable
}


// ═════════════════════════════════════════════════════════════
//  PARSE "angleX,angleY" STRING
// ═════════════════════════════════════════════════════════════
void parseCommand(String msg) {
  msg.trim();                     // remove any stray whitespace / CR

  int commaIdx = msg.indexOf(',');
  if (commaIdx == -1) return;     // malformed packet → ignore

  String sX = msg.substring(0, commaIdx);
  String sY = msg.substring(commaIdx + 1);

  int newX = sX.toInt();
  int newY = sY.toInt();

  // Safety clamp — never command a servo out of safe range
  targetX = constrain(newX, SERVO_MIN, SERVO_MAX);
  targetY = constrain(newY, SERVO_MIN, SERVO_MAX);
}


// ═════════════════════════════════════════════════════════════
//  LINEAR INTERPOLATION HELPER
// ═════════════════════════════════════════════════════════════
float lerp(float a, float b, float t) {
  return a + t * (b - a);
}