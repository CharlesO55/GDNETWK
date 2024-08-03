import java.net.Socket;


import java.io.*;

public class ChatClient
{
	public static void main(String[] args)
	{
		if(args.length < 4){
			System.out.println("ERROR: Needs 4 args");
			System.exit(1);;
		}
		String hostname = args[0];
		int nPort = Integer.parseInt(args[1]);
		String username = args[2];
		String message = args[3];


		try
		{
			Socket clientEndpoint = new Socket(hostname, nPort);
			
			System.out.println(username + ": Connected to server at" + clientEndpoint.getRemoteSocketAddress());
			
			DataOutputStream dosWriter = new DataOutputStream(clientEndpoint.getOutputStream());
			dosWriter.writeUTF(username);
			dosWriter.writeUTF(message);


			DataInputStream disReader = new DataInputStream(clientEndpoint.getInputStream());

			while(!clientEndpoint.isClosed()){
				if(disReader.available() > 0){
					String serverMsg = disReader.readUTF();
					System.out.println(serverMsg);
					
					if(serverMsg.equals("Server: Close connection"))
						break;			
				}
			}
			
			clientEndpoint.close();
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
		finally
		{
			System.out.println(username + ": Connection is terminated.");
		}
	}
}