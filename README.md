# HomeAssistant component for pi-distance sensor

This is the HomeAssistant part for pi-distance to
read data from the Pi Pico and the attached HC-SR04
ultrasonic sensor

See https://github.com/ochorocho/pico-distance for the pi pico sensor instructions

## Example configuration 

```yaml
sensor:
  - platform: pi_distance
    name: "Distance Pi"
    url: http://192.168.178.1/
```