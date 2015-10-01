/* Assignment Part 1b, Sender
 * Matric number: s1477159
 * due February 12th 
 */
import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.util.Timer;
import java.util.TimerTask;

public class Sender1b {
	public static int PAYLOAD_SIZE = 1021;
	public static int port;
	public static byte FLAG_NUM = 0x4;
	public static byte INFO_NUM = 0x1;
	public static Timer t;
	public static byte[] sendData;
	public static byte[] fileData;
	public static byte[] receiveData;
	public static DatagramSocket clientSocket;
	public static InetAddress IPAddress;

	public static int num_retransmissions = 0;

	public static void main(String args[]) throws Exception {
		String host; // 0
		port = 0; // 1
		String filename; // 2
		int timeout = 0; // 3

		host = args[0];
		try {
			port = Integer.parseInt(args[1]);
		} catch (NumberFormatException nfe) {
			System.out.println("Port must be an integer");
			System.exit(1);
		}
		filename = args[2];
		try {
			timeout = Integer.parseInt(args[3]);
		} catch (NumberFormatException nfe) {
			System.out.println("RetryTimeout must be an integer");
			System.exit(1);
		}

		// Set up input stream to read from file
		InputStream f = new FileInputStream(filename);

		clientSocket = new DatagramSocket();

		IPAddress = InetAddress.getByName(host);

		/*************** TESTING VARIABLES ************/
		int file_size_bytes = f.available();
		long program_start_time;
		long program_end_time;

		// Byte arrays
		sendData = new byte[1024];
		fileData = new byte[PAYLOAD_SIZE]; // decrement the 3-byte header
		receiveData = new byte[1024];
		byte[] header = new byte[3];

		int num_bytes_read = 0;

		/* Send over extra bytes info packet */
		byte seq_num2 = INFO_NUM;

		int extra_bytes = (f.available() > PAYLOAD_SIZE) ? (f.available() % PAYLOAD_SIZE)
				: f.available();
		for (int i = 1; i < extra_bytes; i++)
			sendData[i] = 0x1;
		sendData[0] = seq_num2;
		program_start_time = System.currentTimeMillis(); // Communication
															// officially begins
		send_and_receive(timeout, seq_num2);
		t.cancel();
		for (int i = 0; i < sendData.length; i++) { // reset
			sendData[i] = 0x0;
			receiveData[i] = 0x0;
		}
		/* * */

		// Main send/receive loop
		byte seq_num = 0x1; // first round of while loop flips this to 0x0 for
							// first packet
		while (true) {
			seq_num = (byte) ((seq_num == 0x1) ? 0x0 : 0x1); // flip back and
																// forth 0x0 vs
																// 0x1
			header[0] = seq_num;

			// Final packet?
			if (f.available() < PAYLOAD_SIZE) {
				header[2] = FLAG_NUM;
				System.out.println("EOF flag attached");
			}

			num_bytes_read = f.read(fileData);

			// Copy in the header
			for (int i = 0; i < 3; i++) {
				sendData[i] = header[i];
				if (header[2] == FLAG_NUM)
					num_bytes_read = -1; // ugly, but ending this loop (eof)
			}
			// Copy in rest of data from file
			for (int i = 3; i < 1024; i++) {
				sendData[i] = fileData[i - 3];
			}

			// Send and receive loop with timeout
			send_and_receive(timeout, seq_num);

			// Clear file data array
			for (int i = 0; i < fileData.length; i++) {
				fileData[i] = 0x0;
			}
			if (num_bytes_read == -1)
				break; // sender is done
		}
		program_end_time = System.currentTimeMillis();

		System.out.println("File size bytes: " + file_size_bytes
				+ " Run time: " + (program_end_time - program_start_time));
		System.out.println("Average throughput (KB/s): "
				+ (file_size_bytes / (program_end_time - program_start_time)));
		System.out.println("Number of retransmissions: " + num_retransmissions);
		System.out.println("Timeout: " + timeout);

		System.exit(1);
	}

	public static void send_and_receive(int timeout_, byte seqNum)
			throws IOException {
		int delay = timeout_; // milliseconds
		Timeout sendpacket = new Timeout(); // The run function below that
											// repeatedly happens
		t = new Timer(); // Instantiate a new timer
		t.schedule(sendpacket, 0, delay); // Will send a packet every delay
											// milliseconds

		DatagramPacket receivePacket = new DatagramPacket(receiveData,
				receiveData.length);
		clientSocket.receive(receivePacket);
		t.cancel(); // A packet has been received, stop timer, check for ACK

		byte ACK = seqNum; // ACK is the sequence number
		byte response = (byte) receiveData[0];
		if (response == ACK) {
			return;
		} else { // else not an ACK that was received
			num_retransmissions++;
			send_and_receive(timeout_, seqNum); // recursively loop
		}
	}

	public static class Timeout extends TimerTask {
		public void run() { /* Called as "sendpacket" */
			// Send packets
			DatagramPacket sendPacket = new DatagramPacket(sendData,
					sendData.length, IPAddress, port);

			try {
				clientSocket.send(sendPacket);
			} catch (IOException e) {
				e.printStackTrace();
			}
		}
	}
}
