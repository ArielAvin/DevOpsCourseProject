from os import environ
from flask import Flask
from redis import StrictRedis, exceptions
from logging import basicConfig, info, error, INFO

LOG_FILE= "/app/logs/app.log"

basicConfig(filename = LOG_FILE, filemode = "a", level = INFO)

info("App started.")

app = Flask(__name__)

info("Flask initiated")

def print_and_log(message, level = info, function = "pl"):
    function = str(function)
    if "p" in function:
        print(message)
    if "l" in function:
        if level == error:
            error(message)
        else:
            info(message)
    return 0

redis_host = environ.get("REDIS_HOST", "localhost")
redis_port = int(environ.get("REDIS_PORT", 6379))

try:
    r = StrictRedis(host = redis_host, port = redis_port, db = 0, decode_responses = True, socket_connect_timeout = 5)
    r.ping()
    print_and_log("Successfully connected to Redis!")
except exceptions.ConnectionError as e:
    print_and_log(f"Could not connect to Redis: {e}", error)
    r = None

@app.route("/")
def hello():
    standard_message = "Hello, World! Ariel Avinoam's app has been accessed."
    if r:
        try:
            count = r.incr("hits")
            success_message = f"Hello from Flask! I have been seen {count} times. Redis is connected." 
            print_and_log(success_message, info, "l")
            return standard_message + "<br>" + success_message
        except exceptions.ConnectionError as e:
            communication_error = f"Hello from Flask! Could not connect to Redis to get count: {e}"
            print_and_log(communication_error, error, "l")
            return standard_message + "<br>" + communication_error
    else:
        general_error = "Hello from Flask! Redis is not connected."
        print_and_log(general_error, error, "l")
        return standard_message + "<br>" + general_error
