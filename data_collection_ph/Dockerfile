FROM python:3.9

RUN pip3 install --no-cache-dir rpi.gpio 
RUN pip3 install spidev
RUN pip3 install PyMLX90614
RUN pip3 install smbus2


# Copy the application code into the container
COPY . .



# Start the CherryPy server
CMD ["python3", "phSensor.py"]
 