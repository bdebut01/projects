/* Assignment Part 1a, Receiver
 * Matric number: s1477159
 * due February 12
 *
 */

import java.io.FileOutputStream;
import java.io.OutputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class Receiver1a {
	public static byte FLAG_NUM = 0x1;
	public static int PAYLOAD_SIZE = 1021;

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

		DatagramSocket serverSocket = new DatagramSocket(port);
		OutputStream g = new FileOutputStream(filename);

		byte[] sendData = new byte[1024];
		byte[] writeData = new byte[PAYLOAD_SIZE];
		byte[] receiveData = new byte[1024];

		byte flag = 0x0;

		/* Receive extra-bytes info packet */
		DatagramPacket receivePacket2 = new DatagramPacket(receiveData,
				receiveData.length);
		serverSocket.receive(receivePacket2);
		InetAddress IPAddress2 = receivePacket2.getAddress();
		int port_respond2 = receivePacket2.getPort();
		DatagramPacket sendPacket2 = new DatagramPacket(sendData,
				sendData.length, IPAddress2, port_respond2);
		serverSocket.send(sendPacket2);

		int num_extra = 0;
		for (int i = 0; receiveData[i] == 0x1; i++)
			num_extra++; // count up extra-byte markers
		/* * */

		// Start main loop
		while (true) {
			DatagramPacket receivePacket = new DatagramPacket(receiveData,
					receiveData.length); // overwrites previous sendData array
			serverSocket.receive(receivePacket);
			InetAddress IPAddress = receivePacket.getAddress();
			int port_respond = receivePacket.getPort();

			flag = receiveData[2]; // Read EOF flag
			for (int i = 3; i < 1024; i++) {
				writeData[i - 3] = receiveData[i];
			}

			if (flag != FLAG_NUM) {
				g.write(writeData);
			} else { // final packet
				byte[] finalarr = new byte[num_extra]; // Only write num_extra
														// bytes worth of bytes
				for (int i = 0; i < num_extra; i++)
					finalarr[i] = writeData[i];
				g.write(finalarr);
			}

			flag = 0x0; // reset flag
			for (int i = 0; i < writeData.length; i++) { // Clear writeData
															// array
				writeData[i] = 0x0;
			}

			DatagramPacket sendPacket = new DatagramPacket(sendData,
					sendData.length, IPAddress, port_respond);
			serverSocket.send(sendPacket);
		}
	}
}
