import java.util.*;
import java.io.*;
import java.net.*;
import java.util.concurrent.atomic.AtomicLong;
import message.Message;
import message.Type;

public class Server {
    //Server port is preidentified as 5555 according to the problem
    private final int port = 5555;

    //This configuration table initialize the table that server will send out to all routers after they join
    private final String path = "configurationPath.txt";

    //Stores the server socket
    private final DatagramSocket serverSocket;

    //Stores the initial table (from configuration table)
    private final HashMap<String, HashMap<String,Integer>> initTable = new HashMap<>();

    //Stores the neighbor table (for update)
    private final HashMap<String, ArrayList<String>> neighborTable = new HashMap<>();

    //Stores the address of all routers
    private final HashMap<String, InetSocketAddress> addressTable = new HashMap<>();

    //Stores the value of timer, if exceeds, terminate the connection between routers and server
    private static final long timer = 2000;

    /**Constructor of the server */
    public Server() {
        try {
            //Initialize server socket
            serverSocket = new DatagramSocket(this.port);
            //read the configuration path
            BufferedReader r = new BufferedReader(new FileReader(path));
            String line;
            //Read the configuration path and add to the table to initialize initial table
            while ((line = r.readLine()) != null) {
                String[] data = line.replaceAll("<","").replaceAll(">","").replaceAll(":","").replaceAll(",","").split(" ");
                ArrayList<String> neighborList = new ArrayList<>();
                HashMap<String, Integer> table = new HashMap<>();
                table.put(data[0], 0);
                for (int i = 1; i < data.length; i+=2) {
                    String neighborID = data[i];
                    int cost = Integer.parseInt(data[i+1]);
                    table.put(neighborID, cost);
                    if (cost < 0) continue;
                    neighborList.add(neighborID);
                }
                neighborTable.put(data[0], neighborList);
                initTable.put(data[0], table);
            }
            //close the BufferedReader, prevent leak
            r.close();
        }
        catch(IOException e) {
            throw new RuntimeException(e);
        }
    }

    /**Accept method to accept all nodes available in the built network to join */
    public void accept() {
        //Wait for all routers join the network, add the address to addressTable for later reference
        while (addressTable.size() < initTable.size()) {
            Message receivedMessage = Message.recv(serverSocket);
            if (receivedMessage.checkType(Type.JOIN)) {
                addressTable.put(receivedMessage.getID(), receivedMessage.getSocketAddress());
            }
            else continue;
        }
        //After all routers join the network
        initTable.forEach((router, neighbor) -> {
            //Retrieve socket address of router
            InetSocketAddress routerAddress = addressTable.get(router);
            //Retrieve the map from initTable
            HashMap<String, Integer> initMap = initTable.get(router);
            //Send the table to all router
            Message.send(serverSocket, new Message(Type.RESPONSE, routerAddress, router, initMap));
        });
    }

    /**Update method to receive Update request from routers */
    public void update() {
        AtomicLong start = new AtomicLong(System.currentTimeMillis());
        //Create thread, wait for update request from routers
        Thread t = new Thread(() -> {
            while (true) {
                Message receivedMessage = Message.recv(serverSocket);
                start.set(System.currentTimeMillis());
                if (receivedMessage.checkType(Type.UPDATE)){
                    //Get neighbor and send the updated table to them
                    ArrayList<String> neighborList = neighborTable.get(receivedMessage.getID());
                    neighborList.forEach(destination -> {
                        receivedMessage.setSocketAddress(addressTable.get(destination));
                        Message.send(serverSocket, receivedMessage);
                    });
                }
                else continue;
            }
        });
        t.start();
        while (System.currentTimeMillis() - start.get() <= timer){}
        terminate(t);
    }

    /**Terminate the connection */
    public void terminate(Thread t) {
        t.interrupt();
        Message message = new Message(Type.TERMINATE, null, "");
        Collection<String> allRouters = addressTable.keySet();
        allRouters.forEach(destination -> {
            message.setSocketAddress(addressTable.get(destination));
            Message.send(serverSocket, message);
        });
    }

    /**Main method to run this program */
    public static void main(String[] args) {
        Server server = new Server();
        System.out.println("Initiate Server");
        server.accept();
        server.update();
        System.out.println("Closed");
    }
}