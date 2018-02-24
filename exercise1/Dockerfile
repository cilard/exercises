# Use Ubuntu Xenial image
FROM ubuntu:16.04

# Update repoistories cache and install pip
RUN apt-get update && apt-get install -y python3-pip

# Upgrade pip and install libratry for OWM web API
RUN pip3 install --upgrade pip && pip3 install pyowm

# Set the working directory
WORKDIR /app

# Add 'getweather.py' script to the image
ADD ./getweather.py /app

# Run /app/getweather.py when container launches
ENTRYPOINT ["python3", "getweather.py"]
