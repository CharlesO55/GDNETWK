import java.net.Socket;
import java.net.ServerSocket;
import java.io.*;


public class Server {
    public static void main (String[] args){
        System.out.println("Server start");
        
        try{
            ServerSocket serverSocket = new ServerSocket(8806);
            Socket socket = serverSocket.accept();


            BufferedReader clientInput = new BufferedReader(new InputStreamReader(socket.getInputStream()));
            String clientMessage = clientInput.readLine();

            System.out.println("Server received: " + clientMessage);


            socket.close();
            serverSocket.close();
        }
        catch (Exception e){
            e.printStackTrace();           
        }


        System.out.println("Server end");
    }    
}