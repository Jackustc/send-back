#import parsingconfig
from jpype import *
#from ..threshenc.tdh2 import encrypt,decrypt

if __name__ == '__main__':

    if len(sys.argv[1:])<3:
        print "Use: python BFTClient.py <process id> <increment> <number of operations>"
        exit()

    processID = sys.argv[1]
    increment = sys.argv[2]
    nops = sys.argv[3]

    #(n,f,host,baseport) = parsingconfig.readconfig() #James.  Commented out.
    #print (n,f,host,baseport)

    #Original
    #classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bft-smart/bin/BFT-SMaRt.jar"
    

    #James.  Changed classpath, specifically the path to BFT-SMaRt.jar.  Commented out the original
    classpath = "lib/commons-codec-1.5.jar:lib/core-0.1.4.jar:lib/netty-all-4.1.9.Final.jar:lib/slf4j-api-1.5.8.jar:lib/slf4j-jdk14-1.5.8.jar:bin/BFT-SMaRt.jar"
    startJVM(getDefaultJVMPath(),"-Djava.class.path=%s"%classpath)

    # you can then access to the basic java functions
    #java.lang.System.out.println("hello world")

    KVClientClass = JPackage("bftsmart.demo.keyvalue")
    KVClientClass.KVClient.test()
    KVClientClass.KVClient.passArg((processID,increment,nops))
    for i in range(int(nops)):
        KVClientClass.KVClient.sendRequest("Dummy Test Request")

    # and you have to shutdown the VM at the end
    shutdownJVM()
