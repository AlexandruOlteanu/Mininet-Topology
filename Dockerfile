# Use Python runtime as a parent image
FROM python:3.11

# Set the working directory in the container
WORKDIR .

# Copy the current directory contents into the container at /usr/src/app
COPY . .

RUN pip install mininet

RUN pip install --upgrade pip

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Define environment variable
ENV NAME Topology

# Run app.py when the container launches
CMD ["python3.11", "topology.cpython-311.pyc", "alexandru.olteanu01", "-t"]
