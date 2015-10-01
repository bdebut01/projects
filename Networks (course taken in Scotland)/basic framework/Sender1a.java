/* Assignment Part 1a, Sender
 * Matric number: s1477159
 * due February 12th 
 */
import java.io.FileInputStream;
import java.io.InputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;

public class Sender1a {
	public static int PAYLOAD_SIZE = 1021;
	public static byte FLAG_NUM = 0x1;

	public static void main(String args[]) throws Exception {
		String host; // 0
		int port = 0; // 1
		String filename; // 2

		host = args[0];
		try {
			port = Integer.parseInt(args[1]);
		} catch (NumberFormatException nfe) {
			System.out.println("Port must be an integer");
			System.exit(1);
		}
		filename = args[2];

		// Set up input stream to read from file
		InputStream f = new FileInputStream(filename);

		DatagramSocket clientSocket = new DatagramSocket();

		InetAddress IPAddress = InetAddress.getByName(host);

		// Byte arrays
		byte[] sendData = new byte[1024];
		byte[] fileData = new byte[PAYLOAD_SIZE]; // decrement the 3-byte header
		byte[] receiveData = new byte[1024];
		byte[] header = new byte[3];
		header[2] = 0; // Initialise flag to zero

		int num_bytes_read = 0;

		/* Send over extra-bytes info packet */
		int extra_bytes = (f.available() > PAYLOAD_SIZE) ? (f.available() % PAYLOAD_SIZE)
				: f.available();
		for (int i = 0; i < extra_bytes; i++)
			sendData[i] = 0x1; // mark number of extra bytes in array
		DatagramPacket sendPacket2 = new DatagramPacket(sendData,
				sendData.length, IPAddress, port);
		clientSocket.send(sendPacket2);
		DatagramPacket receivePacket2 = new DatagramPacket(receiveData,
				receiveData.length);
		clientSocket.receive(receivePacket2);
		/* * */

		// Main send/receive loop
		while (true) {
			// Final packet?
			if (f.available() < 1021) {
				header[2] = FLAG_NUM;
			}

			num_bytes_read = f.read(fileData);
			if (num_bytes_read == -1)
				break; // Stop loop if no more data to read

			// Copy in the header
			for (int i = 0; i < 3; i++) {
				sendData[i] = header[i];
			}
			// Copy in rest of data from file
			for (int i = 3; i < 1024; i++) {
				sendData[i] = fileData[i - 3];
			}

			DatagramPacket sendPacket = new DatagramPacket(sendData,
					sendData.length, IPAddress, port);
			clientSocket.send(sendPacket);

			// Clear file data array
			for (int i = 0; i < fileData.length; i++) {
				fileData[i] = 0x0;
			}
			DatagramPacket receivePacket = new DatagramPacket(receiveData,
					receiveData.length);
			clientSocket.receive(receivePacket);
		}

		f.close();
		clientSocket.close();
		System.exit(1);
	}
}
