__author__ = 'Felix A. Goebel'

import log, serial, time
from serial.tools import list_ports
from serial import SerialException

class Controller():

    def __init__(self) -> None:

        ports = self.get_ports()
        log.logging.info(f'Ports -> {ports}')
        arduino_port = self.get_arduino_port(ports)
        
        try:
            self.arduino = serial.Serial(port=arduino_port, baudrate=115200, timeout=.1)
        except SerialException:
            log.logging.error(f'Port {arduino_port} can not be found or configured!')
        except ValueError:
            log.logging.error(f'Parameters of Serial Port are out of range!')
        except:
            log.logging.error(f'An error occured when trying to create the port {arduino_port}!')

        if self.arduino.port == None:
           
            self.disconnected = True
            log.logging.error(f'The Arduino could not be found and/ or configured!')
        else:
            self.disconnected = False
            log.logging.info(f'The Arduino is listening on port {arduino_port}.')


    # Check for all active ports
    def get_ports(self) -> list[(str, str)]:
        port = list(list_ports.comports())
        ports = []
        for p in port:
            ports.append((p.name, p.manufacturer))
        return ports

    # If arduino is present, return the corresponding port
    def get_arduino_port(self, ports) -> str:
        for port in ports:
            description = port[1].split()
            for d in description:
                if d.lower() == "arduino":
                    return port[0]
        return None
    
    def reconnect(self):
        was_connected = True
        if self.arduino.port == None:
            was_connected = False

        ports = self.get_ports()
        arduino_port = self.get_arduino_port(ports)

        if arduino_port != None:
            self.disconnected = False
            # It actually helps to wait for other threads, otherwise the first 1... 10 reconnection attempts fail with the current setup 
            time.sleep(.1)
            
            try:
                self.arduino.port = arduino_port
                self.arduino.open()
                if was_connected:
                    log.logging.info(f"The Arduino reconnected on port {arduino_port}.")
                else:
                    log.logging.info(f"The Arduino is now listening on port {arduino_port}.")

            except SerialException:
                log.logging.error(f'Can not open Serial Connection on port {arduino_port}')
                self.arduino.close()
                self.disconnected = True
            except:
                log.logging.error(f'Something went wrong while trying to reconnect.')

 
