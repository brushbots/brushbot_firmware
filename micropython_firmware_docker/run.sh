xhost +

sudo docker run \
    --rm \
    -it \
    --net=host \
    --env="DISPLAY" \
    --volume "$HOME/.Xauthority:/root/.Xauthority:rw" \
    --volume "$(pwd)/inisetup.py:/home/code/micropython_firmware_with_ota/micropython_git/ports/esp32/modules/inisetup.py" \
    --volume "$(pwd)/build_and_deploy_firmware.sh:/home/code/build_and_deploy_firmware.sh" \
    --privileged \
    brushbot:firmware_setup
