package zadanie2;

import java.util.ArrayList;

public class Slowa {
    String slowo;
    ArrayList<Slowa> dzieci;
    int dlugosc;

    Slowa(String s, int i){
        dlugosc = i;
        slowo = s;
        dzieci = new ArrayList<Slowa>();
    }
}
