import java.io.*;
import java.net.*;
import java.util.Date;

class TCPServer {

	public boolean connection_phase_set;
	public String measurement_type;	
	public int number_of_probes_expected; 
	public int message_size;
	public int server_delay = 0;
	public int expected_probe_seq_num = 1;

	
	/*
		Method for Server Delay
	*/
	public static void delayServer(int seconds){
		Date start = new Date();
		Date end = new Date();
		while(end.getTime() - start.getTime() < seconds * 1000){
			end = new Date();
		}
	}

	public int  getServerDelay(){
		return server_delay;
	}
	
	
	/*
		Method for processing the msg request sent to the server
	*/
	public String processMsg(String request){
		String msg;
		String[] tokens =request.split("\\s");
		
			/*
				Check Protocol Phase:
				"s" = connection phase setup  <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>
				"m" = measurement phase <PROTOCOL PHASE><WS><PROBE SEQUENCE NUMBER><WS><PAYLOAD>
				"t" = connection termination phase <PROTOCOL PHASE><WS>
				else 404

			*/			
		String protocol_phase = tokens[0];
		if(protocol_phase.compareTo("s") == 0){
			msg = "404 ERROR: Invalid Connection Setup";
			if(tokens.length != 5){
				//then one of the measurment parameters is missing or just invalid format
				return msg;
			}else{
				//check the measurement type. If it is not rtt or tput, send back an error message
				measurement_type = tokens[1];
				try{
					number_of_probes_expected = Integer.parseInt(tokens[2]);
					message_size = Integer.parseInt(tokens[3]);
					server_delay = Integer.parseInt(tokens[4]);
				}catch(NumberFormatException e){
					//These fields needed to be numbers. Bad Format. Send back 404.
					return msg;
				}
				expected_probe_seq_num = 1;
				return "200 OK: Ready"; 
			}
		}else if(protocol_phase.compareTo("m") == 0){
			msg = "404 ERROR: Invalid Measurement Message";
			int prob_number;
						
			if(tokens.length != 3){
				// or should it be three
				return msg;
			}else if(tokens[2].getBytes().length != message_size){
				//checking the error size
				return msg;
			}else{
				try{
					//make sure the protocol number is actually an int
					prob_number = Integer.parseInt(tokens[1]);
				}catch(NumberFormatException e){
					//These fields needed to be numbers. Bad Format. Send back 404.
					return msg;
				}
				//keep track of the probe sequence numbers to make sure they are indeed being incremented by 1 each time and do not exceed the number of probes specified in the connection setup phase.
				if(prob_number == expected_probe_seq_num){
					//Increment the expected_probe_seq_num by 1 as long as it is <= to number_of_probes_expected
					if(expected_probe_seq_num <=number_of_probes_expected){
						expected_probe_seq_num++;
					}
					return request; /*The server should echo back every probe message received*/
				}else{
					return tokens[2];
				}
			}
			/*The server should echo back every probe message received*/
		
		}else if(protocol_phase.compareTo("t") == 0){
			//Connection Termination Message
			msg = "404 ERROR: Invalid Connection Termination Message";
			if(tokens.length == 1){
				msg = "200 OK: Closing Connection";
			}
			return msg;
		}else{
			return "404 ERROR: Invalid Connection Setup Message";
		}
	}			
	
	/*
		Main Function
	
	*/
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
		try {
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
                        outgoing_message = server.processMsg(incoming_message); 
						
						//if the server delay is not 0 delay the response by the server delay
						if(server.getServerDelay() != 0){
							delayServer(server.getServerDelay());
						}
                        //Write the Response
                        outToClient.writeBytes(outgoing_message + '\n');
                        System.out.println(outgoing_message);
						//If Response Contatins 404, or Termination message, get out of this while loop and close the connection
						if(outgoing_message.contains("404") || outgoing_message == "200 OK: Closing Connection"){
							break;
						}
                    }
				} finally {
					connectionSocket.close();
				}	
			}	
		} finally {
				welcomeSocket.close();
		}	
		
	}
}
