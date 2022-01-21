#define _GNU_SOURCE
#include <pthread.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <netinet/in.h>
#include <sys/wait.h>
#include <stdlib.h>
#include <netdb.h>
#include <signal.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <unistd.h>
#include <errno.h>

struct cln {
  int cfd;
  struct sockaddr_in caddr;
};

struct cln *players[2];
int bufferSize = 4;
int playerInRoom = -1;

int safeSend(int cfd, char buffer[], int size) {
	int correctlySend = 0, i;

	while (size != correctlySend) {
		i = write(cfd, buffer + correctlySend, size - correctlySend);

		// wykrycie bledow
		if (i == 0 || i == -1) {
			printf("%s\n", strerror(errno));
			return 0;
		}

		correctlySend = correctlySend + i;
	}

	return correctlySend;
}

int safeReceive(int cfd, char buffer[], int size) {
	int correctlyReceived = 0, i;

	while (size != correctlyReceived) {
		i = read(cfd, buffer + correctlyReceived, size - correctlyReceived);

		// wykrycie bledow
		if (i == 0 || i == -1) {
			printf("%s\n", strerror(errno));
			return 0;
		}

		correctlyReceived = correctlyReceived + i;
	}

	return correctlyReceived;
}

void *game(void *arg) {
	char buffer[4];
	int running = 1, lostConnection = 0, result;
	
	struct cln *firstPlayer = players[0];
	printf("New connection, ip: %s, port: %d\n", inet_ntoa((struct in_addr)firstPlayer->caddr.sin_addr), firstPlayer->caddr.sin_port);
	
	struct cln *secondPlayer = players[1];
	printf("New connection, ip: %s, port: %d\n", inet_ntoa((struct in_addr)secondPlayer->caddr.sin_addr), secondPlayer->caddr.sin_port);

	// przydzielenie koloru graczowi pierwszemu
	result = safeSend(firstPlayer->cfd, "BBBB", bufferSize);

	// sprawdzenie czy pierwszy gracz jest wciaz polaczony
	if (result == 0) {
		// wyslanie powiadomienia do gracza drugiego, jesli pierwszy nie jest polaczany
		buffer[0] = 'L';
		buffer[1] = 'O';
		buffer[2] = 'S';
		buffer[3] = 'T';
		
		safeSend(secondPlayer->cfd, buffer, bufferSize);

		close(firstPlayer->cfd);
		close(secondPlayer->cfd);

		free(firstPlayer);
		free(secondPlayer);

		return EXIT_SUCCESS;
	}

	// przydzielenie koloru graczowi drugiemu
	result = safeSend(secondPlayer->cfd, "WWWW", bufferSize);

	if (result == 0) {
		// wyslanie powiadomienia do gracza pierwszego, jesli drugi nie jest polaczany
		buffer[0] = 'L';
		buffer[1] = 'O';
		buffer[2] = 'S';
		buffer[3] = 'T';
	
		safeSend(firstPlayer->cfd, buffer, bufferSize);

		close(firstPlayer->cfd);
		close(secondPlayer->cfd);

		free(firstPlayer);
		free(secondPlayer);

		return EXIT_SUCCESS;
	}

	while (running == 1) {
		result = safeReceive(firstPlayer->cfd, buffer, bufferSize);
		printf("Received %s\n", buffer);
		// sprawdzenie czy przeciwnik wciaz jest polaczony
		if (result == 0) {
			running = 0;
			lostConnection = 1;
		}

		// powiadomienie o utracie polaczenia z przeciwnikiem
		if (lostConnection == 1) {
			running = 0;

			buffer[0] = 'L';
			buffer[1] = 'O';
			buffer[2] = 'S';
			buffer[3] = 'T';
		}

		result = safeSend(secondPlayer->cfd, buffer, bufferSize);
		printf("Sent %s\n", buffer);

		if (result == 0) {
			// powiadomienie przeciwnika, w przypadku gdy stracimy polaczenie
			if (lostConnection == 0) lostConnection = 1;
			// zakonczenie wykonywanie petli, gdy obie strony straca polaczenie
			else running = 0;
		}

		if (running == 0) break;

		if (lostConnection == 0) {
			result = safeReceive(secondPlayer->cfd, buffer, bufferSize);
			printf("Received %s\n", buffer);

			if (result == 0) {
				lostConnection = 1;
				running = 0;
			}
		}

		// powiadomienie o utracie polaczenia z przeciwnikiem
		if (lostConnection == 1) {
			running = 0;
			
			buffer[0] = 'L';
			buffer[1] = 'O';
			buffer[2] = 'S';
			buffer[3] = 'T';
		}

		result = safeSend(firstPlayer->cfd, buffer, bufferSize);
		printf("Sent %s\n", buffer);

		if (result == 0) {
			running = 0;

			buffer[0] = 'L';
			buffer[1] = 'O';
			buffer[2] = 'S';
			buffer[3] = 'T';
		
			safeSend(secondPlayer->cfd, buffer, bufferSize);
		}
	}
    
	close(firstPlayer->cfd);
	close(secondPlayer->cfd);

	free(firstPlayer);
	free(secondPlayer);

	return EXIT_SUCCESS;
  
}

int main(int argc, char * argv[]) {
	struct sockaddr_in saddr;
  	pthread_t tid;
	int sfd, on = 1;
	socklen_t sl;
	
	saddr.sin_port = htons(3333);
	saddr.sin_family = PF_INET;
  	saddr.sin_addr.s_addr = INADDR_ANY;
	
	sfd = socket(PF_INET, SOCK_STREAM, 0);
	setsockopt(sfd, SOL_SOCKET, SO_REUSEADDR, (char*)&on, sizeof(on));
	bind(sfd, (struct sockaddr*)&saddr, sizeof(saddr));
	listen(sfd, 5);

	while (1) {
	  struct cln* c = malloc(sizeof(struct cln));
	  sl = sizeof(c->caddr);
	  c->cfd = accept(sfd, (struct sockaddr*)&c->caddr, &sl);

	  printf("New client connected\n");

	  playerInRoom++;
	  players[playerInRoom] = c;
     	  
		if(playerInRoom == 1) {
			playerInRoom = -1;
			printf("New room created\n");

			pthread_create(&tid, NULL, game, players);
			pthread_detach(tid);
		}
	}
	
	close(sfd);

	return EXIT_SUCCESS;
}
