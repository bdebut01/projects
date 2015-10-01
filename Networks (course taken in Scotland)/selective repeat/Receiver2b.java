import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.ArrayList;

public class Receiver2b {

	public static byte FLAG_NUM = 0x4;
	public static int PAYLOAD_SIZE = 1021;
	public static DatagramSocket serverSocket;
	public static OutputStream g;
	public static boolean receivingPacket;
	public static byte[] receivedSeq;

	public static ArrayList<Packet> allPackets;
	public static ArrayList<Short>	rcv_seqs;
	public static short 			base;
	public static short 			last_seq = -1;
	public static int 				num_bytes_last = 6;
	public static boolean			alreadyWrote = false;

	public static void main(String args[]) throws Exception {
		int port = 0; // 0
		String filename; // 1
		int windowsize = 1; //2

		try {
			port = Integer.parseInt(args[0]);
		} catch (NumberFormatException nfe) {
			System.out.println("Port must be an integer");
			System.exit(1);
		}
		filename = args[1];
		try {
			windowsize = Integer.parseInt(args[2]);
		} catch (NumberFormatException nfe) {
			System.out.println("Window size must be an integer greater than 0");
			System.exit(1);
		}
		windowsize = (windowsize == 0) ? 1 : windowsize; //don't allow that windowsize of zero

		serverSocket = new DatagramSocket(port);
		g = new FileOutputStream(filename);

		byte[] sendData 	= new byte[1024];
		byte[] receiveData = new byte[1024];
		receivedSeq = new byte[2];
		allPackets 	= new ArrayList<Packet>();
		rcv_seqs 	= new ArrayList<Short>();

		// Start main loop
		//short expected_seq = 1;
		base = 1;
		while (true) {
			DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
			serverSocket.receive(receivePacket);
			InetAddress IPAddress = receivePacket.getAddress();
			int port_respond = receivePacket.getPort();

			receivedSeq[0] = receiveData[0]; receivedSeq[1] = receiveData[1];
			byte flag_received = receiveData[2];
			short rcved_seqnum = bytesToShort(receivedSeq);
			
			if(isValid(rcved_seqnum, windowsize)) {
				byte[] fileData;
				//Send back the sequence number received
				sendData[0] = receivedSeq[0]; sendData[1] = receivedSeq[1];
				//Add seq to list of seqs seen
				rcv_seqs.add(rcved_seqnum);

				//Increment base?
				if(base == rcved_seqnum) {
					base = nextUnreceivedPkt();
				}
				//Info packet?
				if(flag_received == FLAG_NUM) {
					last_seq = (short)(rcved_seqnum + 1);
					for (int i = 3; (byte) receiveData[i] == 0x1; i++) num_bytes_last++;
				}
				//Last packet?
				if(rcved_seqnum == last_seq) {
					fileData = new byte[num_bytes_last - 3];
					for (int i = 3; i < num_bytes_last; i++) fileData[i-3] = receiveData[i];
				} else {
					fileData = new byte[PAYLOAD_SIZE];
					for (int i = 3; i < 1024; i++) fileData[i - 3] = receiveData[i];
				}
				//Be sure not to write the info packet later!
				allPackets.add(new Packet(rcved_seqnum, fileData));
				System.out.println("Received packet #: " + rcved_seqnum);
				// Send packet back
				DatagramPacket sendPacket = new DatagramPacket(sendData,
						sendData.length, IPAddress, port_respond);
				serverSocket.send(sendPacket);
			}
			//else nothing
			if(isFinished() && !alreadyWrote) {
				System.out.println("Gonna write to file around now");
				writeToFile();
			}
		}
	}

	// Basically returns where the new base should be
	public static short nextUnreceivedPkt() {
		short result = base;
		for(; rcv_seqs.contains(result); result++);
		return result;
	}
	public static boolean isFinished() {
		if(last_seq == -1) return false;
		for(short i = 1; i <= last_seq; i++) {
			if(!rcv_seqs.contains(i)) return false;
		}
		return true;
	}

	public static void writeToFile() {
		for(short seq = 1; seq <= last_seq; seq++) {
			for(int j = 0; j < allPackets.size(); j++) {
				if(seq == allPackets.get(j).my_seq) {
					if(seq == (short)(last_seq-1)) continue;
					//^if that fails throw && in orig. if statement
					Packet found = allPackets.get(j);
					try { g.write(found.my_arr);
					} catch (IOException e) { e.printStackTrace(); }
					//allPackets.remove(found)?? might mess with index #s?
				}
			}
		}
		alreadyWrote = true;
	}

	public static boolean isValid(short seq, int windowsize_) {
		return (seq >= base && seq < base + windowsize_);
	}

	public static short bytesToShort(byte[] bytes) {
	     return ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN).getShort();
	}
		
	public static byte[] shortToBytes(short value) {
	    return ByteBuffer.allocate(2).order(ByteOrder.LITTLE_ENDIAN).putShort(value).array();
	}

	public static class Packet {
		public byte[] 	my_arr;
		public short 	my_seq;

		public Packet(short sequence_number, byte[] fileData_) {
			this.my_arr = new byte[fileData_.length];
			this.my_seq = sequence_number;

			for(int i = 0; i < fileData_.length; i++)
				this.my_arr[i] = fileData_[i];
		}
	}
}
