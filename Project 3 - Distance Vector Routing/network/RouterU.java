package network;

public class RouterU extends Router{
    public RouterU() {
        super("u");
    }
    public static void main(String[] args) {
        RouterU node = new RouterU();
        node.drive();
    }
}
