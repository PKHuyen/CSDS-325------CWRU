import java.net.*;
import java.io.*;
import java.util.*;

public class Proxy {
    private static int port = 9099;
    private final Socket socket;
    private static final HashMap<String, byte[]> cache = new HashMap<>();

    public Proxy(Socket socket) {
        this.socket = socket;
    }

    public void init() {
        try {
            //Receive request from the client and read
            InputStream client = socket.getInputStream();
            BufferedReader reader = new BufferedReader(new InputStreamReader(client));
            String request = reader.readLine();
            String[] requestMessage = request.split(" ");
            String url = requestMessage[1];

            //Send the request to the destination (destination is taken from url extracted when reading the request)
            byte[] cached = cache.get(url);
            if (cached == null) {
                HttpURLConnection connection = (HttpURLConnection)new URL(url).openConnection();
                connection.setRequestMethod(requestMessage[0]);

                //Get server's response
                InputStream server = connection.getInputStream();
                ByteArrayOutputStream response = new ByteArrayOutputStream();

                //Reformat the response, add status line, reponse header, and body
                String status = "HTTP/1.1 " + connection.getResponseCode() + " " + connection.getResponseMessage() + "\r\n";
                response.write(status.getBytes());
                for (String key : connection.getHeaderFields().keySet()) {
                    if (key != null) {
                        String header = key + ": " + connection.getHeaderField(key) + "\r\n";
                        response.write(header.getBytes());
                    }
                }
                response.write("\r\n".getBytes());
                byte[] buffer = new byte[2048];
                while (server.read(buffer) != -1) response.write(buffer, 0, server.read(buffer));
                cached = response.toByteArray();
                cache.put(url, cached);

                //Disconnect connection to the server
                connection.disconnect();

                //Send reponse to client
                OutputStream toClient = socket.getOutputStream();
                toClient.write(cached);
                toClient.flush();

                //Disconnect with the client
                socket.close();
            }
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main (String[] args) {
        try (ServerSocket serverSocket = new ServerSocket(9099)) {
            System.out.println("Listening on port 9099");
            while (true) new Proxy(serverSocket.accept()).init();
        }
        catch (IOException e) {
            e.printStackTrace();
        }
    }
}