import network.*;
public class Run {
    public static void run (Router router) {
        new Thread(router :: drive).start();
    }
    
    public static void main(String[] args) {
        RouterU u = new RouterU();
        RouterV v = new RouterV();
        RouterW w = new RouterW();
        RouterX x = new RouterX();
        RouterY y = new RouterY();
        RouterZ z = new RouterZ();
        run(u);
        run(v);
        run(w);
        run(x);
        run(y);
        run(z);
    }
}
