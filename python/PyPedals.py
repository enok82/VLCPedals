'''
Created on 11 apr. 2017

@author: stefan
'''
from telnetlib import Telnet
from serial import Serial
from time import sleep

class VlcControl:
    def __init__(self):
        self.telnetConnection = Telnet("localhost", 4212)
        
        telnetBuffer = ""

        while not telnetBuffer.endswith("Password: "):
            telnetBuffer = self.telnetConnection.read_eager()

            telnetBuffer = telnetBuffer.decode("utf-8")
            
            if telnetBuffer != '':
                print(telnetBuffer)
        
        self.sendCommand(b"python\n")
        
        telnetBuffer = ""
        
        while not telnetBuffer.endswith("> "):
            telnetBuffer = self.telnetConnection.read_eager()

            telnetBuffer = telnetBuffer.decode("utf-8")
            
            if telnetBuffer != '':
                print(telnetBuffer)
        
                                       
    def sendCommand(self, cmd):
        self.telnetConnection.write(cmd)

class SerialControl:
    def __init__(self, port = "COM10"):
        self.serialConnection = Serial(port, 9600, timeout = 0)

if __name__ == '__main__':
    vlcControl = VlcControl()
    
    serialControl = SerialControl()
    
    playbackRate = 1
    
    while True:
        sleep(0.2)
        
        receivedCommand = serialControl.serialConnection.readline().strip().decode("utf-8")
        
        if receivedCommand == "#0+0":
            vlcControl.sendCommand(b"seek +15\n")
            
            print(receivedCommand)
            
        elif receivedCommand == "#1+0":
            vlcControl.sendCommand(b"pause\n")
            
            print(receivedCommand)
            
        elif receivedCommand == "#2+0":
            vlcControl.sendCommand(b"seek -15\n")
            
            print(receivedCommand)
        
        elif receivedCommand == "#0+1":
            playbackRate += 0.1
            
            vlcControl.sendCommand(str.encode("rate {}\n".format(playbackRate)))
            
            print(receivedCommand)
        
        elif receivedCommand == "#1+1":
            playbackRate = 1
            
            vlcControl.sendCommand(str.encode("rate {}\n".format(playbackRate)))
            
            print(receivedCommand)
            
        elif receivedCommand == "#2+1":
            playbackRate -= 0.1
            
            vlcControl.sendCommand(str.encode("rate {}\n".format(playbackRate)))
            
            print(receivedCommand)
        
        elif receivedCommand != "":
            print(receivedCommand)
            
        receivedCommand = ""
            