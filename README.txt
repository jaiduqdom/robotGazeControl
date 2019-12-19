Run gaze control system: catkin_ws/lanzar_seguimiento.sh

Important: It requires ROS Kinetic and Linux Ubuntu.

There are some components that should be installed (spanish):

Ejecutar desde la ruta donde se descomprime DLIB (versión 19.18 para tener soporte CUDA/GPU):
	 python setup.py install.

Instalar pyaudio:

sudo apt-get install libasound-dev portaudio19-dev libportaudio2 libportaudiocpp0
sudo apt-get install ffmpeg libav-tools
sudo pip install pyaudio


Uso de auditok
https://github.com/amsehili/auditok


git clone https://github.com/amsehili/auditok.git
cd auditok
python setup.py install


Programa de pose estimation
https://github.com/yinguobing/head-pose-estimation

Instalar OpenFace
git clone https://github.com/cmusatyalab/openface
cd openface
python setup.py install

Instalar Face Recognition
pip install face_recognition


Controladores NVidia
Install via PPA

    $ sudo add-apt-repository ppa:graphics-drivers/ppa
    $ sudo apt update

https://medium.com/@kapilvarshney/how-to-setup-ubuntu-16-04-with-cuda-gpu-and-other-requirements-for-deep-learning-f547db75f227

############################################################################################
INSTALAR DLIB CON SOPORTE GPU: CUDA
############################################################################################
# Instalar CUDA
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/cuda-ubuntu1604.pin
sudo mv cuda-ubuntu1604.pin /etc/apt/preferences.d/cuda-repository-pin-600
wget http://developer.download.nvidia.com/compute/cuda/10.1/Prod/local_installers/cuda-repo-ubuntu1604-10-1-local-10.1.243-418.87.00_1.0-1_amd64.deb
sudo dpkg -i cuda-repo-ubuntu1604-10-1-local-10.1.243-418.87.00_1.0-1_amd64.deb
sudo apt-key add /var/cuda-repo-10-1-local-10.1.243-418.87.00/7fa2af80.pub
sudo apt-get update
sudo apt-get -y install cuda

# Variables entorno CUDA
export PATH=/usr/local/cuda-10.1/bin${PATH:+:${PATH}}
export LD_LIBRARY_PATH=/usr/local/cuda-10.1/lib64\${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}

# Instalar ejemplos CUDA
cuda-install-samples-10.1.sh ~
cd ~/NVIDIA_CUDA-10.1_Samples/5_Simulations/nbody
make
./nbody

# Solución a "Se ha detectado un problema en un programa de sistema"
sudo rm /var/crash/*

# Descargar CUDNN de NVIDIA y ejecutar
# Runtime
sudo dpkg -i libcudnn7_7.6.4.38-1+cuda10.1_amd64.deb
# Developer library
sudo dpkg -i libcudnn7-dev_7.6.4.38-1+cuda10.1_amd64.deb
# Documentación y ejemplos
sudo dpkg -i libcudnn7-doc_7.6.4.38-1+cuda10.1_amd64.deb
# Verificar instalación
cp -r /usr/src/cudnn_samples_v7/ $HOME
cd  $HOME/cudnn_samples_v7/mnistCUDNN
make clean && make
./mnistCUDNN

# Compilar DLIB versión (19.18)
python setup.py install

# Verificar instalación (Debe ser true)
python
import dlib
dlib.DLIB_USE_CUDA

# Instalar arduino IDE:
sudo apt install arduino

# Instalar python-pandas (para representaciones gráficas)
sudo apt-get install python-pandas

# Instalación micrófono Respeaker
# Ver en web: http://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/#update-firmware
sudo apt-get update
sudo pip install pyusb click
git clone https://github.com/respeaker/usb_4_mic_array.git
cd usb_4_mic_array
sudo python dfu.py --download 6_channels_firmware.bin  # The 6 channels version 

# if you want to use 1 channel,then the command should be like:

sudo python dfu.py --download 1_channel_firmware.bin


# Para incluir el USB en el usuario. De lo contrario la librería dará error
#If you don't want to access USB device with sudo, add a udev .rules file to /etc/udev/rules.d:

echo 'SUBSYSTEM=="usb", MODE="0666"' | sudo tee -a /etc/udev/rules.d/60-usb.rules
sudo udevadm control -R  # then re-plug the usb device



