if [ $# -eq 0 ] ; then
    echo 'Please give port as input.'
		echo 'Example: sh install.sh /dev/ttyUSB0'
    exit 1
fi

echo "========================================"
echo ""
echo "---------------------------"
echo "Building ESP32 firmware ..."
echo "---------------------------"
echo ""

cd /home/code/micropython_firmware_with_ota/micropython_git/ports/esp32 && make

echo ""
echo "------------------"
echo "... done building."
echo "------------------"
echo ""

echo ""
echo "-----------------------"
echo "Erasing ESP32 flash ..."
echo "-----------------------"
echo ""

esptool.py --chip esp32 --port $1 --baud 460800 erase_flash

echo ""
echo "-----------------"
echo "... done erasing."
echo "-----------------"
echo ""

echo ""
echo "----------------------------"
echo "Deploying to ESP32 flash ..."
echo "----------------------------"
echo ""

esptool.py --chip esp32 --port $1 --baud 460800 write_flash -z --flash_mode dio --flash_freq 40m 0x1000 /home/code/micropython_firmware_with_ota/micropython_git/ports/esp32/build-GENERIC/firmware.bin

echo ""
echo "-------------------"
echo "... done deploying."
echo "-------------------"
echo ""
echo "========================================"
