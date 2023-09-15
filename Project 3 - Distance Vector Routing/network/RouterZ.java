package network;

public class RouterZ extends Router{
    public RouterZ() {
        super("z");
    }
    public static void main(String[] args) {
        RouterZ node = new RouterZ();
        node.drive();
    }
}
