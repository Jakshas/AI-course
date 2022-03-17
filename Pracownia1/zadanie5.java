import java.io.File;
import java.io.FileNotFoundException;
import java.util.Random;
import java.util.Scanner;

public class zadanie5 {
    public static void main(String[] args) throws FileNotFoundException {
        // int[] kolumny = {2,2,6,6,2,2};
        // int[] wiersze = {2,2,6,6,2,2};
        int[] kolumny = {5,4,3,2,1};
        int[] wiersze = {5,4,3,2,1};
        wypisz(znajdzobrazek(kolumny, wiersze));
    }

    public static void wypisz(int[][] obrazek) {
        for (int i = 0; i < obrazek.length; i++) {
            for (int j = 0; j < obrazek[i].length; j++) {
                System.out.print(obrazek[j][i]);
            }
            System.out.println();
        }
    }

    public static int[][] znajdzobrazek(int[] kolumny, int[] wiersze){
        Random rand = new Random();
        int[][] obrazek = new int[kolumny.length][wiersze.length];
        int zmiany = 0;
        while (!czypoprawnyobrazek(obrazek, kolumny, wiersze)) {
            zmiany = 0;
            obrazek = new int[kolumny.length][wiersze.length];
            while (!czypoprawnyobrazek(obrazek, kolumny, wiersze) && zmiany < 2000) {
                int r;
                do{
                    r = rand.nextInt(kolumny.length);
                    zmiany++;
                }while (kolumny[r] == sumujkol(obrazek, r) && zmiany < 2000);
                znajdzpasujacy(obrazek, r, kolumny, wiersze);
                zmiany++;
            }
        }
        return obrazek;
    }

    public static boolean sprawdzwiersze(int[][] obrazek,int[] kolumny, int[] wiersze , int r) {
        for (int i = 0; i < wiersze.length; i++) {
            if (sumujwiersz(obrazek, i) != wiersze[i]) {
                return false;
            }
        }
        return true;
    }

    public static void znajdzpasujacy(int[][] obrazek, int k, int[] kolumny, int[] wiersze) {
        Random r = new Random();
        int rn;
        int[] tab = new int[wiersze.length];
        if (sumujkol(obrazek, k) > kolumny[k]) {
            for (int i = 0; i < wiersze.length; i++) {
                do{
                    rn = r.nextInt(wiersze.length);
                }
                while (tab[rn] == 1);
                tab[rn] = 1;
                if (obrazek[k][rn] == 1 && sumujwiersz(obrazek, rn) >= wiersze[i]) {
                    obrazek[k][rn] = 0;
                    return;
                }
            }
        }else{
            for (int i = 0; i < wiersze.length; i++) {
                do{
                    rn = r.nextInt(wiersze.length);
                }
                while (tab[rn] == 1);
                tab[rn] = 1;
                if (obrazek[k][rn] == 0 && sumujwiersz(obrazek, rn) <= wiersze[i]) {
                    obrazek[k][rn] = 1;
                    return;
                }
            }
        }
    }

    public static int sumujwiersz(int[][] obrazek, int r) {
        int wynik = 0;
        int i=0;
        while (i < obrazek.length && obrazek[i][r] == 0) {
            i++;
        }
        while (i < obrazek.length && obrazek[i][r] == 1){
            i++;
            wynik++;
        }
        return wynik;
    }

    public static int sumujkol(int[][] obrazek, int r) {
        int wynik = 0;
        int i=0;
        while (i < obrazek.length && obrazek[r][i] == 0) {
            i++;
        }
        while (i < obrazek.length && obrazek[r][i] == 1){
            i++;
            wynik++;
        }
        return wynik;
    }

    public static boolean czypoprawnyobrazek(int[][] obrazek, int[] kolumny, int[] wiersze){
        for (int i = 0; i < kolumny.length; i++) {
            int pom = sumujkol(obrazek, i);
            if (pom != kolumny[i]) {
                return false;
            }
        }
        for (int i = 0; i < wiersze.length; i++) {
            int pom =sumujwiersz(obrazek, i); 
            if (pom != wiersze[i]) {
                return false;
            }
        }
        return true;
    }
}
