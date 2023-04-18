# PumpControl
This python program is wrote to communicate with the pump control station (DK-SPC) in iharbor-lab.

Using MODBUS-RTU as communication protocol.

Environment with python3.8, PyQt5, modbus_tk and serial module is required.

## **Functions**
>1. Connect & Disconnect;
>2. Set diameter for syringe;
>3. Set flow rate (default time is 1 hour) for pumps;
>4. Run & Stop;
>5. Refresh.

## **Instruction:**
Step 1. Set correct port and baudrate, click "*Connect*" to build connection between program and control station;

Step 2. Check rows according to the number of the pumps need to be used;

Step 3. Tap the diameters or flow rate then click "*Set Select*" to send the change to the control station;

Step 4. Using "*Run Select*" or "*Stop Select*" to control the status of the pumps.

