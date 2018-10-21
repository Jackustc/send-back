import parsingconfig
from jpype import *
import sys
import socket
import socks
from io import BytesIO
import struct

#Since we deliver message from java module to python module, 
#I think it is ok to just use this socket function to directly
#deliver and process the message
#Need to figure out whether it is true. 
def connect_to_channel(hostname,port,id):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print 'socket created'
    newport = int(port)+int(id)
    #sock.bind(("localhost", newport))

    sock.bind((hostname, newport))  #James.  Replaced localhost with parameter passed in.
    
    sock.listen(1)
    return sock

def listen_to_channel(sock):
    while 1:
        conn,addr = sock.accept()
        print "got a message..."
        try:
            buf = conn.recv(1024)
            #print buf
            tmp = BytesIO(buf)
            sequence,cid,length = struct.unpack('>iii', tmp.read(12))
            msg = tmp.read(length)
            if msg=="Dummy Test Request":
                print "good."
                print "We have assigned sequence number ",sequence," for client ",cid, " and request ",msg
        except:
            print "may have got a not well-formatted message" 
            #TODO: Need to figure out why sometimes there are empty or not well-formatted messages
            pass
        
if __name__ == '__main__':
    if len(sys.argv[1:])<1:
        print "Use: python BFTServer.py <ReplicaID>"
        exit()

    replicaID = sys.argv[1]
    
    (n,f,host,baseport) = parsingconfig.readconfig()   #Read in the config number of replicas, failures, host, and port number.
    sock = connect_to_channel(host,baseport,replicaID) #The parameters to connect_to_channel are (hostname,port,id)
 
    #original classpath:
    #classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bft-smart/bin/BFT-SMaRt.jar"


    #James.  Changed classpath, specifically the path to BFT-SMaRt.jar.  Commented out the original
    classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bin/BFT-SMaRt.jar"

    startJVM(getDefaultJVMPath(),"-Djava.class.path=%s"%classpath)

    KVServerClass = JPackage("bftsmart.demo.keyvalue") #Create instance of KVServer class from the demo/keyvalue/KVServer.java class
    KVServerClass.KVServer.passArgs((replicaID,"1"))   #James.  TO DO:  Change this call to include host and port number.
    
    listen_to_channel(sock)
    

    # and you have to shutdown the VM at the end
    shutdownJVM()
