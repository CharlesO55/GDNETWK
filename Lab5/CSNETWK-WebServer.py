from socket import *


class WebServer:
    def __init__(self, HOST, PORT):
        self.HOST = HOST;
        self.PORT = PORT;

        self.serverSocket = socket(AF_INET, SOCK_STREAM)
        self.serverSocket.bind((HOST, PORT));
        self.serverSocket.listen();
    
        self.start();
    

    def start(self):
        while True:
            print('CSNETWK Web Server is ready to serve at ' + self.HOST + ':' + str(self.PORT))
            connectionSocket, addr = self.serverSocket.accept();    

            try:        
                # /GET /CSNETWK.html /...
                request = connectionSocket.recv(1024).decode();

                filename = request.split()[1][1:];
                f = open(filename, 'rb');
                outputdata = f.read();
                f.close();

                #Send one HTTP header line into socket
                connectionSocket.send(b'HTTP/1.1 200 OK\r\n');
                connectionSocket.send(self.getFileTypeHeader(filename));                
                # connectionSocket.send(b'Content-Type: text/html\n\n');


                #Send the content of the requested file to the client
                outputdata
                connectionSocket.send(outputdata);

                connectionSocket.send(b'\r\n\r\n');
                connectionSocket.close();
            
            except IOError:
                connectionSocket.send(b'HTTP/1.1 404 Not Found\r\n');
                connectionSocket.close();

        self.serverSocket.close()


    def getFileTypeHeader(*filename):
        header = 'Content-Type: ';
        type = filename[1].split('.')[1]

        if type in ('html', 'txt', 'md'):
            header += 'text/';
        elif type in ('png', 'jpg', 'jpeg', 'gif'):
            header += 'image/';
        else:
            raise Exception("Unhandled file type: " + type);

        header += type + '\n\n';
        return header.encode();
                


# py CSNETWK-WebServer.py
WebServer("127.0.0.1", 3000);