import java.io.*;
import java.net.*;
import java.util.Arrays;


class TCPClient {

	/*
		Create Msg to setup a connection with the server
	 Connection Setup Phase (CSP)
		FORMAT: <PROTOCOL PHASE><WS><MEASUREMENT TYPE><WS><NUMBER OF PROBES><WS><MESSAGE SIZE><WS><SERVER DELAY>
	*/
	public static String createCSPmessage(String measurement,int msgSize,int numProbes,int delay){
		String msg;
		String protocol_phase = "s";
		String ws = " "; 				//whitespace
		String measurment_type = measurement;
		int number_of_probes = numProbes; // ???
		int message_size= msgSize;
		int server_delay = delay; 
		msg = protocol_phase + ws + measurment_type + ws+ number_of_probes + ws + message_size + ws + server_delay; 
		return msg;
	}
	
	/*
	
	Method to create the Measurement phase message
	@param probe number, byte size
	
	Measurement Phase (MP)
	FORMAT :<PROTOCOL PHASE><WS><PROBE SEQUENCE NUMBER><WS><PAYLOAD>
	
	PROBE SEQUENCE NUMBER: The probe messages should have increasing sequence numbers starting from 1 up to the number of probes
	specified in the connection setup message using the NUMBER OF PROBES variable.

	*/
	public static String createMPmessage(int prob_number,int bytes){

		String protocol_phase = "m";
		int probe_seq_number = prob_number;
		String payload = createStringPacket(bytes);
		String ws = " ";
		String msg = protocol_phase + ws + probe_seq_number + ws + payload; 
		return msg;			
	}

	/*
		Method to create a string of a certain bytes
		@param byte size 
	*/
	public static String createStringPacket(int bytes){
		//create the array of bytes to the size that the string needs to be
		byte[] s = new byte[bytes];
		Arrays.fill(s, (byte) 'a');
		String payload = new String(s);
		return payload;
	}
	
	/* 
	Method to create termination request
	FORMAT :<PROTOCOL PHASE><WS> 
	When terminating the connection will be denoted by the lower case character 't'.

	*/
	 
	 public static String createCTPmessage(){

		String protocol_phase = "t";
		String ws = " ";
		String msg = protocol_phase + ws;
		return msg;
	 }

	/*
		Main Function
	
	*/

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
			
			

			Socket clientSocket = new Socket(hostname, port);

			DataOutputStream outToServer = new DataOutputStream(clientSocket.getOutputStream());
			BufferedReader inFromServer = new BufferedReader(new InputStreamReader(clientSocket.getInputStream()));

			String measurement;
			int bytes = 0;
			int probes = 0;
			int delay = 0;

			//Get User Input for the measurement
			// meaurement size probes delay
			//example: rtt 1024 10 0
			System.out.println("Enter the type of measurement(rtt or tput), msg size in bytes, and # of probes, and delay seperated by a space: ");
				
			BufferedReader inFromUser = new BufferedReader(new InputStreamReader(System.in));
			
			String parameters = inFromUser.readLine();
			String[] tokens = parameters.split("\\s");
			
			if(tokens[0].equals("rtt") || tokens[0].equals("tput")){
			
				measurement = tokens[0];
				
				try{
					bytes = Integer.parseInt(tokens[1]);
					probes = Integer.parseInt(tokens[2]);
					delay = Integer.parseInt(tokens[3]);
				}catch(Exception e){
					System.out.println("Please enter a Integer for the byte size for the second paramter");
					System.out.println("Please enter a number of probes for the third paramter");
					System.out.println("Please enter a delay for the fourth paramter");
				}
				
				//Send Connection Setup Phase message
				msg = createCSPmessage(measurement,bytes,probes,delay);
				outToServer.writeBytes(msg + '\n');
				return_msg = inFromServer.readLine();
				System.out.println(return_msg);
				
				//The Server sends back a 200 OK response then we can start sending the data
				if(return_msg.contains("200") && return_msg.contains("OK")){
					System.out.println("Sending probe messages:");
					//Start doing the calculations
					//Do a calculation for each probe 
					
						if(measurement.equals("rtt")){
							String string ="\t# probes\t Time Msg Sent(nano secs) \t Time Msg Recieved(nano secs) \t RTT (nano secs)" ;			
							System.out.println(string);
						}
				
						if(measurement.equals("tput")){
							String string ="\t# probes\t Time Msg Sent(nano secs)\t Time Msg Recieved(nano secs)\t TPUT (bits/mili seconds)" ;			
							System.out.println(string);
						}
						long runningTotalRTT = 0; 	//Use this to keep a running total of the RTT. Use for avg
						long runningTotalTPUT = 0;	// Same thing for throughput
						
						for(int i=1; i <= probes; i++){
						
							//create the message to send
							msg = createMPmessage(i,bytes);
							
							//Time Stamp the time Message Sent 
							long msgSent = System.nanoTime();
							//And then send the message
							outToServer.writeBytes(msg + '\n');
							//Get the incomming message
							return_msg = inFromServer.readLine();	
							return_msg = return_msg.trim();
							//Time Stamp when the return Message was recieved
							long msgRecieved = System.nanoTime();
							
							//The Round Trip time is MsgRecieved - Msg Sent
							long roundTripTime = msgRecieved - msgSent;
							float time = (float)(roundTripTime/(1000000)); //Into mili seconds 
							
							//Calculations to get the throughput as a float
							runningTotalRTT += roundTripTime;
							float size = (float)bytes; 
							float throughput = size/time;
							
							//System.out.println(throughput);

							runningTotalTPUT += throughput;

							
							if(measurement.equals("rtt")){
								System.out.println("\t   "+i + "\t\t\t        " +  msgSent + "\t  " + msgRecieved + "\t\t  " + roundTripTime );
							}
							if(measurement.equals("tput")){
								System.out.println("\t   "+i + "\t        " +  msgSent + "\t\t  " + msgRecieved + "\t\t\t  " + throughput );
							}
						}

							if(measurement.equals("rtt")){
								System.out.println(" Average RTT: " + (runningTotalRTT/probes) + " nano seconds");
							}
							if(measurement.equals("tput")){
								System.out.println(" Average TPUT: " + (runningTotalTPUT/probes) + " bits/mili seconds");
							}
						//After the stats have been printed send a message to terminate the connection
						//CTP: Connection Termination Phase
						msg = createCTPmessage();
						outToServer.writeBytes(msg + '\n');
						return_msg = inFromServer.readLine();
					}				
			}else{
				System.out.println("Please enter rtt or tput as the first parameter");
			}
			clientSocket.close();
		}
	}
}
