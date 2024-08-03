// Submitted by: Charles Ong

import java.io.DataOutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.nio.file.Files;

public class FileServer{
    private final String IN_FILENAME = "Download.txt";
    private int _nPort;

    public static void main(String[] args){
        FileServer server = new FileServer();
        server.VerifyArgs(args);

        server.StartServer();
    }

    private void VerifyArgs(String args[]){
        if(args.length != 1){
            this._nPort = 8806;
            System.out.println("Server: Insufficient args. Using defaults. nPort: " + this._nPort);    
        }
        else{
            this._nPort = Integer.parseInt(args[0]);
        }
    }

    private void StartServer(){
        try{
            System.out.println("\nServer: Listening on port " + this._nPort);

            ServerSocket ss = new ServerSocket(this._nPort);
            Socket socket = ss.accept();
            System.out.println("\nServer: New client connected: " + socket.getRemoteSocketAddress());

            this.SendFile(socket);    

            socket.close();
        }
        catch (Exception e){
            e.printStackTrace();
        }
        finally{
            System.out.println("\nServer: Connection is terminated");
        }
    }

    private void SendFile(Socket socket) throws Exception{
        //READ THE FILE
        Path filePath = Paths.get(this.IN_FILENAME);
        byte[] payload = Files.readAllBytes(filePath);
        
        System.out.println("\nServer: Sending file: \"" + filePath.getFileName() + "\" (" + Files.size(filePath) + " bytes)");

        
        //SEND IT
        DataOutputStream oStream = new DataOutputStream(socket.getOutputStream());
        oStream.write(payload);
    }
}