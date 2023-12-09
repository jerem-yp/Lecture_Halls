# Use the official MySQL image as the base image
FROM mysql:latest

# Copy custom MySQL configurations or initialization scripts if needed
COPY init.sql /docker-entrypoint-initdb.d/

# Expose the default MySQL port
EXPOSE 3306

# Define a build argument for the MySQL root password
ARG MYSQL_ROOT_PASSWORD

# Set the MySQL root password using the build argument as an environment variable
ENV MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD}

# format: docker build --build-arg MYSQL_ROOT_PASSWORD=your_password -t my-mysql-image .