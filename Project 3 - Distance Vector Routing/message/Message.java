package message;
import java.util.*;
import java.io.*;
import java.net.*;

public class Message implements Serializable{
    //Stores the type of this message;
    private final Type type;

    //Stores the socket address of the server or router that sends this message
    private InetSocketAddress socketAddress;

    //Stores the id of the server or router that sends this message
    private final String id;

    //Stores the table that this message is sending
    private final HashMap<String, Integer> table;

    /** Constructor of the Message, type response and update */
    public Message (Type type, InetSocketAddress socketAddress, String id, HashMap<String, Integer> table) {
            this.type = type;
            this.socketAddress = socketAddress;
            this.id = id;
            this.table = table;
    }

    /**Constructor of this message, type join and terminate */
    public Message (Type type, InetSocketAddress socketAddress, String id) {
        this(type, socketAddress, id, null);
    }

    /** Helper method to retrieve the type of this message */
    public Type getType() {
        return this.type;
    }

    /** Helper method to retrieve the socket address of this message */
    public InetSocketAddress getSocketAddress() {
        return this.socketAddress;
    }

    /** Helper method to change the socket address of this message */
    public void setSocketAddress(InetSocketAddress socketAddress) {
        this.socketAddress = socketAddress;
    }

    /** Helper method to retrieve the id of the message's sender */
    public String getID() {
        return this.id;
    }

    /** Helper method to retrieve the table */
    public HashMap<String, Integer> getTable() {
        return this.table;
    }

    /** Helper method to check the type */
    public boolean checkType(Type type) {
        return this.type == type;
    }

    /**Send message to the socket */
    public static void send(DatagramSocket socket, Message message) {
        byte[] queue = new byte[2048];
        //Converting message into byte array
        try(ByteArrayOutputStream a = new ByteArrayOutputStream(); ObjectOutputStream b = new ObjectOutputStream(a)){
            b.writeObject(message);
            queue = a.toByteArray();
        }
        catch (IOException e) {
            throw new RuntimeException(e);
        }
        //Sending byte array
        DatagramPacket packet = new DatagramPacket(queue, queue.length, message.getSocketAddress());
        try {
            socket.send(packet);
        }
        catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    /** Recv message from the socket */
    public static Message recv(DatagramSocket socket) {
        byte[] queue = new byte[2048];
        DatagramPacket packet = new DatagramPacket(queue, queue.length);
        try {
            socket.receive(packet);
        }
        catch (IOException e) {
            throw new RuntimeException(e);
        }

        Message receivedMessage;
        try(ByteArrayInputStream a = new ByteArrayInputStream(packet.getData()); ObjectInputStream b = new ObjectInputStream(a)){
            receivedMessage = (Message)(b.readObject());
        }
        catch (IOException | ClassNotFoundException e) {
            throw new RuntimeException(e);
        }
        receivedMessage.setSocketAddress(new InetSocketAddress(packet.getAddress(), packet.getPort()));
        return receivedMessage;
    }
}
