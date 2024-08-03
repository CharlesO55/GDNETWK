import java.io.DataInputStream;
import java.io.DataOutputStream;
import java.io.IOException;
import java.net.Socket;

public class Client {
    public String username;
    public String message;

    private Socket socket;

    private DataInputStream reader;
    private DataOutputStream writer;

    public Client(Socket socket) throws Exception{
        this.socket = socket;

        this.reader = new DataInputStream(socket.getInputStream());
        this.writer = new DataOutputStream(socket.getOutputStream());

        this.username = this.reader.readUTF();
        this.message = this.reader.readUTF();

        this.start();
    }

    private void start(){
        System.out.println("New client "+ username +" connected from: " + socket.getRemoteSocketAddress());
    }

    public String read() throws Exception{
        return this.reader.readUTF();
    }
    public void send(String msg){
        try{
            this.writer.writeUTF(msg);
        } catch (IOException e){
            this.closeConnection();
        }
    }
    public void closeConnection(){
        try{
            this.socket.close();
        }catch(Exception e){}
    }
}