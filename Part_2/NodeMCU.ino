const int MODE_BTN = D5;
const int PUMP_BTN = D6;

bool manualMode = false;
bool pumpCmd = false;

bool prevModeBtn = HIGH;
bool prevPumpBtn = HIGH;

unsigned long lastModePress = 0;
unsigned long lastPumpPress = 0;

const unsigned long debounceMs = 200;

void setup()
{
    pinMode(MODE_BTN, INPUT_PULLUP);
    pinMode(PUMP_BTN, INPUT_PULLUP);

    Serial.begin(115200);

    Serial.println("ESP8266 Controller Ready");
}

void loop()
{
    bool modeBtn = digitalRead(MODE_BTN);
    bool pumpBtn = digitalRead(PUMP_BTN);

    if (prevModeBtn == HIGH &&
        modeBtn == LOW &&
        millis() - lastModePress > debounceMs)
    {
        manualMode = !manualMode;

        Serial.print("MODE:");
        Serial.println(manualMode ? 1 : 0);

        lastModePress = millis();
    }

    if (manualMode)
    {
        if (prevPumpBtn == HIGH &&
            pumpBtn == LOW &&
            millis() - lastPumpPress > debounceMs)
        {
            pumpCmd = !pumpCmd;

            Serial.print("PUMP:");
            Serial.println(pumpCmd ? 1 : 0);

            lastPumpPress = millis();
        }
    }

    prevModeBtn = modeBtn;
    prevPumpBtn = pumpBtn;
}
