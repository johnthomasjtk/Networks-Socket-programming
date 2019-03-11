import json
import sys
import socket
import os

NUMBER_OF_CLIENTS = 3


def mergeDictionaries(x, y):
    z = x.copy()
    z.update(y)
    return z


def processGame(jsonString):
    inputDict = json.loads(jsonString)

    lastSqr = inputDict["board_dimension"] ** 2
    laddersNSnakes = mergeDictionaries(inputDict["ladders"], inputDict["snakes"])
    dieTosses = inputDict["die_tosses"]

    gameState = {}
    gameState["winner"] = None
    gameState["game_state"] = "progress"
    gameState["final_positions"] = {}
    gameState["squares_traversed"] = {}

    roundNum = 1
    while gameState["game_state"] == "progress" and str(roundNum) in dieTosses:        # for each round, do the following; until the game is finished.
        round = dieTosses[str(roundNum)]
        playersInRound = len(round)

        for playerNum in range(1, playersInRound + 1):      # for each player in the round, do the following..
            if str(playerNum) not in gameState["final_positions"]:      # initialisation
                gameState["final_positions"][str(playerNum)] = 0
                gameState["squares_traversed"][str(playerNum)] = []

            if gameState["final_positions"][str(playerNum)] + round[str(playerNum)] <= lastSqr:
                gameState["final_positions"][str(playerNum)] += round[str(playerNum)]
                gameState["squares_traversed"][str(playerNum)].append(gameState["final_positions"][str(playerNum)])

                if gameState["final_positions"][str(playerNum)] == lastSqr:
                    gameState["game_state"] = "finished"

                while gameState["game_state"] == "progress" and str(gameState["final_positions"][str(playerNum)]) in laddersNSnakes:
                    gameState["final_positions"][str(playerNum)] = laddersNSnakes[str(gameState["final_positions"][str(playerNum)])]
                    gameState["squares_traversed"][str(playerNum)].append(gameState["final_positions"][str(playerNum)])

                    if gameState["final_positions"][str(playerNum)] == lastSqr:
                        gameState["game_state"] = "finished"

                if gameState["game_state"] == "finished":
                    gameState["winner"] = playerNum
                    break

        roundNum += 1

    return json.dumps(gameState) + "\n"


def serveClient(sockt):
    socktFile = sockt.makefile()
    query = socktFile.readline()

    while query != '0\n':
        response = processGame(query)
        sockt.sendall(response)
        query = socktFile.readline()

    socktFile.close()
    sockt.close()


def server():
    port = int(sys.argv[1])
    processIDs = []

    serverSocket = socket.socket()
    serverSocket.bind(('', port))
    serverSocket.listen(5)

    while len(processIDs) != NUMBER_OF_CLIENTS:
        (sockt, _) = serverSocket.accept()
        pid = os.fork()

        if pid == 0:            # Child process
            serveClient(sockt)
            serverSocket.close()
            return
        else:                   # Parent process
            processIDs.append(pid)

    for i in range(NUMBER_OF_CLIENTS):	# wait for all the children before exiting...
        os.waitpid(processIDs[i], 0)

    serverSocket.close()

server()
