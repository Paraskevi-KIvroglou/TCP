import socket
import sys
import time
import subprocess
#We use this command in order to specify how many arguments we can give.
assert(len(sys.argv)==2)
#We assign to varibales the values from argv
t=sys.argv[1].split(",") #We strip the content of the argument
TCP_List=list(t) #TCP list made
TCP_List[0]=TCP_List[0][1:]
TCP_List[-1]=TCP_List[-1][:-1]

def interface_output(): #Parsing the output that we want from ifconfig resutl
    output1 = subprocess.check_output(['ifconfig'])
    print ('Have %d bytes in output' % len(output1))
    output=output1.decode()
    print (output)
    Lines=output.splitlines()
    L=Lines[1].split()
    return L[1]
#Open file with configurations
ListIP=["","",""]
Dhost={}
Dinter={}
f=open("config.txt","r")
L=f.readlines() #Read all the lines of the file in a list
f.close()
for i in range(len(L)): #Parse the list with split method
#I chooce how to split the lines the ones with i even are the ones that contain information about the routers
    s=L[i].split()
    s0=s[0].split("-")
    print(s0)
    if s0[1]=='host':
        key=str(s[0])
        Dhost[key]=s[1]
    else:
        key1=str(s[0])
        Dinter[key1]=s[1].split(",")

print("The dictionary with all the available host IPs: ")
print(Dhost)
print("The dictionary with all the available interfaces in our AS66: ")
print(Dinter)
for j in Dhost.items():
    if (j[0]==TCP_List[0]):
        ListIP[0]=j[1]
    if (j[0]==TCP_List[1]):
        ListIP[1]=(j[1])
    if (j[0]==TCP_List[2]):
        ListIP[2]=(j[1])
print("The hosts we need to execute ping and traceroute: ")
print(TCP_List)
print("And their IPs: ")
print(ListIP)
#Socket creating and sending message to senders...
client_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Sockets successfully created.")
message="ping,traceroute,"+str(ListIP[0])+","+str(ListIP[1])+","+str(ListIP[2])
print(len(message))
#Create connection to send message to other host
client_sock.connect((ListIP[1],50008))
print("COnnected")
client_sock.send(message.encode())
client_sock.close()
#Now we will do the same for other IP Routes
####################################################################################
ip_local=interface_output() #Now here we receive again from the same port the data that comes in from the server
BUFFER_SIZE=254
client_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_sock.bind((ip_local,50008))
client_sock.listen()
conn,addr=client_sock.accept() #Accerted like in the theory handshake
print("Connection established with: ",addr[0])
Ping_Latency=[] #Ping Latency list that stores ping measurements
Traceroute_Route=[] #Traceroutes result from the data
while True:
    data=conn.recv(BUFFER_SIZE)
    data_de=data.decode()
    if data_de:
        print("THe data was send: ",data_de,addr[0],addr[1])
    Data=data_de.split("|")
    for da in range(len(Data)):
        if da<=2:
            Ping_Latency.append(Data[da])
        else:
            Traceroute_Route.append(Data[da])
    if len(Ping_Latency)==3:
        break
conn.close()
client_sock.close()
print(Ping_Latency)
print(Traceroute_Route)
print("Now we start storing: ")
Ping_Latency[0]+=Traceroute_Route[0]
Traceroute_Route.remove(Traceroute_Route[0])
print(Traceroute_Route)
#for trace in range(len(Traceroute_Route)-1):
    #Ping_Latency.append(Traceroute_Route[trace])
print(Ping_Latency)
print(Traceroute_Route)
Traces=Traceroute_Route[-1]
print(Traces) #With this function we store as it supposed to the traceroutes from the output in Traceroute _ROute
def Routing_List(Traces):
    Routes=[]
    tmp0=""
    for i in range(len(Traces)):
        if Traces[i]=="[":
            continue
        if Traces[i]=="]":
            continue
        if Traces[i]=="'":
            continue
        if Traces[i]=="'":
            continue
        if Traces[i]==",":
            Routes.append(tmp0)
            tmp0=""
            continue
        if Traces[i]==" ":
            continue
        tmp0+=Traces[i]
        if i==len(Traces)-1:
            Routes.append(tmp0)
    print(Routes)
    return Routes
def Pairs(ListIP): #Now we translate the pairs by using the ips in the message send back to server
    pairs=[]
    for na in range(len(ListIP)):
        inr=ListIP.index(addr[0])
        if ListIP[na]==addr[0]:
            continue
        else:
            pairs.append(TCP_List[na]+"-"+TCP_List[inr])
    print(pairs)
    return pairs
