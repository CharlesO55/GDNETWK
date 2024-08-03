import java.net.Socket;
import java.io.DataInputStream;
import java.io.DataOutputStream;

public class ChatClient{
    private Socket _socket;
    private DataInputStream IN;
    private DataOutputStream OUT;
    private String _username;


    public ChatClient(){
        this._socket = new Socket(8806);
    }

    public void start(){

    }

    public static void main(String args[]){
        ChatClient client = new ChatClient();
        client.start();
    }  
}