# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR .

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME Topology

# Run app.py when the container launches
CMD ["python3", "topology.cypython-311.pyc", "alexandru.olteanu01"]
