import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;


public class Receiver2a {

	public static byte FLAG_NUM = 0x4;
	public static short INFO_NUM = -1;
	public static int PAYLOAD_SIZE = 1021;
	public static byte[] sendData;
	public static byte[] writeData;
	public static byte[] receiveData;
	public static DatagramSocket serverSocket;
	public static int num_extra = 3; //Yeah three appears to be the magic #
	public static short lastSeq = 0;
	public static boolean receivingPacket;
	public static byte[] receivedSeq;

	public static void main(String args[]) throws Exception {
		int port = 0; // 0
		String filename; // 1
		//int windowsize;

		try {
			port = Integer.parseInt(args[0]);
		} catch (NumberFormatException nfe) {
			System.out.println("Port must be an integer");
			System.exit(1);
		}
		filename = args[1];
		/*try {
			windowsize = Integer.parseInt(args[2]);
		} catch (NumberFormatException nfe) {
			System.out.println("Window size must be an integer greater than 0");
			System.exit(1);
		}*/

		serverSocket = new DatagramSocket(port);
		OutputStream g = new FileOutputStream(filename);

		sendData = new byte[1024];
		writeData = new byte[PAYLOAD_SIZE];
		receiveData = new byte[1024];
		receivedSeq = new byte[2];

		// Start main loop
		short expected_seq = 1;
		while (true) {
			if(expected_seq % 50 == 0) System.out.print(".");

			DatagramPacket receivePacket = new DatagramPacket(receiveData,
					receiveData.length);
			serverSocket.receive(receivePacket);
			InetAddress IPAddress = receivePacket.getAddress();
			int port_respond = receivePacket.getPort();

			receivedSeq[0] = receiveData[0];
			receivedSeq[1] = receiveData[1];
			byte flag_received = receiveData[2];
			
			short sequenceNum_received = bytesToShort(receivedSeq);
			
			
			if (sequenceNum_received == expected_seq) {

				sendData[0] = receivedSeq[0]; // GOOD -- ack is same as expected
				sendData[1] = receivedSeq[1];// seq number

				// Copy over data
				for (int i = 3; i < 1024; i++) writeData[i - 3] = receiveData[i];

				// Not info packet nor final packet of sequence
				if (flag_received != FLAG_NUM && expected_seq != lastSeq) 
					g.write(writeData);
				
				// Check for final packet
				else if(expected_seq == lastSeq) {
					byte[] finalarr = new byte[num_extra];
					for (int i = 0; i < num_extra; i++) finalarr[i] = writeData[i];
					g.write(finalarr);
				}
				else { // it is the info packet PRECEDING the final packet
					lastSeq = (short)(sequenceNum_received+1);
					for (int i = 3; (byte) receiveData[i] == 0x1; i++)
						num_extra++;
				}
				// Clear writeData array
				for (int i = 0; i < writeData.length; i++)	writeData[i] = 0x0; 
				// Next sequence number
				expected_seq++;
			} else { // Duplicate sequence number
				short replyACK = (short)(expected_seq-1);
				byte[] temp = new byte[2];
				temp = shortToBytes(replyACK);
				sendData[0] = temp[0]; // (send back expected sequence number
				sendData[1] = temp[1];// Note: do not increment to next sequence number

			}
			// Send packet back
			DatagramPacket sendPacket = new DatagramPacket(sendData,
					sendData.length, IPAddress, port_respond);
			serverSocket.send(sendPacket);

		}
	}

	public static short bytesToShort(byte[] bytes) {
	     return ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN).getShort();
	}
		
	public static byte[] shortToBytes(short value) {
	    return ByteBuffer.allocate(2).order(ByteOrder.LITTLE_ENDIAN).putShort(value).array();
	}

}
