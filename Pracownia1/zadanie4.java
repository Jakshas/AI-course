import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.util.Scanner;

public class zadanie4 {

    public static void main(String[] args) throws IOException {
        Scanner sc = new Scanner(new File("zad4_input.txt"));
        File f = new File("zad4_output.txt");
        FileWriter wr = new FileWriter(f);
        while (sc.hasNext()) {
            String s = sc.next();
            int n = sc.nextInt();
            int x = opt_dist(s, n);
            wr.append(x+"\n");
        }
        wr.close();
    }
    
    public static int opt_dist(String s, int n){
        int x = s.length();
        char[] c = s.toCharArray();
        for (int i = 0; i <= s.length() - n; i++) {
            int l = 0;
            for (int j = 0; j < i; j++) 
                if (c[j] == '1') l++;
            for (int j = 0; j < n; j++) 
                if (c[i+j] == '0') l++;
            for (int j = 0; i+n+j < s.length(); j++) 
                if (c[i+n+j] == '1') l++;
            if (l < x) x = l;
        }
        return x;
    }
}