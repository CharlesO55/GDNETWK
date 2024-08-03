// Submitted by: Charles Ong
import java.io.DataInputStream;
import java.net.Socket;

import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;

public class FileClient{
    private final String SAVE_FILENAME = "Received.txt";
    private String _strIP;
    private int _nPort;


    public static void main(String[] args){
        FileClient client = new FileClient();
        client.VerifyArgs(args);

        //BEGIN CONNECTION
        client.Connect();
    }

    private void VerifyArgs(String args[]){
        if(args.length != 2){
            this._strIP = "localhost";
            this._nPort = 8806; 
            System.out.println("\nClient: Insufficient args. Using defaults. IP: " + this._strIP + ", Port: " + this._nPort);
        }
        else{
            this._strIP = args[0];
            this._nPort = Integer.parseInt(args[1]);
        }
    }

    private void Connect(){
        System.out.println("\nClient: Connecting to server at " + this._strIP + "/" + this._nPort);

        try{
            Socket socket = new Socket(this._strIP, this._nPort);

            System.out.println("\nClient: Connected to server at " + socket.getRemoteSocketAddress());

            this.DownloadFile(socket);
            socket.close();
        }
        catch (Exception e){
            e.printStackTrace();
        }
        finally{
            System.out.println("\nClient: Connection is terminated");
        }
    }

    private void DownloadFile(Socket socket) throws Exception {
        DataInputStream iStream = new DataInputStream(socket.getInputStream());
        byte[] payload = iStream.readAllBytes();

        Path filePath = Paths.get(SAVE_FILENAME);
        Files.write(filePath, payload);

        System.out.println("\nClient: Downloaded file \"" + filePath.getFileName() + "\"(" + Files.size(filePath) + " bytes)");
    }
}