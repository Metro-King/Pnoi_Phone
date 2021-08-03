import bluetooth
import os
from datetime import datetime
host = ""
port = 1
name=''
command_lineStop2 = 'sudo pkill -f bluetooth-sendto'
command_lineStop1 = 'pkill arecord'

#command_lineStart = 'arecord -D plughw:3,0 --rate=16000 test1.wav & arecord -D plughw:4,0 --rate=16000 test2.wav'
server = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
print('Bluetooth Socket Created')
#path_y=/home/pi/Rohan-27-07-2021-02:07:21-mouth.wav
try:
        server.bind((host, port))
        print("Bluetooth Binding Completed")
except:
        print("Bluetooth Binding Failed")
server.listen(1) # One connection at a time
# Server accepts the clients request and assigns a mac address.
client, address = server.accept()
print(address[0])
#print("Connected To", address)
print("Client:", client)

mems_send='bluetooth-sendto --device='+ address[0] +' /home/pi/sample1.wav '
now=datetime.now()
dt_string=now.strftime("%d-%m-%Y-%H:%M:%S")
print(dt_string)
try:
        while True:
                # Receivng the data.
                data = client.recv(1024)
                 
                #print(data)# 1024 is the buffer size
                if data == b'\x01':
                    command_lineStart = 'arecord -D plughw:3,0 --rate=16000 '+str(name)+'-'+str(dt_string)+'-'+'mouth.wav & arecord -D plughw:4,0 --rate=16000 ' +str(name)+'-'+str(dt_string)+'-'+'breath.wav'
                    os.popen(command_lineStart)
                elif data ==b'\x02':
                    os.popen(command_lineStop1)
                elif data ==b'\x03':
                    os.popen(command_lineStop2)
                elif data == b'\x04':
                    print(name)
                    command_lineSend1 = 'bluetooth-sendto --device=' + address[0] +' /home/pi/Desktop/'+name+'-'+str(dt_string)+'-'+'mouth.wav'
                    print(command_lineSend1)
                    os.popen(command_lineSend1)
                elif data == b'\x05':
                    command_lineSend2 = 'bluetooth-sendto --device=' + address[0] +' /home/pi/Desktop/'+name+'-'+str(dt_string)+'-'+'breath.wav'
                    
                    os.popen(command_lineSend2)
                elif data == b'\x06':
                    mems='arecord -D plughw:2 -c2 -r 16000 -f S32_LE -t wav -V stereo -v '+str(name)+'-'+str(dt_string)+'-'+'mems.wav'
                    os.popen(mems)
                elif data == b'\x07':
                    mems_send='bluetooth-sendto --device='+ address[0] +' /home/pi/Desktop/'+str(name)+'-'+str(dt_string)+'-'+'mems.wav'
                    os.popen(mems_send)
                data=data.decode('utf-8')# to decode the name out of it
                if type(data)==str and data.isalpha() :
                    #data=data.decode('utf-8')
                    ##print(data)
                    name=data
                    print(name)

except:
        
        # Closing the client and server connection
        client.close()
        server.close()
