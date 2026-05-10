from flask import Flask, abort
import time
import gpiozero
import json

_DEFAULT_GPIO = 17

"""
Init the GPIO pin to be an input with no pull up and active HIGH.
No pull up is very import since we need the GPIO pin to be in a
high impedance (high z) state to emulate a button

NOTE: The active state doesn't really matter as we well never actually sample
        the gpio pin. 

"""
def init_gpio_pin(pin: str = _DEFAULT_GPIO) -> gpiozero.InputDevice:
    print("init")
    return gpiozero.InputDevice(pin, pull_up=None, active_state=True)


"""
Emulate a button press with GPIO
"""
def button_press(gpio: gpiozero.InputDevice, press_time: float) -> gpiozero.InputDevice:
    # grab the pin we are using
    pin = gpio.pin
    print(pin)

    # close our input device
    gpio.close()

    # make an output device
    # We need to active low to close the circuit (i.e. connect the grounds)
    # we also make sure that the pin starts in the active state
    output_dev = gpiozero.OutputDevice(17, active_high=False, initial_value=True)

    # delay
    time.sleep(press_time)

    # swap back to input
    output_dev.off()
    output_dev.close()

    # Return the gpio pin back in input
    return init_gpio_pin(17)


###########
# Web Stuffs
###########
app = Flask(__name__)

_gpio = init_gpio_pin(17)

@app.route("/hit_the_button", methods=['POST'])
def hit_the_button():
    global _gpio
    try:
        _gpio = button_press(_gpio, 0.5)
    except Exception as e:
        import traceback
        traceback.format_exc(e)
        abort(500, json.dumps({"exception":f"{e}"}))

    return "Success"


@app.route("/program_the_button", methods=['POST'])
def program_the_button():
    global _gpio
    try:
        _gpio = button_press(_gpio, 3)
    except Exception as e:
        import traceback
        traceback.format_exc(e)
        abort(500, json.dumps({"exception" : f"{e}"}))

    return "Success"




if __name__ == "__main__":
    pass
