import java.io.InputStream;
import java.io.OutputStream;
import java.net.Socket;



public class Program {

	public static void main (String[] args) throws Exception {		
		int port = 0; //donner une valeur correcte
		String host = ""; //donner une valeur correcte
		
		// Connexion au serveur
		try {
			//connecte la socket
			Socket socket = new Socket(host, port);
			
			//Récupère le flux d'entrée de la socket
			InputStream in = socket.getInputStream();
			OutputStream out = socket.getOutputStream();
		} catch (Exception e) {
			//Gérer ici les problèmes
		}
		
		//Envoi du nom
		String nomEquipe = "";
		byte[] trameNME = ("NME" + nomEquipe).getBytes();
        
        try {
            out.write(trameNME, 0, trameNME.length);
        } catch (Exception e) {
            System.out.println("Erreur d'écriture de la trame NME");
			//gérer les erreurs
        }
		
		//début des échanges
		while (true) {
            boolean isByeTrame = client.receiveTrame();
            if (isByeTrame) {
                break;
            }
        }
		
		//fermeture de tout
		in.close();
        out.close();
        socket.close();
		
	}
    

    // Méthode qui permet de traiter les trames
    static boolean receiveTrame() throws Exception {
	
		//lecture des 3 premiers octets
        byte[] trame = new byte[3];
        int nbBytesLus = in.read(trame, 0, 3);
        if (nbBytesLus != 3) {
            throw new Exception("Erreur de lecture de l'entÃªte de trame");
        }
        String typeTrame = new String(trame, "ASCII");
        
		//action en fonction de la nature de la trame
        if (typeTrame.equalsIgnoreCase("SET")) {
            trame = new byte[2];
            nbBytesLus = in.read(trame, 0, 2);
            if (nbBytesLus != 2) {
                throw new Exception("Erreur de lecture de la trame SET");
            }
            //Effectuer ici ce qui est nécessaire pour la commande SET
			//Sachant que trame[0] est le nombre de lignes, et trame[1] de colonnes
			
        } else if (typeTrame.equalsIgnoreCase("HUM")) {
            trame = new byte[1];
            nbBytesLus = in.read(trame, 0, 1);
            if (nbBytesLus != 1) {
                throw new Exception("Erreur de lecture de N de la trame HUM");
            }
            int N = (int) trame[0] & 0xff;
            trame = new byte[2 * N];
            nbBytesLus = in.read(trame, 0, 2 * N);
            if (nbBytesLus != 2 * N) {
                throw new Exception("Erreur de lecture des données de la trame HUM");
            }
			//traiter la trame ici pour la commande HUM
            //Il y a N maisons à  placer
			//donc N couples X Y de coordonnées
        } else if (typeTrame.equalsIgnoreCase("HME")) {
            trame = new byte[2];
            nbBytesLus = in.read(trame, 0, 2);
            if (nbBytesLus != 2) {
                throw new Exception("Erreur de lecture de la trame HME");
            }
            //placer ici le traitement de la commande HME
			//trame contient X Y, coordonnées de votre maison
        } else if (typeTrame.equalsIgnoreCase("MAP")) {
            trame = new byte[1];
            nbBytesLus = in.read(trame, 0, 1);
            if (nbBytesLus != 1) {
                throw new Exception("Erreur de lecture de N de la trame MAP");
            }
            int N = (int) trame[0] & 0xff;
            trame = new byte[5 * N];
            nbBytesLus = in.read(trame, 0, 5 * N);
            if (nbBytesLus != 5 * N) {
                throw new Exception("Erreur de lecture des données de la trame MAP");
            }
            //traiter ici la trame correspondant à  MAP
			//Il y a N changements
			//chaque changement correspond à  5 cases du tableau
        } else if (typeTrame.equalsIgnoreCase("UPD")) {
            trame = new byte[1];
            nbBytesLus = in.read(trame, 0, 1);
            if (nbBytesLus != 1) {
                throw new Exception("Erreur de lecture de N de la trame UPD");
            }
            int N = (int) trame[0] & 0xff;
            trame = new byte[5 * N];
            nbBytesLus = in.read(trame, 0, 5 * N);
            if (nbBytesLus != 5 * N) {
                throw new Exception("Erreur de lecture des données de la trame UPD");
            }
            //traiter ici la trame correspondant à  UPD
			//Il y a N changements
			//chaque changement correspond à  5 cases du tableau
			
			//calculer le prochain coup ici
			
			//envoyer les commandes MOV ou ATK
			byte[] response = null; //affecter correctement
			try {
				out.write(response, 0, response.length);
			} catch (Exception e) {
				System.out.println("Erreur d'écriture de la trame MOV ou ATK");
			}
				
        } else if (typeTrame.equalsIgnoreCase("END")) {
            //ajouter ici les actions à  faire en fin de partie
        } else if (typeTrame.equalsIgnoreCase("BYE")) {
            return true;
        } else {
            throw new Exception("Trame non reconnue");
        }
        return false;
    }

}
