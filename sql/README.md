*Docker Container Setup - Local*

**Instructions**
1. Pull the MySQL image

```bash
docker pull mysql
```
2. Create a container
```bash
docker run --name AntHalls_container -p 3306:3306 -e MYSQL_ROOT_PASSWORD=password -d mysql
```
    + --name: Container name
    + -p: Ports [Host]:[Container port]
    + -e: password for mysql
    + -d: image to use
3. Use an IDE to connect
    * Connecting to port 3307
4. Run ./init.sql