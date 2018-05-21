try:
    import RPi.GPIO as GPIO
except:
    print("ops, someone have tried to run a pi program on the pc... (<cuffing> 'defiantly nir karl')")

UNSLEEP = {"U": 26, "R": 6, "F": 13, "D": 5, "L": 19, "B": 11}

def pi_init():
    GPIO.setmode(GPIO.BCM)
    for u in UNSLEEP:
        GPIO.setup(UNSLEEP[u], GPIO.OUT)
        GPIO.output(UNSLEEP[u], 1)

try:
    pi_init()
    input("press a key st clean up GPIOs")
    GPIO.cleanup()
    print("GPIOs have been cleaned up.")
except:
    print("no pi i guess...")