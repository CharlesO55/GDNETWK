import java.net.*;
import java.nio.file.Path;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.io.*;

public class CSNETWKServer
{
	public static void main(String[] args)
	{
		CSNETWKServer server = new CSNETWKServer();

		int nPort = args.length == 1 ? Integer.parseInt(args[0]) : 8801;


		

		server.StartSever(nPort);
	}

	private void StartSever(int nPort){
		System.out.println("Server: Listening on port " + nPort + "...");
		ServerSocket serverSocket;
		Socket serverEndpoint;

		try 
		{
			serverSocket = new ServerSocket(nPort);
			serverEndpoint = serverSocket.accept();
			
			System.out.println("Server: New client connected: " + serverEndpoint.getRemoteSocketAddress());
			
			DataInputStream disReader = new DataInputStream(serverEndpoint.getInputStream());
			System.out.println(disReader.readUTF());
			
			DataOutputStream dosWriter = new DataOutputStream(serverEndpoint.getOutputStream());
			// dosWriter.writeUTF("Server: Hello World!");

			// Path filePath = Paths.get("C:\\Users\\cmath\\OneDrive\\Desktop\\GDNETWK\\Lab3\\Download.txt");
			Path filePath = Paths.get("Download.txt");
			dosWriter.write(Files.readAllBytes(filePath));

			serverEndpoint.close();
		}
		catch (Exception e)
		{
			e.printStackTrace();
		}
		finally
		{
			System.out.println("Server: Connection is terminated.");
		}
	}
}