# Multithreading
import threading

# Server
import flask
from flask import request, jsonify, render_template
from flask_socketio import SocketIO
from device_tables import DeviceTables
import json

# Create flask server
app = flask.Flask(__name__, static_url_path="", static_folder="")
app.config["DEBUG"] = True
app.config[
    "SEND_FILE_MAX_AGE_DEFAULT"
] = 0  # IMPORTANT disables cacheing of our javascript on requesting computer so printer list will update every time it is requested

socketio = SocketIO()
socketio.init_app(app)

# Create data table handler
tables = DeviceTables()

# Returns a html version of the ip addresses tables
@app.route("/")
def home():
    print("Route - home")
    return render_template("main.html")


# Returns json list of printers. (Does not work on wiki)
@app.route("/api", methods=["GET"])
def api_json():
    print("Route - api")
    tables.check_all_printer_status()
    return jsonify(tables.printers)


# Flushes all entires in printer and device tables.
@app.route("/api/flush", methods=["GET"])
def api_flush():
    print("Route - api/flush")
    tables.clear_all_ip_addresses()
    socketio.emit("flush", namespace="/")
    return render_template("flush.html")


# Returns javascript table of printers. (for wiki)
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


@app.route("/api/updater_git", methods=["GET"])
def api_updater_git():
    print("Route - api/updater_git")
    with open("updater_git.txt") as infile:
        return infile.read()

@app.route("/api/slicer_settings.json", methods=["GET"])
def api_get_slicer_settings():
    print("Route GET - api/slicer_settings.json")
    return app.send_static_file("slicer_settings.json")

@app.route("/api/slicer_settings.json", methods=["POST"])
def api_set_slicer_settings():
    print("Route POST - api/slicer_settings.json")

    with open("slicer_settings.json", "w") as outfile:
        outfile.write(request.form['json'])


# Called by devices for register
@socketio.on("register_ip", namespace="/")
def register_ip(message):
    print("Socket - register_ip")
    tables.register_ip(message)


# Start printer discovery
service_thread = threading.Thread(target=tables.loop)
service_thread.daemon = True
service_thread.start()

# Run the flask server
app.run(
    "0.0.0.0",
    port=443,
    ssl_context=(
        "cert/BundledCert.crt",
        "cert/nordinip.key",
    ),
)  # https with full certificate (requires password on startup)
