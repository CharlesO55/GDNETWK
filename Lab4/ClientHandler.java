import java.util.ArrayList;
import java.net.Socket;
import java.io.DataInputStream;
import java.io.DataOutputStream;


public class ClientHandler implements Runnable{
    public static ArrayList<ClientHandler> CH_Instances = new ArrayList<>();

    private Socket _socket;
    private DataInputStream IN;
    private DataOutputStream OUT;
    private String _username;

    public ClientHandler(Socket socket) throws Exception{
        this._socket = socket;
        this.IN = new DataInputStream(_socket.getInputStream());
        this.OUT = new DataOutputStream(_socket.getOutputStream());

        this._username = IN.readUTF();

        CH_Instances.add(this);

    }

    @Override
    public void run(){
        String message;
        while (this._socket.isConnected()) {
            try {
                message = IN.readUTF();
                broadcastMessage(this._username + ": " + message + '\n');
            }
            catch (Exception e) {
                // e.printStackTrace();
                removeClient();
                break;
            }
        }
    }

    public void broadcastMessage(String message) throws Exception{
        for (ClientHandler instance : CH_Instances){
            if(!instance._username.equals(this._username)){
                instance.OUT.writeUTF(message);
                instance.OUT.flush();
            }           
        }
    }

    public void removeClient(){
        try{
            broadcastMessage(this._username + " has disconnected\n");
        
            if(this.IN != null)
            this.IN.close();
            if(this.OUT != null)
                this.OUT.close();
            if(this._socket != null)
                this._socket.close();
        }
        catch (Exception e){}
        
        CH_Instances.remove(this);
    }
}