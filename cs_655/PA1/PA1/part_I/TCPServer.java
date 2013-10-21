/*
Shan Sikdar
PA1: part I
Class: TCPServer

The server should 
After being started, the server should repeatedly accept an input message from a client
and send back the same message.

*/

import java.io.*;
import java.net.*;





class TCPServer {

    public static void main(String args[]) throws Exception {
	
		TCPServer server = new TCPServer();
		
  		int port;
		String incoming_message;
		String outgoing_message = "meow";

		port = 8000;	
		if(args.length > 0){
			try{
				port = Integer.parseInt(args[0]);	
			}
			catch(NumberFormatException e){
				System.out.println("The port number could not be parsed to an int");
				System.out.println("Choosing default port (" + port + ") instead");
			}
		}

		//Check to see if a port number was given as an argument
		//Otherwise default port number will be 8000
		
	  
		ServerSocket welcomeSocket = new ServerSocket(port);

		System.out.println("Server running at port: " + port + ".....");

			while(true) {
				//Wait, on welcoming socket for contact by client
				Socket connectionSocket = welcomeSocket.accept();
				try {
					//Create input sream attached to socket for contact by client
					BufferedReader inFromClient = new BufferedReader(new InputStreamReader(connectionSocket.getInputStream()));
				
					//create output stream, attached to socket
					DataOutputStream outToClient = new DataOutputStream(connectionSocket.getOutputStream());
					
					
					//Read in line from socket
                    while ((incoming_message = inFromClient.readLine()) != null) {
                        //process the message and determine Server Response
                        outgoing_message = incoming_message; 
                        //Write the Response
                        outToClient.writeBytes(outgoing_message + '\n');
                        System.out.println(outgoing_message);
                    }
				} finally {
					connectionSocket.close();
				}	
			}	
	}
}
