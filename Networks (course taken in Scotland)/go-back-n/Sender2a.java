import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.net.DatagramPacket;
import java.net.DatagramSocket;
import java.net.InetAddress;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.ArrayList;
import java.util.Timer;
import java.util.TimerTask;


public class Sender2a {
	public static int PAYLOAD_SIZE = 1021;
	public static int port;
	public static int windowsize;
	public static byte FLAG_NUM = 0x4; //flag indicates the info packet now
	public static short base = 0;
	public static short nextseqnum = 0;
	public static boolean isEnd = false;
	public static short seqOfLastPacket = -1;
	public static boolean endOfSender = false;
	public static Timer t2;
	public static byte[] sendData;
	public static ArrayList<Packet> windowData;
	public static byte[] fileData;
	public static byte[] receiveData;
	public static DatagramSocket clientSocket;
	public static InputStream f;
	public static InetAddress IPAddress;

	public static void main(String args[]) throws Exception {
		String host; // 0
		port = 0; // 1
		String filename; // 2
		int timeout = 0; // 3
		windowsize = 0; //4

		/* 				COMMAND LINE VARIABLES				  */
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
		try {
			windowsize = Integer.parseInt(args[4]);
		} catch (NumberFormatException nfe) {
			System.out.println("Window size must be an integer");
			System.exit(1);
		}
		windowsize = (windowsize == 0) ? 1 : windowsize; //don't allow that windowsize of zero
		
		/*						***							*/

		// Set up input stream to read from file
		f = new FileInputStream(filename);

		clientSocket = new DatagramSocket();

		IPAddress = InetAddress.getByName(host);

		/*************** TESTING VARIABLES ************/
		int file_size_bytes = f.available();
		long program_start_time = 0;
		long program_end_time = 0;

		// Byte arrays
		sendData = new byte[1024];
		fileData = new byte[PAYLOAD_SIZE];
		receiveData = new byte[1024];
		windowData = new ArrayList<Packet>();

		// Main send/receive loop
		base = 1; nextseqnum = 1;
		program_start_time = System.currentTimeMillis();
		while (true) { 
		
			nextseqnum = controlLoop(timeout, nextseqnum);
		
			receivePacket(timeout);	
			
			if(endOfSender) break;
		}
		
		program_end_time = System.currentTimeMillis();
		long num_kilobytes = file_size_bytes / 1000;
		float runtime = (program_end_time - program_start_time) / 1000;
		float throughput = (float)(num_kilobytes / runtime);
		
		System.out.println("File size KB: " + num_kilobytes + " Run time (s): " + runtime);
		System.out.println("Average throughput (KB/s): " + throughput);
		System.out.println("Window size: " + windowsize);
		System.out.println("Timeout: " + timeout);

		System.exit(1);
	}

	public static short controlLoop(int timeout_, short seqNum) {
		short nextseqnum_ = seqNum;

		if(nextseqnum_ < base + windowsize && nextseqnum_ != seqOfLastPacket + 1) {
			
			isEnd = addNextSequencePkt(nextseqnum_); 
			
			sendPacket(nextseqnum_);
			
			if(base == nextseqnum_) {
				Timeout2 sendWindow = new Timeout2();
				t2 = new Timer();
				t2.schedule(sendWindow, 0, timeout_);
			}
			nextseqnum_++;
		} 
		/* else you have sent the whole window, so camp at this nextseq */
		return nextseqnum_;
	}
	
	public static void receivePacket(int timeout_) {
		DatagramPacket receivePacket = new DatagramPacket(receiveData,
				receiveData.length);
		try {
			clientSocket.receive(receivePacket);
		} catch (IOException e) { e.printStackTrace(); }
		
		byte[] header = new byte[2];
		header[0] = receiveData[0]; header[1] = receiveData[1];
		base = (short) (bytesToShort(header) + 1);

		if(base == nextseqnum) {
			t2.cancel();
		}
		else {
			t2.cancel();
			Timeout2 sendWindow = new Timeout2();
			t2 = new Timer();
			t2.schedule(sendWindow, 0, timeout_);
		}
		if((short)(base-1) == seqOfLastPacket) endOfSender = true; //also questionable
	}
	
