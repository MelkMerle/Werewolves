#include <iostream>
using std::cout;

#include <winsock2.h>
#pragma comment(lib, "ws2_32.lib")


int main()
{
	std::string nickname = "";

	//Initialisation des sockets
	WSADATA WSAData; //variable n�cessaire
    try
	{
		WSAStartup(MAKEWORD(2,0), &WSAData);
	}
	catch (char* str)
	{
		cout<<"Erreur initialisation socket: " << str;
	}
	
	SOCKET sock;
	SOCKADDR_IN sin;
	sin.sin_addr.s_addr	= inet_addr("127.0.0.1"); //<-- mettre la bonne ip
	sin.sin_family		= AF_INET;
	sin.sin_port		= htons(5555); //<-- mettre le bon port
	sock = socket(AF_INET,SOCK_STREAM,0);

	try
	{
		connect(sock, (SOCKADDR *)&sin, sizeof(sin));
	}
	catch (char* str)
	{
		cout<<"Erreur d'attache de la socket: " << str;
	}

	//Envoie du nom
	char* trameNME = "NME*NOM"; //Mettez ici le nom de l'�quipe en laissant le *
	trameNME[3] = (char) (sizeof trameNME - 4);
	try
	{
		send(sock, trameNME, sizeof trameNME, 0);
	}
	catch (char *err)
	{
		cout<<"Erreur envoi NME: " << err;
	}

	delete nomEquipe;
	delete trameNME;

	char code[3];
	while (1)
	{
		//on recoit les trois premiers octets
		int read;
		try
		{
			read = recv(sock, code, 3, 0);
		}
		catch (std::exception *e)
		{
			cout<<"Probl�me r�ception commande";
		}

		if (read != 3)
		{
			throw std::exception("La commande ne fait pas 3 caract�res!");
		}

		if (code == "SET") {
			//Traitement de la commande SET
			char buffer[2];
			try
			{
				read = recv(sock, buffer, 2, 0);
			}
			catch (std::exception *e)
			{
				cout<<"Probl�me r�ception commande SET";
			}
			if (read != 2)
			{
				throw std::exception("La commande SET ne fait pas 2 octets!");
			}
			//mettez ici tout ce qu'il faut faire pour traiter SET sachant que x et y sont
			//dans les cases 0 et 1 de buffer

			delete buffer;
		} if (code == "HUM") {
			char *buffer = new char[1];
            try
			{
				read = recv(sock, buffer, 1, 0);
			}
			catch (std::exception *e)
			{
				cout<<"Probl�me r�ception commande HUM";
			}
			if (read != 1)
			{
				throw std::exception("La commande HUM a un probl�me!");
			}
            int N = (int) buffer[0];
			delete buffer;

            buffer = new char[2 * N];
            try
			{
				read = recv(sock, buffer, 2*N, 0);
			}
			catch (std::exception *e)
			{
				cout<<"Probl�me r�ception commande HUM";
			}
			if (read != 2*N)
			{
				throw std::exception("La commande HUM a un probl�me!");
			}

			//traiter la trame ici pour la commande HUM
            //Il y a N maisons � placer
			//donc N couples X Y de coordonn�es

			delete buffer;
		} else if (code == "HME") {
            char *buffer = new char[2];
            try
			{
				read = recv(sock, buffer, 2, 0);
			}
			catch (std::exception *e)
			{
				cout<<"Probl�me r�ception commande HME";
			}
			if (read != 2)
			{
				throw std::exception("La commande HME a un probl�me!");
			}
            //placer ici le traitement de la commande HME
			//trame contient X Y, coordonn�es de votre maison

			delete buffer;
        } else if (code == "MAP") {
            char *buffer = new char[1];
            try
			{
				read = recv(sock, buffer, 1, 0);
			}
			catch (std::exception *e)
			{
				cout<<"Probl�me r�ception commande MAP";
			}
			if (read != 1)
			{
				throw std::exception("La commande MAP a un probl�me!");
			}
            int N = (int) buffer[0];
			delete buffer;

            buffer = new char[5*N];
            try
			{
				read = recv(sock, buffer, 5*N, 0);
			}
			catch (std::exception *e)
			{
				cout<<"Probl�me r�ception commande MAP";
			}
			if (read != 5*N)
			{
				throw std::exception("La commande MAP a un probl�me!");
			}
            //traiter ici la trame correspondant � MAP
			//Il y a N changements
			//chaque changement correspond � 5 cases du tableau

			delete buffer;
        } else if (code == "UPD") {
            char *buffer = new char[1];
            try
			{
				read = recv(sock, buffer, 1, 0);
			}
			catch (std::exception *e)
			{
				cout<<"Probl�me r�ception commande MAP";
			}
			if (read != 1)
			{
				throw std::exception("La commande MAP a un probl�me!");
			}
            int N = (int) buffer[0];
			delete buffer;
            buffer = new char[5*N];
            try
			{
				read = recv(sock, buffer, 5*N, 0);
			}
			catch (std::exception *e)
			{
				cout<<"Probl�me r�ception commande MAP";
			}
			if (read != 5*N)
			{
				throw std::exception("La commande MAP a un probl�me!");
			}
            //traiter ici la trame correspondant � UPD
			//Il y a N changements
			//chaque changement correspond � 5 cases du tableau
			
			delete buffer;

			//calculer le prochain coup ici
			
			//envoyer les commandes MOV ou ATK
			char *response = NULL; //affecter correctement
			try {
				send(sock, response, sizeof response, 0);
			} catch (std::exception e) {
				cout<<"Erreur d'�criture de la trame MOV ou ATK";
			}
			delete response;
        } else if (code == "END") {
            //ajouter ici les actions � faire en fin de partie
        } else if (code == "BYE") {
            break;
        } else {
            throw std::exception("Trame non reconnue");
        }
		
	}
	delete code;

	//Pr�parez ici la fin de votre programme
	
	//Fermeture des sockets
	try
	{
		closesocket(sock);
		delete &sock;
		WSACleanup();
	}
	catch (char* str)
	{
		cout<<"Erreur de fermeture de la socket: " << str;
	}


	return 0;
}