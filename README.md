# SolVro - backend project

Project was accomplished using Flask as http server and MySQL as SQL server.
Used technologies: python, Flask, MySQL, git, Docker.

In order to run this project a few steps must be accomplished:
0. Create a docker network for ease of connection between the MySQL engine and provided Flask server:
- `sudo docker network create <network_name>`

1. Build and run the database container:
- run following commands from "mySQLContainer" folder
- `sudo docker build -t <sql_container_name> .`
- `sudo docker run --name <sql_container_id> -d -e MYSQL_ROOT_PASSWORD=<root_password> --net=<network_name> <sql_container_name>`

2. Build and run the server container:
- run following commands from the main project folder
- `sudo docker build -t <server_container_name> .`
- `sudo docker run --name <server_container_id> -d -p 5000:5000 --net=<network_name> <server_container_name> -a <sql_container_id>` 

3. That's it! You can request the server through:
- `curl -i -H "Content-Type: application/json" [-X <method>] [-d <arguments>] http://0.0.0.0:5000/lists`

Important notes!
- Remember to shutdown the services through `sudo docker stop <service-id>` in order to prevent data loss. You can restart the services through `sudo docker start <service-id>`.
- Added a functionality under address of `http://0.0.0.0:5000/restartDB` in order to try restoring a connection to the database service (after DB service restart).

