import socket
import sys
import time
import subprocess
import re

assert(len(sys.argv)==1)
BUFFER_SIZE=48
def interface_output(): #Parsing the output that we want from ifconfig resutl
    output1 = subprocess.check_output(['ifconfig']) #From the ifconfig output we have stored the output
    print ('Have %d bytes in output' % len(output1))
    output=output1.decode()
    print (output)
    Lines=output.splitlines() #Splitting the lines from output
    L=Lines[1].split()
    return L[1] #Return the first one
def ping_result(ip_ping): #THis function will be the one that executed ping and stores the output
    output1=subprocess.check_output(['ping','-c','3',ip_ping])
    print ('Have %d bytes in output' % len(output1))
    output=output1.decode()
    print (output)
    Lines=output.splitlines()
    L=Lines[-1].split()
    print(Lines[-1])
    return L
def traceroute_result(ip_traceroute): #THis is the tracerooute function and stores the output
    output1=subprocess.check_output(['traceroute',ip_traceroute])
    print ('Have %d bytes in output' % len(output1))
    output=output1.decode()
    print (output)
    Lines=output.splitlines()
    L=[]
    for line in Lines:
        line_t=line.split()
        L.append(line)
    return L
sock_server1=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Creating the sockets
print("Sockets have been successfully created.")
ip_local=interface_output()
print(ip_local) #Ip found
TCP_Port=50008 #We set the port
sock_server1.bind((ip_local,TCP_Port)) #Bind the socket communication
sock_server1.listen(1)#LIstewn to one active communication
(connection,address)=sock_server1.accept()
print("Connection has been established with: ",address[0]) #Connection established
Pings=[]
Traceroutes=[]
while True: #We will receve the new data and divide them properly
    data=connection.recv(BUFFER_SIZE)
    data_d=data.decode()
    p_data=data_d.split(",")
    print(p_data)
    loops=0;
    for i in p_data:
        loops=loops+1
        if loops==6:
            break
        if p_data==ip_local:
            Pings.append(" ")
            Traceroutes.append(" ")
        else:
            if i=="ping":
                continue
            if i=="traceroute":
                continue
            Pings.append(ping_result(i))
            Traceroutes.append(traceroute_result(i))
    if len(Pings)==3 and len(Traceroutes)==3:
        break

connection.close()
sock_server1.close()
print("Socket connection closed.")
print(Pings)
print(Traceroutes)
IProute=[] #More splitting and dividing data
for trace in Traceroutes:
    for route in trace:
        new_trace=route.split("(")
        new_r=new_trace[1].split(")")
        IProute.append(new_r)
print(IProute)
listn=[]
for tracing in IProute:
    if tracing[0]==ip_local:
        continue
    else:
        listn.append(tracing[0])
print(listn)
#All the process of data
x=listn.count(p_data[2])
x1=listn.count(p_data[3])
x2=listn.count(p_data[4])
indexes=[]
if x>=1:
    s0=listn.index(p_data[2])
    indexes.append(s0)
if x1>=1:
    s1=listn.index(p_data[3])
    indexes.append(s1)
if x2>=1:
    s2=listn.index(p_data[4])
    indexes.append(s2)
print(indexes)
NewIProute={}
key=listn[int(indexes[0])]
NewIProute[key]=listn[1:indexes[1]]
key1=listn[int(indexes[1])]
NewIProute[key1]=listn[int(indexes[1])+1:]
print(NewIProute)
#COnnecting after extracting data to send them back to client
sock_server1=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #Creating new socket to send info back to client
print("Sockets have been successfully created.")
sock_server1.connect((address[0],TCP_Port))
totalb=0
for i in range(len(Pings)):
    mt=" "
    for ping in Pings[i]:
        mt+=ping+"|"
    sock_server1.send(mt.encode())
    totalb+=len(mt.encode())
sock_server1.send(str(NewIProute[key]).encode())
totalb+=len(str(NewIProute[key]).encode())
sock_server1.send(",".encode())
sock_server1.send(str(NewIProute[key1]).encode())
totalb+=len(str(NewIProute[key1]).encode())
print("The total transmitted bytes are: ",totalb)
print(Pings)
print(NewIProute)
sock_server1.close() #Close the socket so after the program run will not be any problems to use the sam port 
