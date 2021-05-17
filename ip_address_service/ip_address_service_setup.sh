#!/bin/sh

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# echo $PROJECT_ROOT

echo "Create virtual env..."
if [ ! -d "../env" ]
then
    python3 -m venv ../env
fi

echo "Install prereqs..."
$PROJECT_ROOT/../env/bin/pip3 install -r "requirements.txt"

echo "Remove any old installations..."
sudo rm /etc/systemd/system/ip_address_service.service
sudo rm /etc/systemd/system/ip_address_updater_service.service
sudo rm printer_info.py

echo "Create printer_info.py..."
echo ""
echo "Is this device a printer? (True, False)"
read is_printer
echo "What series does it belong to? (HR, MR, Calibration, ...)"
read series
echo "What is its version number? (1.0, 3.3, ...)"
read version

sudo echo "IS_PRINTER = $is_printer"                >> printer_info.py
sudo echo "HARDWARE_SERIES = \"$series\""               >> printer_info.py
sudo echo "HARDWARE_VERSION = \"$version\""             >> printer_info.py

echo "Create service..."
sudo echo "[Unit]"                                              >> /etc/systemd/system/ip_address_service.service
sudo echo "Description=Broadcasts this devices IP address, hostname, and hardware type to static ip server."
                                                                >> /etc/systemd/system/ip_address_service.service
sudo echo "After=network.target"                                >> /etc/systemd/system/ip_address_service.service

sudo echo "[Service]"                                           >> /etc/systemd/system/ip_address_service.service
sudo echo "ExecStart=$PROJECT_ROOT/../env/bin/python -u ip_address_service.py"    >> /etc/systemd/system/ip_address_service.service
sudo echo "ExecStop=/bin/systemctl kill ip_address_service"        >> /etc/systemd/system/ip_address_service.service
sudo echo "WorkingDirectory=$PROJECT_ROOT"                      >> /etc/systemd/system/ip_address_service.service
sudo echo "StandardOutput=inherit"                              >> /etc/systemd/system/ip_address_service.service
sudo echo "StandardError=inherit"                               >> /etc/systemd/system/ip_address_service.service
sudo echo "Restart=always"                                      >> /etc/systemd/system/ip_address_service.service
sudo echo "RestartSec=10"                                     >> /etc/systemd/system/ip_address_service.service
sudo echo "User=root"                                           >> /etc/systemd/system/ip_address_service.service

sudo echo "[Install]"                                           >> /etc/systemd/system/ip_address_service.service
sudo echo "WantedBy=multi-user.target"                          >> /etc/systemd/system/ip_address_service.service

echo "Create updater service..."
sudo echo "[Unit]"                                              >> /etc/systemd/system/ip_address_updater_service.service
sudo echo "Description=Pulls any updates to ip_address_service from github repository."
                                                                >> /etc/systemd/system/ip_address_updater_service.service
sudo echo "After=network.target"                                >> /etc/systemd/system/ip_address_updater_service.service

sudo echo "[Service]"                                           >> /etc/systemd/system/ip_address_updater_service.service
sudo echo "ExecStart=$PROJECT_ROOT/../env/bin/python -u ip_address_updater_service.py"    >> /etc/systemd/system/ip_address_updater_service.service
sudo echo "ExecStop=/bin/systemctl kill ip_address_updater_service"        >> /etc/systemd/system/ip_address_updater_service.service
sudo echo "WorkingDirectory=$PROJECT_ROOT"                      >> /etc/systemd/system/ip_address_updater_service.service
sudo echo "StandardOutput=inherit"                              >> /etc/systemd/system/ip_address_updater_service.service
sudo echo "StandardError=inherit"                               >> /etc/systemd/system/ip_address_updater_service.service
sudo echo "Restart=always"                                      >> /etc/systemd/system/ip_address_updater_service.service
# sudo echo "RestartSec=86400"                                    >> /etc/systemd/system/ip_address_updater_service.service
sudo echo "User=root"                                           >> /etc/systemd/system/ip_address_updater_service.service

sudo echo "[Install]"                                           >> /etc/systemd/system/ip_address_updater_service.service
sudo echo "WantedBy=multi-user.target"                          >> /etc/systemd/system/ip_address_updater_service.service

echo "Launch services..."
sudo systemctl daemon-reload
sudo systemctl start ip_address_updater_service.service
sudo systemctl start ip_address_service.service
sudo systemctl enable ip_address_updater_service.service
sudo systemctl enable ip_address_service.service
