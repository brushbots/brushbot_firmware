# Modify, compile and deploy the brushbot firmware

1. connect the brushbot using an FTDI-USB cable
2. `sh run.sh` to run docker container
3. From inside container: `sh /home/code/build_and_deploy_firmware.sh /dev/ttyUSB0` where `/dev/ttyUSB0` is the port corresponding to the brushbot

To modify the firmware before building it, edit the file `inisetup.py` before step 2.
