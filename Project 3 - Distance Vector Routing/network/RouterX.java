package network;

public class RouterX extends Router{
    public RouterX() {
        super("x");
    }
    public static void main(String[] args) {
        RouterX node = new RouterX();
        node.drive();
    }
}
