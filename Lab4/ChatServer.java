import java.net.ServerSocket;
import java.net.Socket;

public class ChatServer {
    private ServerSocket _serverSocket;
    private int _nPort;

    private ChatServer(int nPort){
        this._nPort = nPort;
    }
    

    public void start(){
        try{
            this._serverSocket = new ServerSocket(this._nPort);
            consoleLog("Listening to port " + this._nPort);

            while (!this._serverSocket.isClosed()){
                Socket newClient = this._serverSocket.accept();
                consoleLog("A new client has connected from " + newClient.getRemoteSocketAddress());

                
                Thread newThread = new Thread(new ClientHandler(newClient));
                newThread.start();
            }

        }
        catch (Exception e){
            e.printStackTrace();
        }
    }

    public void terminate(){
        try{
            if(this._serverSocket != null)
                this._serverSocket.close();
        }
        catch (Exception e){}
        consoleLog("Server closed");
    }

    private void consoleLog(String message){
        System.out.println("\nSERVER: " + message);
    }

    public static void main (String[] args){
        ChatServer server = new ChatServer(8880);
        server.start();
    }   
}