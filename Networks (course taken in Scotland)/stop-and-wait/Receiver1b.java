/* Assignment Part 1b, Receiver
 * Matric number: s1477159
 * due February 12th 
 */
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class Receiver1b {
	public static byte FLAG_NUM = 0x4;
	public static byte INFO_NUM = 0x1;
	public static int PAYLOAD_SIZE = 1021;
	public static byte[] sendData;
	public static byte[] writeData;
	public static byte[] receiveData;
	public static DatagramSocket serverSocket;
	public static int num_extra;
	public static boolean receivingPacket;

	public static void main(String args[]) throws Exception {
		int port = 0; // 0
		String filename; // 1

		try {
			port = Integer.parseInt(args[0]);
		} catch (NumberFormatException nfe) {
			System.out.println("Port must be an integer");
			System.exit(1);
		}
		filename = args[1];

		serverSocket = new DatagramSocket(port);
		OutputStream g = new FileOutputStream(filename);

		sendData = new byte[1024];
		writeData = new byte[PAYLOAD_SIZE];
		receiveData = new byte[1024];
		receivingPacket = false;

		byte flag = 0x0;

		// Start main loop
		byte expected_seq = 0x0;
		while (true) {
			if (!receivingPacket) {
				/* info packet receive and send */
				receiveInfoPacket();
			}

			byte bad_seq = (byte) ((expected_seq == 0x1) ? 0x0 : 0x1); // opposite
																		// expected
																		// seq

			DatagramPacket receivePacket = new DatagramPacket(receiveData,
					receiveData.length);
			serverSocket.receive(receivePacket);
			InetAddress IPAddress = receivePacket.getAddress();
			int port_respond = receivePacket.getPort();

			// Check for duplicates
			byte seq_received = (byte) receiveData[0];
			byte flag_received = (byte) receiveData[2];
			if (seq_received == expected_seq) {
				// It's good, send ack back
				sendData[0] = expected_seq; // GOOD -- ack is same as expected
											// seq number

				// Copy over data
				for (int i = 3; i < 1024; i++)
					writeData[i - 3] = receiveData[i];

				// Check for final packet
				flag = flag_received;
				if (flag != FLAG_NUM)
					g.write(writeData);

				else { // final packet
					byte[] finalarr = new byte[num_extra];
					for (int i = 0; i < num_extra; i++)
						finalarr[i] = writeData[i];
					g.write(finalarr);
					// **** FINAL PACKET SO CLIENT DONE, NO LONGER RECEIVE
					// ****//
					receivingPacket = false;
				}

				flag = 0x0; // reset flag
				for (int i = 0; i < writeData.length; i++)
					writeData[i] = 0x0; // Clear writeData array
				// Next sequence number
				expected_seq = (byte) ((expected_seq == (byte) 0) ? 1 : 0);
			} else { // Duplicate sequence number
				sendData[0] = bad_seq; // (BAD)
				// Note: do not increment to next sequence number
			}
			// Send packet back
			DatagramPacket sendPacket = new DatagramPacket(sendData,
					sendData.length, IPAddress, port_respond);
			serverSocket.send(sendPacket);
		}
	}

	/*
	 * Function to receive first info packet from sender which includes the
	 * number of extra bytes that will exist in the final packet. This is keep
	 * the Receiver from writing additional empty bytes on the final packet.
	 */
	public static void receiveInfoPacket() {
		DatagramPacket receivePacket2 = new DatagramPacket(receiveData,
				receiveData.length);

		try {
			serverSocket.receive(receivePacket2);
		} catch (IOException e) {
			e.printStackTrace();
		}

		byte received_seq2 = (byte) receiveData[0];
		byte bad_seq = 0x0;
		byte send_back = (received_seq2 == INFO_NUM) ? received_seq2 : bad_seq;

		num_extra = 1;
		for (int i = 1; (byte) receiveData[i] == 0x1; i++)
			num_extra++; // Gets overwritten right away below

		InetAddress IPAddress2 = receivePacket2.getAddress();
		int port_respond2 = receivePacket2.getPort();
		sendData[0] = send_back;
		DatagramPacket sendPacket2 = new DatagramPacket(sendData,
				sendData.length, IPAddress2, port_respond2);

		try {
			serverSocket.send(sendPacket2);
		} catch (IOException e) {
			e.printStackTrace();
		}

		if (send_back == bad_seq)
			receiveInfoPacket(); // If a negative packet sent back, loop and
									// wait for correct packet
		else {
			for (int i = 0; i < sendData.length; i++) { // Reset arrays used
				sendData[i] = 0x0;
				receiveData[i] = 0x0;
			}
			receivingPacket = true; // Info packet has been received, set to
									// true so Receiver knows it is in the
									// process of receiving a packet.
			return;
		}
	}
}
