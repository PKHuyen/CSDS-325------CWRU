package network;

public class RouterV extends Router{
    public RouterV() {
        super("v");
    }
    public static void main(String[] args) {
        RouterV node = new RouterV();
        node.drive();
    }
}
