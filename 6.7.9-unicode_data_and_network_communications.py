# encoding:utf-8
## 6.7.9 Unicode data and Network Communication
# Network sockets are also byte streams, like stdin and stdout.
import sys, SocketServer

# use makefile() to get a file-like handle for the socket,
# wrap that handle with a stream-based reader or writer
# then unicode strings will get encoded on their way in or out.

class Echo(SocketServer.BaseRequestHandler):
    def handle(self):
        # Get some bytes and echo them back to the client
        # There is no need to decode them, since they are not used
        data = self.request.recv(1024)
        self.request.send(data)
        return
        
class PassThrough(object):
    
    def __init__(self, other):
        self.other = other
    
    def write(self, data):
        print 'Writing :', repr(data)
        return self.other.write(data)
    
    def read(self, size=-1):
        print 'Reading :',
        data = self.other.read(size)
        print repr(data)
        return data
        
    def flush(self):
        return self.other.flush()
        
    def close(self):
        return self.other.close()
        
if __name__ == '__main__':
    import codecs, socket, threading
    
    address = ('localhost', 0) # auto-port number
    server = SocketServer.TCPServer(address, Echo)
    
    # Set up server
    t = threading.Thread(target=server.serve_forever)
    t.setDaemon(True) # don't hang on exit
    t.start()
    
    # Connect to server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect( server.server_address )
    
    # Wrap the socket with a reader and a writer
    incoming = codecs.getreader('utf-8')(PassThrough( s.makefile('r') ))
    outgoing = codecs.getwriter('utf-8')(PassThrough( s.makefile('w') ))
    
    # Send the data
    data = u"pi: π"
    print 'Sending :', repr(data)
    outgoing.reset()
    outgoing.write(data)
    outgoing.flush()
    
    # Receive a response
    response = incoming.read()
    print 'Received:', repr(response)
    
    #Clean up
    s.close()
    server.socket.close()