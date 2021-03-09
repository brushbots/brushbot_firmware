FROM ubuntu:18.04

# general purpose software
RUN apt-get update && apt-get install -y git wget vim tar netbase net-tools arp-scan iputils-ping
# micropython
RUN apt-get install -y python-pip python3 python3-pip
RUN apt-get install -y gcc make libncurses-dev flex bison gperf python python-setuptools python-serial python-cryptography python-future python-pyparsing libffi-dev libssl-dev
# arduino
RUN apt-get install -y libxrender-dev libxtst-dev

# micropython interface tools
RUN pip install esptool
RUN pip install adafruit-ampy
RUN pip3 install pyparsing

# download necessary code
# arduino IDE
RUN mkdir -p /home/code && cd /home/code && wget https://downloads.arduino.cc/arduino-1.8.13-linux64.tar.xz && tar -xvf arduino-1.8.13-linux64.tar.xz && rm arduino-1.8.13-linux64.tar.xz
# micropython firmware github repository
RUN mkdir -p /home/code/micropython_firmware_with_ota && cd /home/code/micropython_firmware_with_ota && git clone https://github.com/micropython/micropython.git micropython_git && mv micropython_git/ports/esp32/modules/inisetup.py micropython_git/ports/esp32/modules/inisetup.py.ori
# Espressif IDF
ENV ESPIDF_HASH="9e70825d1e1cbf7988cf36981774300066580ea7"
ENV ESPIDF="/home/code/micropython_firmware_with_ota/esp-idf"
RUN mkdir -p $ESPIDF && cd $ESPIDF && git clone https://github.com/espressif/esp-idf.git $ESPIDF && cd $ESPIDF && git checkout $ESPIDF_HASH && git submodule update --init --recursive
RUN cd /home/code/micropython_firmware_with_ota/micropython_git/ports/esp32 && pip install --upgrade pip && pip install -r $ESPIDF/requirements.txt
# Xtensa cross-compiler
RUN cd /home/code/micropython_firmware_with_ota && wget https://dl.espressif.com/dl/xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz && tar -xvzf xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz && rm xtensa-esp32-elf-linux64-1.22.0-80-g6c4433a-5.2.0.tar.gz
ENV PATH="/home/code/micropython_firmware_with_ota/xtensa-esp32-elf/bin:${PATH}"

# build firmware submodules
RUN cd /home/code/micropython_firmware_with_ota/micropython_git/mpy-cross && make mpy-cross
RUN cd /home/code/micropython_firmware_with_ota/micropython_git/ports/esp32 && make submodules

ENTRYPOINT ["/bin/bash"]
