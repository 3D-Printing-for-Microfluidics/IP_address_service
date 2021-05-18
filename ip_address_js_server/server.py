# multithreading
import threading

# server
import flask
from flask import request, jsonify
from flask_socketio import SocketIO
from device_tables import DeviceTables
import json

# from time import sleep

# sleep(10)

# create flask server
app = flask.Flask(__name__, static_url_path="", static_folder="")
app.config["DEBUG"] = True
app.config[
    "SEND_FILE_MAX_AGE_DEFAULT"
] = 0  # IMPORTANT disables cacheing of our javascript on requesting computer so printer list will update every time it is requested

socketio = SocketIO()
# socketio = SocketIO(app)
socketio.init_app(app)

# creates ip_discovery object
tables = DeviceTables()

# A route used for trusting the database
@app.route("/", methods=["GET"])
def home():
    print("Route - home")
    return (
        """<p>Printer server now trusted. Return to wiki for printer information.</p>"""
    )


# A route that returns json list of printers. (Does not work on wiki)
@app.route("/api", methods=["GET"])
def api_json():
    print("Route - api")
    tables.check_all_printer_status()
    return jsonify(tables.printers)


# A route that returns json list of printers. (Does not work on wiki)
@app.route("/api/flush", methods=["GET"])
def api_flush():
    print("Route - api/flush")
    tables.clear_all_ip_addresses()
    return "Printers flushed"


# A route that returns javascript table of printers. (for wiki)
@app.route("/api/data.js")
def api_js():
    print("Route - api/data.js")
    tables.check_all_printer_status()
    tables.check_all_device_status()
    # create new js file with current data
    with open("data.js", "w") as outfile:
        # write header
        outfile.write("printers = ")
        # write json data
        outfile.write(json.dumps(tables.printers))
        outfile.write("\r\n")
        # write header
        outfile.write("devices = ")
        # write json data
        outfile.write(json.dumps(tables.devices))
        outfile.write("\r\n")
        # write the rest of the functions
        with open("data_functions.js") as infile:
            outfile.write(infile.read())
    return app.send_static_file("data.js")


@socketio.on("register_ip", namespace="/")
def register_ip(message):
    print("Socket - register_ip")
    tables.register_ip(message)


# start printer discovery
service_thread = threading.Thread(target=tables.loop)
service_thread.daemon = True
service_thread.start()

# app.run(host="0.0.0.0", port=5000)  # http server

# app.run(host="0.0.0.0", port=5001, ssl_context="adhoc")  # https with blank certificate

# app.run(
#     "0.0.0.0",
#     port=5000,
#     ssl_context=(
#         "/home/pi/Bonjour_3D_printer_discovery/bonjour_js_server/cert.crt",
#         "/home/pi/Bonjour_3D_printer_discovery/bonjour_js_server/key.key",
#     ),
# )  # https with full certificate (requires password on startup)

app.run(
    "0.0.0.0",
    port=443,
    ssl_context=(
        "cert/BundledCert.crt",
        "cert/nordinip.key",
    ),
)  # https with full certificate (requires password on startup)
