using System;
using System.Collections.Generic;
using System.Net;
using System.Net.Sockets;
using System.Text;
using System.Threading;
using VampiresVSWerewolves;


namespace TestClient
{
    class Program2
    {
        static byte[]
            NME = Encoding.ASCII.GetBytes("NME"),
            ATK = Encoding.ASCII.GetBytes("ATK"),
            MOV = Encoding.ASCII.GetBytes("MOV");
        
        

        static void Main(string[] args)
        {
            string ip = "138.195.86.154";
            int port = 5555;

            /****************** DEMARRAGE ******************/
            //crée le point terminal de la connexion
            var ipep = new System.Net.IPEndPoint(IPAddress.Parse(ip), port);
            
            //crée une socket pour se connecter au serveur
            Socket socket = new Socket(AddressFamily.InterNetwork, SocketType.Stream, ProtocolType.Tcp);

            //demande de connection
            socket.Connect(ipep);

            /****************** PROTOCOLE: nom ******************/
            //on envoie NME
            socket.Send(NME);
            socket.Send(new byte[] { 7 });
            socket.Send(Encoding.ASCII.GetBytes("NomDuJoueur")); //<-- Remplacez ici par le nom de votre groupe

            /****************** PROTOCOLE: carte ******************/
            //on reçoit SET
            while (socket.Available < 5)
                Thread.Sleep(100);
            byte[] buffer = new byte[2048];
            socket.Receive(buffer, 5, SocketFlags.Partial);
            
            if (Encoding.ASCII.GetString(buffer, 0, 3) != "SET")
                throw new Exception("Erreur, attendu: SET");
            
            //Utilisez buffer[3] (lignes) et buffer[4] (colonnes) pour créer une grille
            
            //on recoit HUM
            while (socket.Available < 4)
                Thread.Sleep(100);
            socket.Receive(buffer, 4, SocketFlags.Partial);
            if (Encoding.ASCII.GetString(buffer, 0, 3) != "HUM")
                throw new Exception("Erreur, attendu: HUM");
            while (socket.Available < buffer[3] * 2) //ici on attend les arguments
                Thread.Sleep(100);
            int read = socket.Receive(buffer, buffer[3]*2, SocketFlags.Partial);

            //read contient deux fois le nombre de maisons dans la carte
            //pour tout i pair ou nul, buffer[i] contient x et buffer[i+1] contient y

            //on recoit HME, c'est-à-dire la case où sont placés vos montres
            while (socket.Available < 5)
                Thread.Sleep(100);
            socket.Receive(buffer, 5, SocketFlags.Partial);
            if (Encoding.ASCII.GetString(buffer, 0, 3) != "HME")
                throw new Exception("Erreur, attendu: HME");
            
            //Mettez à jour votre grille en utilisant (buffer[3], buffer[4]) comme coordonnées de votre demeure

            //on recoit MAP
            while (socket.Available < 4)
                Thread.Sleep(100);
            socket.Receive(buffer, 4, SocketFlags.Partial);
            if (Encoding.ASCII.GetString(buffer, 0, 3) != "MAP")
                throw new Exception("Erreur, attendu: MAP");
            while (socket.Available < buffer[3] * 5)
                Thread.Sleep(100);

            read = socket.Receive(buffer, buffer[3] * 5, SocketFlags.Partial);

            //read contient 5x le nombre de 5-tuplets.
            //buffer contient la liste des changements



            /****************** PARTIE ******************/
            while (true)
            {
                //ATTENTE D'UN MESSAGE DU SERVEUR (UPD OU END)
                while (socket.Available < 3)
                    Thread.Sleep(100);
                socket.Receive(buffer, 3, SocketFlags.Partial);
                string cmd = Encoding.ASCII.GetString(buffer, 0, 3);

                if (cmd == "END") break; //Ici on gère la sortie de la boucle
                if (cmd != "UPD") throw new Exception("Erreur protocole, attendu : UPD");

                //si on est là c'est qu'on a reçu UPD
                while (socket.Available < 1)
                    Thread.Sleep(100);
                socket.Receive(buffer, 1, SocketFlags.Partial);

                //buffer[0] contient le nombre de changements à prendre en compte
                if (buffer[0] > 0)
                {
                    Console.WriteLine("Cellules modifiées:");

                    while (socket.Available < buffer[0] * 5)
                        Thread.Sleep(100);

                    read = socket.Receive(buffer, buffer[0] * 5, SocketFlags.Partial);

                    //buffer contient read = n * 5 5-tuplets
                    //n est le nombre de changements

                    //modifiez votre grille ici en fonction des changements
                }

                //ICI FAITES VOS CALCULS
                byte[] response = new byte[0];
                //créez un byte[] contenant tout ce qu'il faut
                socket.Send(response);
            }   
			
			socket.Close();
			socket.Dispose();
        }
    }
}
