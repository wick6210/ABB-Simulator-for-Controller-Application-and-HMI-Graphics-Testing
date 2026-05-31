# FSM Working in the Project

There are 5 states in total for this project:

1. `FILLING`
2. `DRAINING`
3. `ALARM_HIGH`
4. `ALARM_LOW`
5. `MANUAL`

## `FILLING`

In the `FILLING` state, the water pump is ON and water flows into the tank. This continues to flow until the tank reaches 80% of total capacity, after which, the water pump will get a signal to turn OFF.

Level >= 80 -> `DRAINING`
Level >= 95 -> `ALARM_HIGH`

## `DRAINING`

In the `DRAINING` state, the water pump is OFF, and water flows out of the tank. This continues to flow until the tank reaches 20% of total capacity, after which, the water pump will get a signal to turn ON.

Level <= 20 -> `FILLING`
Level <= 5  -> `ALARM_LOW`

## `ALARM_HIGH`

In the `ALARM_HIGH` state, it sends an alarm to the controller, saying that the tank is about to reach maximum capacity, and that the water flow must halt. This forcefully stops the water pump from flowing water into the tank, and the tank is allowed to drain. The `ALARM_HIGH` state will be enabled so long as the water level in the take is greater than 80% of the tanks total capacity. After the water level has reduced to 80% of the tanks total capacity, the state will change to `DRAINING`.

Level >= 80 -> `ALARM_HIGH`
Level < 80  -> `DRAINING`

## `ALARM_LOW`

In the `ALARM_LOW` state, it sends an alarm to the controller, saying that the tank is about to be completely draining, and that water flow must start. This forcefully starts the water pump and allows for water to flow into the tank, and te tank is allowed to fill. The `ALARM_LOW` state is enabled so long as the water level is less than 20% of the tanks total capacity. After the water level has increased to 20% of the tanks total capacity, the state will change to `FILLING`.

Level <= 20 -> `ALARM_LOW`
Level > 20  -> `FILLING`

## `MANUAL`

In the `MANUAL` state, the controller abandons automatic level monitoring of the water tank, and the water pump is manually turned ON and OFF. The water pump is not forcefully turned ON or OFF based on the water level in the tank. Until and unless the operator changes the water pump state, or the operator switches to automotic level monitoring, the tank will continue to fill/drain regardless of threshold limits.