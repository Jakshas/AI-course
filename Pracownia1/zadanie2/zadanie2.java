package zadanie2;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.Collator;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Scanner;

public class zadanie2 {
    public static void main(String[] args) throws IOException {
        File file = new File("zadanie2\\slowa.txt");
        Scanner sc = new Scanner(file);
        ArrayList<String> text = new ArrayList<String>();
        ArrayList<String> slowa = new ArrayList<String>();
        while (sc.hasNext()) {
            String i = sc.next();
            slowa.add(i);
        }
        sc.close();
        sc = new Scanner(new File("zadanie2\\1.txt"));
        while (sc.hasNext()) {
            String i = sc.next();
            text.add(i);
        }
        Collections.sort(slowa);
        ArrayList<Slowa> sl = new ArrayList<Slowa>();
        FileWriter file2 = new FileWriter("zadanie2\\zad2_output.txt");
        for (int g = 0; g <= 500; g++) {
            String string = text.get(g);
        //  for (String string : text) {
            sl.clear();
            for (int i = 1; i <= string.length(); i++) {
                String s = string.substring(0, i);
                if (wslowach(slowa, s)) {
                    sl.add(new Slowa(s, i));
                }
            }
            for (Slowa slowo : sl) {
                przeszukanie(slowo, string.substring(slowo.dlugosc ,string.length()), slowa);
            }
            najlepsze(string.length(), 0, 0, sl);
            maxdl = 0;
            String out = "";
            for (String str : smax) {
                out += str+" ";
            }
            out = out.substring(0, out.length()-1);
            out += '\n';
            file2.append(out);
        }
        file2.close();
    }

    public static void przeszukanie(Slowa sl, String text, ArrayList<String> slowa) {
        for (int i = 1; i <= text.length(); i++) {
            String s = text.substring(0, i);
            if (wslowach(slowa, s)) {
                sl.dzieci.add(new Slowa(s, i));
            }
        }
        for (Slowa slowo : sl.dzieci) {
            przeszukanie(slowo, text.substring(slowo.dlugosc,text.length()), slowa);
        }
    }

    public static boolean wslowach(ArrayList<String> slowa, String sl) {
        if (Collections.binarySearch(slowa, sl) > 0) {
            return true;
        }else{
            return false;
        }
    }

    static int maxdl = 0;
    static ArrayList<String> smax = new ArrayList<String>();
    static ArrayList<String> str = new ArrayList<String>();
    static Collator myDefaultCollator = Collator.getInstance();

    public static void najlepsze(int dlugosctxt, int dlugosc, int suma, ArrayList<Slowa> ars) {
        for (Slowa string : ars) {
            str.add(string.slowo);
            if ((dlugosc + string.dlugosc == dlugosctxt) && maxdl < (suma + (string.dlugosc*string.dlugosc))) {
                maxdl = suma + (string.dlugosc*string.dlugosc);
                smax.clear();
                for (String string2 : str) {
                    smax.add(string2);
                }
            }else{
                najlepsze(dlugosctxt, dlugosc + string.dlugosc, suma + (string.dlugosc*string.dlugosc), string.dzieci);
            }
            str.remove(str.size()-1);
        }
    }
}
