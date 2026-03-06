# Air Handler Simulator

![Dashboard - Air Handler Simulator](/screenshots/dashboard.png)

My father worked in commercial and residential HVAC, and I previously worked as a controls programmer. I started this project a couple years ago as a learning tool for controls. I decided to pick it back up recently to rebuild the frontend and fix some annoying bugs. Eventually that turned into a new version with a new sim loop and Vite frontend.

Project is an air handler serving three VAV zones with a lite thermodynamics engine to calculate changes in temperature and airflow. Temperature change is calculated by BTU transfer. Dampers and fans dynamically adjust airflow based on position. The air handler will start and calculate temperatures automatically. The frontend displays air handler simulated sensor data such as temperature and airflow. Static values, such as humidity and setpoint, are also present and may be calculated in future versions. VAV and zone sensor data is also displayed with a slider to adjust VAV damper position. AHU values such as fan speeds, coil temperatures and damper positions can be changed.

Project contains Docker Compose files with an image for the frontend and an image for the backend. Backend is Django, frontend is Vite.

## Temperature Change

### Coils
The entering air calculates its BTU per sim time step based on the difference between its air temperature and the coil's temperature. BTU per sim time step is calculated using the sensible heat equation, where the change in temperature is the time-adjusted change in temperature. This change in temperature is also limited to a maximum of 5°F per minute. This limit was decided based on realistic numbers I was seeing in the field vs. logs from the simulator. The BTU per sim time step is then used in the sensible heat equation, rearranged to calculate the updated leaving air temperature.

### Air Mixing and Meeting
When air streams mix, the receiver's air temperature is calculated as a mass-weighted average by CFM.

## Event Bus

`hvac.engine.events` — This was new to the recent version. I was focused on decoupling systems and pulling logic out of the simulation loop. This also made trend logs easier to implement and enabled a coordinated air handler runtime.

## HVAC

`hvac.engine.core` is responsible for all HVAC objects and calculations.

`Air` currently calculates BTU transfer and temperature change based on BTU per sim time step.

All HVAC air handler objects have an air component. This is how air is simulated moving through the air handler. `Air`, `Fan`, `Coil`, and `Damper` all make up an air handler serving VAVs. `Fan` can calculate its own CFM based on speed when set. `Damper` can calculate airflow based on size and actuator position.

`AirUnit` is the air handler object. Based on a multi-zone AHU with hydronic heating/cooling coils, a mixed air damper, and a supply/return fan serving 3 equally sized 10x10x10 zones.

## Trends

Trends were designed for the frontend graphs and as a logging resource. Time and buffer size are configurable to allow for logging. They just need to be added to the event bus and are then saved with the object back into the database.

## Sim Loop

Manages two versions of the object: a database version and a class instance. This was the easiest way I found to keep an up-to-date database while utilizing the object's class methods.

# Future Versions
I may expand this to include latent cooling effects.