	public static boolean addNextSequencePkt(short nextseqnum_) {
		Packet recent = new Packet(nextseqnum_);
		if(recent.isLast) {
			/* Sneak in the info packet that describes how many bytes the last packet
			 * 		contains. Also swap their sequence numbers so they are still 
			 * 		in order.
			 */
			Packet pkt_info_flag = new Packet(nextseqnum_, recent.my_extra_bytes);
			recent.setSequenceNumber((short)(nextseqnum_+1)); //set actual packet # to +1 
			windowData.add(pkt_info_flag);
		} 
		windowData.add(recent);
		
		return recent.isLast; 
	}
	
	public static void sendPacket(short seq_number) { 
		//send the latest packet that has not been sent yet
		int index = (int)(seq_number-1);
		DatagramPacket sendPacket = new DatagramPacket(windowData.get(index).my_arr,
									windowData.get(index).my_arr.length, IPAddress, port);
		try {
			clientSocket.send(sendPacket);
		} catch (IOException e) { e.printStackTrace(); }
	}

	/* Executes after the specified delay (TimerTask task, long delay) */
	public static class Timeout2 extends TimerTask {
		public void run() { 
			/* Send every packet in the window, starting from base (or front of ArrayList) */
			for(int i = base; i < nextseqnum; i++) {
				DatagramPacket sendPacket = new DatagramPacket(windowData.get(i-1).my_arr,
						windowData.get(i-1).my_arr.length, IPAddress, port);
				try {
					clientSocket.send(sendPacket);
				} catch (IOException e) {
					e.printStackTrace();
				}
			}
		}
	}

	public static short bytesToShort(byte[] bytes) {
	     return ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN).getShort();
	}
		
	public static byte[] shortToBytes(short value) {
	    return ByteBuffer.allocate(2).order(ByteOrder.LITTLE_ENDIAN).putShort(value).array();
	}
	
	public static class Packet {
		public byte[] my_arr;
		public boolean isLast = false;
		public short  my_seqnum = 0;
		public int my_extra_bytes = 0;
		public boolean hasSent = false;

		//Special constructor for building the packet that describes
		//	the number of extra bytes in the last packet.
		public Packet(short sequence_number, int num_bytes) {
			my_arr = new byte[1024];
			my_seqnum = sequence_number;
			my_extra_bytes = num_bytes;
			byte[] my_header = new byte[3];
			/* Copy over sequence number into header */
			byte[] temp = shortToBytes(sequence_number);
			my_header[0] = temp[0]; my_header[1] = temp[1];

			my_header[2] = FLAG_NUM; //NOTE
			for (int i = 0; i < 3; i++) 			 my_arr[i] = my_header[i];
			for (int i = 3; i < my_extra_bytes; i++) my_arr[i] = 0x1;
		}

		//NOTE: When constructed, automatically reads from input file, 
		//	fills personal array of bytes.
		public Packet(short sequence_number) {
			my_arr = new byte[1024];
			my_seqnum = sequence_number;

			byte[] my_header = new byte[3];
			
			/* Copy over sequence number into header */
			byte[] temp = shortToBytes(sequence_number);
			my_header[0] = temp[0]; my_header[1] = temp[1];
			
			try { /* Last packet work, to let the Receiver only write relevant data */
				if (f.available() < PAYLOAD_SIZE && f.available() > 0) {
					seqOfLastPacket = (short)(my_seqnum+1); //Set sequence number of last packet [going to be incremented later]
					isLast = true;
					my_extra_bytes = f.available();
				} else if(f.available() == 0) { //Calling new packet on empty file, DON'T try to read
					isLast = true;
					return;
				}
			} catch (IOException e1) { e1.printStackTrace();}
			
			try {
				f.read(fileData);
			} catch (IOException e) { e.printStackTrace();}
			
			// Copy in the header
			for (int i = 0; i < 3; i++)  			   my_arr[i] = my_header[i];
			// Copy in rest of data from file
			for (int i = 3; i < 1024; i++) 			   my_arr[i] = fileData[i - 3];
			// Reset fileData rray
			for (int i = 0; i < fileData.length; i++)  fileData[i] = 0x0;
			
		}
		public void setSequenceNumber(short sequence_number) {
			my_seqnum = sequence_number;
			byte[] temp = shortToBytes(sequence_number);
			byte[] my_header = new byte[3];
			my_header[0] = temp[0]; my_header[1] = temp[1];
			for (int i = 0; i < 3; i++) my_arr[i] = my_header[i];
			return;
		}

		public void setSentBool(boolean val) {
			hasSent = val;
			return;
		}
	}
}
