import java.net.Socket;
import java.io.*;

public class Client{
    public static void main (String[] args){
        System.out.println("Client started");
        
        try{
            Socket socket = new Socket("localhost", 8806);

            PrintWriter stream = new PrintWriter(socket.getOutputStream());
            
            BufferedReader clientInput = new BufferedReader(new InputStreamReader(System.in));
            stream.println(clientInput.readLine());
            stream.flush();



            socket.close();
        }
        catch (Exception e){
            e.printStackTrace();
        }
               
        System.out.println("Client end");
    }
}