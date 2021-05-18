
ip_address_server opens a socket on the default https port. Other devices can then send information regarding their status to this port.
A web page is made available showing all printer and device ip addressses. 
The server also exposes a web api that can be used to display or utilize that information.
To install:

1) Open terminal in this directory.
2) Run "sudo -s source ip_address_server_setup.sh"
3) Use this device's IP address or domain name to access the web api.