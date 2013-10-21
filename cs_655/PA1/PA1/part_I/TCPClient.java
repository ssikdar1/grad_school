/*
Shan Sikdar
PA: Part I
TCPClient

The client should accept, as command line arguments, a host name (or IP address), as
well as a port number for the server. Using this information, it creates a connection (using
TCP) with the server, which should be running already. The client
program then sends a message (text string) to the server using the connection. When it receives back the
message, it prints it and exits.

*/
import java.io.*;
import java.net.*;

class TCPClient{

  public static void main(String args[]) throws Exception {
		String hostname;
		int port;
		String msg;
		String return_msg;
		
		if(args.length != 2){
			System.out.println("Need 2 arguments hostname/IP Address and port number");
		}else{
			hostname = args[0];
			port = Integer.parseInt(args[1]);

			// BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));

			Socket clientSocket = new Socket(hostname, port);

			//Create Output Stream Attached to Socket
			DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
			
			//Create Input Stream Attached to Socket
			BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

			msg = "Here is a test message that goes to the server and back!";
			
			//Send to Server
			outToServer.writeBytes(msg + '\n');
			
			//Get Line From Server
			return_msg = inFromServer.readLine();
			
			System.out.println(return_msg);
			
			//and again....
			
			msg = "The server is accepting continuous client requests!";
			outToServer.writeBytes(msg + '\n');
			return_msg = inFromServer.readLine();
			System.out.println(return_msg);

			clientSocket.close();
		}
	}
}