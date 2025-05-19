Flask Redis Counter App
=======================

A simple Flask web application that increments a counter stored in Redis and logs activity to ./logs/app.log. When its main page is visited, it displays a "Hello, World! Ariel Avinoam's app has been accessed." message in the browser, along with the hit count.

This guide will help you set up and run this application using Docker.

PREREQUISITES
-------------
* Docker: Install Docker (find instructions at https://docs.docker.com/get-docker/)
* Docker Compose: Install Docker Compose (find instructions at https://docs.docker.com/compose/install/) (usually included with Docker Desktop)

IMPORTANT: Ensure your Docker engine (Docker Desktop or Docker daemon) is running before proceeding with the steps below.

PROJECT STRUCTURE
-----------------
When you clone this repository, the project will have the following structure:

'''text
 app.py            # Flask application code
├── Dockerfile        # Dockerfile for building the Flask app image
├── docker-compose.yml # Docker Compose configuration
├── requirements.txt  # Python dependencies
└── logs/             # Host directory for persistent application logs
    └── .gitkeep      # (Ensures the 'logs' directory is present after cloning)
'''

GETTING STARTED
---------------

1. Clone the Repository:
   Open your terminal or command prompt and run:

   git clone https://github.com/ArielAvin/DevOpsCourseProject
   cd DevOpsCourseProject

2. Log Directory Information:
   The application writes logs to a directory named `logs` in the project folder. This `logs` directory should be created automatically when you clone the repository.

BUILD AND RUN THE APPLICATION
-----------------------------
Navigate to the project's root directory (`DevOpsCourseProject`) in your terminal and run:

docker-compose up -d

This command will:
- Build the Docker images if they don't already exist or if changes have been made to the Dockerfile or application code since the last build.
- Start the Flask web application and the Redis service in detached mode (meaning the terminal will be free).
- Make the application's logs available in the `./logs/app.log` file on your computer.

ACCESS THE APPLICATION
----------------------
Once the command above is running and the services have started (you can check their status with `docker-compose ps`), open your web browser and go to:

http://localhost:5000/

Each time you visit this page, the browser will display "Hello, World! Ariel Avinoam's app has been accessed." followed by a message indicating the hit count and Redis connection status.

VIEWING LOGS
------------
- **Application Logs (File):** Application activity, including startup messages, Redis connection status, and page visits with hit counts, is logged to `./logs/app.log` within the project directory on your computer.
- **Container Console Logs:** Initial messages like Redis connection success or failure are also printed to the Flask container's standard output.
- Since the application is running in detached mode, you can view the combined console logs of all services using:
  docker-compose logs

- To view console logs for a specific service (e.g., the web application):
  docker-compose logs web
  (Or use `docker logs flask_web_app` if your container is named `flask_web_app` as per the `docker-compose.yml`).

TROUBLESHOOTING: LOG PERMISSIONS
--------------------------------
If logs aren't in `./logs/app.log`, it might be a permission issue. The Flask app in the container (runs as root, UID 0) needs write access to `./logs` on your host.

Secure Fixes:
* Linux/macOS: Ensure your user owns `./logs` and has write permission:
  `sudo chown -R $(id -u):$(id -g) ./logs`
  `chmod -R u+w ./logs`
  (The root user in container should then write. SELinux/AppArmor might interfere.)

* Windows (Admin PowerShell/CMD): Grant your user full control:
  `icacls "./logs" /grant "%USERNAME%":(F) /T`

Fallback (less secure, for local dev only if above fails):
* Linux/macOS: `sudo chmod -R 777 ./logs`
* Windows: `icacls "./logs" /grant Everyone:(F) /T`

After adjusting permissions, restart:
`docker-compose down --rmi all`
Then: `docker-compose up -d`

STOPPING THE APPLICATION
------------------------
1. To stop the running application (since it's in detached mode):

   docker-compose stop

2. To remove the containers, network, and all images used by services defined in the `docker-compose.yml` file (this will not delete your `./logs` directory):

   docker-compose down --rmi all

   (If you also want to remove the Docker volume used by Redis, which stores the counter data, you can add the `-v` flag: `docker-compose down -v --rmi all`. Note that `--rmi all` removes all images used by any service in the Compose file, which can be useful for a clean slate but might require re-downloading/re-building images later.)
