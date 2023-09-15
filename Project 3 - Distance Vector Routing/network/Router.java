package network;
import java.util.*;
import java.util.concurrent.atomic.AtomicBoolean;
import java.net.*;
import message.Message;
import message.Type;
public class Router {
    //Stores the port number of server
    public final int port = 5555;

    //Stores the server address
    private InetSocketAddress serverAddress;
    
    //Stores the routerID (name)
    private final String routerID;

    //Stores the routerSocket
    private final DatagramSocket routerSocket;
    
    //Stores the table <router, cost>
    private HashMap<String, Integer> table;
    
    //Stores the parent table of each router <router, parent>
    private HashMap<String, String> parent = new HashMap<>();

    /**Constructor for Router */
    public Router(String routerID) {
        this.routerID = routerID;
        try {
            routerSocket = new DatagramSocket();
        }
        catch(SocketException e) {
            throw new RuntimeException(e);
        }
    }

    /** Connect the router to server */
    public void connect (InetSocketAddress serverAddress) {
        //Send JOIN message to serverAddress
        this.serverAddress = serverAddress;
        Message.send(routerSocket, new Message(Type.JOIN, this.serverAddress, this.routerID));

        //Receive RESPONSE message from routerSocket
        Message receivedMessage = Message.recv(routerSocket);
        if (receivedMessage.checkType(Type.RESPONSE)) {
            //Update the current table (null) to current table (table get from configuration path) and update the rest of the table
            this.table = receivedMessage.getTable();
            table.forEach((router, cost) -> {
                if (cost < 0) {
                    table.put(router, Integer.MAX_VALUE - 1000);
                    parent.put(router, null);
                }
                else {
                    parent.put(router, router);
                }
            });
        }
        else return;
    }

    /**Update the router */
    public void update() {
        //Send the update request to server
        Message.send(routerSocket, new Message(Type.UPDATE, this.serverAddress, this.routerID, this.table));

        //Wait for response (other's router request)
        while (true) {
            Message receivedMessage = Message.recv(routerSocket);
            if (receivedMessage.checkType(Type.UPDATE)) {
                String neighborID = receivedMessage.getID();
                HashMap<String, Integer> receivedTable = receivedMessage.getTable();
                AtomicBoolean changed = new AtomicBoolean(false);
                //Update table
                table.forEach((router, cost) -> {
                    int newCost = table.get(neighborID) + receivedTable.get(router);
                    int old = table.get(router);
                    if (newCost < old) {
                        table.put(router, newCost);
                        parent.put(router, neighborID);
                        changed.set(true);
                    }
                });
                if (changed.get() == false) continue;
                Message.send(routerSocket, new Message(Type.UPDATE, serverAddress, routerID, this.table));
            }
            else if (receivedMessage.checkType(Type.TERMINATE)) break;
            else continue;
        }
    }

    /** Print table, format <destination router, cost>*/
    public String printTable() {
        StringBuilder b = new StringBuilder();
        table.entrySet().stream().sorted(Map.Entry.comparingByKey()).forEach(e -> b.append(String.format(" <%s,%d>", e.getKey(), e.getValue() == Integer.MAX_VALUE -1000 ? -1 : e.getValue())));
        return b.toString();
    }

    /**Run this class */ 
    public void drive() {
        InetSocketAddress serverAddress;
        try {
            serverAddress = new InetSocketAddress(InetAddress.getByName("localhost"), port);
        }
        catch(UnknownHostException e) {
            throw new RuntimeException(e);
        }
        this.connect(serverAddress);
        System.out.println("Initial Table: " + printTable() + "\n");
        this.update();
        System.out.println("Updated Table: " + printTable());
    }
}
