import java.net.*;
import java.util.ArrayList;

public class ChatServer
{
	public static void main(String[] args)
	{
		int nPort = Integer.parseInt(args[0]);
		System.out.println("Server: Listening on port " + nPort + "...");
		ServerSocket serverSocket;
		
		ArrayList <Client> clientsList = new ArrayList<>();

		try 
		{
			serverSocket = new ServerSocket(nPort);

			while (true) {
				Client newClient = new Client(serverSocket.accept());
				clientsList.add(newClient);

				for (Client client : clientsList) {
					client.send(newClient.username + " has joined");
				}

				if(clientsList.size() > 1){
					for (Client sender : clientsList) {
						for (Client recipient : clientsList) {
							if(sender.username != recipient.username){
								recipient.send("Message from " + sender.username + " : " + sender.message);
							}
						}
					}

					break;
				}
			}
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
		finally
		{
			for(Client client : clientsList){
				client.send("Server: Close connection");
				client.closeConnection();
				client = null;
			}

			System.out.println("Server: Connection is terminated.");
		}
	}
}