#The Pairs and ROures translated for 2nd IP
Route1=Routing_List(Traces)
Pairs1=Pairs(ListIP)
def Transorm(): #Transform the ip of hops from the file
    Transformation=[]
    for ro in Route1:
        print(ro)
        for item in Dinter.items():
            B=item[1]
            for it in range(len(B)):
                if ro==B[it]:
                    Transformation.append(item[0])
    print(Transformation)
    return Transformation
Transformation=Transorm()
D_Final={}
key=Pairs1[0]
D_Final[key]=Transformation[0:2]
D_Final[key].append(Ping_Latency)
D_Final[key].append(len(Transformation[0:2]))
key1=Pairs1[1]
D_Final[key1]=Transformation[2:4]
D_Final[key1].append(Ping_Latency)
D_Final[key1].append((len(Transformation[2:4])))
print(D_Final)
#SAme for the other 2 servers left ....
#################################################################
#Open in the client as server to listen the results
client_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Sockets successfully created.")
message="ping,traceroute,"+str(ListIP[0])+","+str(ListIP[1])+","+str(ListIP[2])
print(len(message))
#Create connection to send message to other host
client_sock.connect((ListIP[2],50008))
print("COnnected")
client_sock.send(message.encode())
client_sock.close()
#Now for the Last ROute
client_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_sock.bind((ip_local,50008))
client_sock.listen()
conn,addr=client_sock.accept()
print("Connection established with: ",addr[0])
Ping_Latency=[]
Traceroute_Route=[]
while True:
    data=conn.recv(BUFFER_SIZE)
    data_de=data.decode()
    if data_de:
        print("THe data was send: ",data_de,addr[0],addr[1])
    Data=data_de.split("|")
    for da in range(len(Data)):
        if da<=2:
            Ping_Latency.append(Data[da])
        else:
            Traceroute_Route.append(Data[da])
    if len(Ping_Latency)==3:
        break
conn.close()
client_sock.close()
print(Ping_Latency)
print(Traceroute_Route)
print("Now we start storing: ")
Ping_Latency[0]+=Traceroute_Route[0]
Traceroute_Route.remove(Traceroute_Route[0])
print(Traceroute_Route)
for trace in range(len(Traceroute_Route)-1):
    Ping_Latency.append(Traceroute_Route[trace])
print(Ping_Latency)
print(Traceroute_Route)
Traces=Traceroute_Route[-1]
print(Traces)
#Transformation the routes to name of hops
D_Final2={}
Transformation=Transorm()
key2=Pairs1[0]
D_Final2[key2]=Transformation[0:2]
D_Final2[key2].append(Ping_Latency)
D_Final2[key2].append(len(Transformation[0:2]))
key3=Pairs1[1]
D_Final2[key3]=Transformation[2:4]
D_Final2[key3].append(Ping_Latency)
D_Final2[key3].append((len(Transformation[2:4])))
print(D_Final2)
#####################################################
#Now we do the same process for other servers
client_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
print("Sockets successfully created.")
message="ping,traceroute,"+str(ListIP[0])+","+str(ListIP[1])+","+str(ListIP[2])
print(len(message))
#Create connection to send message to other host
client_sock.connect((ListIP[0],50008))
print("COnnected")
client_sock.send(message.encode())
client_sock.close()
client_sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_sock.bind((ip_local,50008))
client_sock.listen()
conn,addr=client_sock.accept()
print("Connection established with: ",addr[0])
Ping_Latency=[]
Traceroute_Route=[]
while True:
    data=conn.recv(BUFFER_SIZE)
    data_de=data.decode()
    if data_de:
        print("THe data was send: ",data_de,addr[0],addr[1])
    Data=data_de.split("|")
    for da in range(len(Data)):
        if da<=2:
            Ping_Latency.append(Data[da])
        else:
            Traceroute_Route.append(Data[da])
    if len(Ping_Latency)==3:
        break
conn.close()
client_sock.close()
print(Ping_Latency)
print(Traceroute_Route)
print("Now we start storing: ")
Ping_Latency[0]+=Traceroute_Route[0]
Traceroute_Route.remove(Traceroute_Route[0])
print(Traceroute_Route)
for trace in range(len(Traceroute_Route)-1):
    Ping_Latency.append(Traceroute_Route[trace])
print(Ping_Latency)
print(Traceroute_Route)
Traces=Traceroute_Route[-1]
print(Traces)
#Transformation the routes to name of hops
D_Final1={}
Transformation=Transorm()
key5=Pairs1[0]
D_Final1[key5]=Transformation[0:2]
D_Final1[key5].append(Ping_Latency)
D_Final1[key5].append(len(Transformation[0:2]))
key6=Pairs1[1]
D_Final1[key6]=Transformation[2:5]
D_Final1[key6].append(Ping_Latency)
D_Final1[key6].append((len(Transformation[2:4])))
print(D_Final1)

print("The final dict: ")
D_Final.update(D_Final1)
D_Final.update(D_Final2)
print(D_Final)
