package network;

public class RouterW extends Router{
    public RouterW() {
        super("w");
    }
    public static void main(String[] args) {
        RouterW node = new RouterW();
        node.drive();
    }
}
