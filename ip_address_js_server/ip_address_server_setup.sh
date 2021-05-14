#!/bin/sh

PROJECT_ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo $PROJECT_ROOT

#install prereqs
pip3 install flask
pip3 install python-socketio
pip3 install Flask-SoketIO
pip3 install pyopenssl

sudo rm /etc/systemd/system/ip_address_server.service

#add create script service
sudo echo "[Unit]"                                      >> /etc/systemd/system/ip_address_server.service
sudo echo "Description=API Server exposing javascript and json with printer IP addresses"
                                                        >> /etc/systemd/system/ip_address_server.service
sudo echo "After=syslog.target network.target electrum.service"                        >> /etc/systemd/system/ip_address_server.service

sudo echo "[Service]"                                   >> /etc/systemd/system/ip_address_server.service
sudo echo "ExecStart=/usr/bin/python3 -u server.py"     >> /etc/systemd/system/ip_address_server.service
sudo echo "ExecStop=/bin/systemctl kill ip_address_server" >> /etc/systemd/system/ip_address_server.service
sudo echo "WorkingDirectory=$PROJECT_ROOT"              >> /etc/systemd/system/ip_address_server.service
sudo echo "StandardOutput=inherit"                      >> /etc/systemd/system/ip_address_server.service
sudo echo "StandardError=inherit"                       >> /etc/systemd/system/ip_address_server.service
sudo echo "Restart=always"                              >> /etc/systemd/system/ip_address_server.service
sudo echo "User=root"                                   >> /etc/systemd/system/ip_address_server.service

sudo echo "[Install]"                                   >> /etc/systemd/system/ip_address_server.service
sudo echo "WantedBy=multi-user.target"                  >> /etc/systemd/system/ip_address_server.service

sudo systemctl daemon-reload
sudo systemctl start ip_address_server.service
sudo systemctl enable ip_address_server.service

#print instruction messages
echo ""
echo "To use server update the ip address on the project wiki page to this machine's static ip"
echo "Plese reboot for changes to take effect."
