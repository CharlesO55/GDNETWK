import java.net.*;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.io.*;

public class CSNETWKClient
{


	public static void main(String[] args)
	{
		String sServerAddress = "localhost";
		int nPort = 8801;
		if(args.length == 2){
			sServerAddress = args[0];
			nPort = Integer.parseInt(args[1]);
		}
		
		CSNETWKClient client = new CSNETWKClient();
		client.ConnectToServer(sServerAddress, nPort);		
	}

	private void ConnectToServer(String sServerAddress, int nPort){
		try
		{
			Socket clientEndpoint = new Socket(sServerAddress, nPort);
			
			System.out.println("Client: Connected to server at" + clientEndpoint.getRemoteSocketAddress());
			
			DataOutputStream dosWriter = new DataOutputStream(clientEndpoint.getOutputStream());
			dosWriter.writeUTF("Client: Hello from client" + clientEndpoint.getLocalSocketAddress());
			
			DataInputStream disReader = new DataInputStream(clientEndpoint.getInputStream());
			// System.out.println(disReader.readUTF());
			// Path filePath = Paths.get("Check.txt");
			// Files.createFile(filePath, null)

			Path filePath = Paths.get("Received.txt");
			Files.write(filePath, disReader.readAllBytes());

			clientEndpoint.close();
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
		finally
		{
			System.out.println("Client: Connection is terminated.");
		}
	} 
}