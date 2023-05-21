# RENAME!!!!!!!!!!  This file to game.py
import random
import time
from termcolor import colored
from tqdm import tqdm
import mysql.connector
from pymongo import MongoClient


#Connect credentials to MongoDB
DOMAIN = 'mongodb'
PORT = 27017
client = MongoClient(
        host = [ str(DOMAIN) + ":" + str(PORT) ],
        serverSelectionTimeoutMS = 3000, # 3 second timeout
        username = "admin",
        password = "root",
    )

###CONNECT AND CREATE COLLECTION IN MongoDB #########
db = client['mydb']
collection = db['game_score']


#Connect credentials to mysqlDB
connection = mysql.connector.connect(
    user='root', 
    password='root', 
    host='mysql', 
    port="3306",
    database='game_score')
print("DB connected")


###CONNECT AND CREATE TABLE IN MYSQL #########
mycursor = connection.cursor()
mycursor.execute('CREATE TABLE IF NOT EXISTS game_score (player1_name VARCHAR(255), player2_name VARCHAR(255), player1_score INT, player2_score INT, winer VARCHAR(255));')




############ START MAIN SECTION ######################

board3d = []
for x in range(0, 10):
    board3d.append(" " + str(x))
for x in range(10, 28):
    board3d.append(str(x))

def defaut_board():
    for x in range(0, 10):
        board3d[x] = (" " + str(x))
    for x in range(10, 28):
        board3d[x] = (str(x))

win_combinations = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6),
            (9,10,11),(12,13,14),(15,16,17),(9,12,15),(10,13,16),(11,14,17),(9,13,17),(11,13,15),
            (18,19,20),(21,22,23),(24,25,26),(18,21,24),(19,22,25),(20,23,26),(18,22,26),(20,22,24),
            (0,9,18),(1,10,19),(2,11,20),(3,12,21),(4,13,23),(5,14,23),(6,15,24),(7,16,25),(8,17,26),
            (0,10,20),(2,10,18),(2,14,26),(8,14,20),(8,16,24),(6,16,26),(6,12,18),(0,12,24),(3,13,23),
            (5,13,21),(1,13,25),(7,13,19),(0,13,26),(2,13,24),(8,13,18),(6,13,20),(4,13,22)]

def draw():
    print()
    print(board3d[1] + '|' + board3d[2] + '|' + board3d[3] + '\t\t' + board3d[10] + '|' + board3d[11] + '|' + board3d[12] + '\t\t' + board3d[19] + '|' +
          board3d[20] + '|' + board3d[21])
    print('--|--|--' + '\t\t' + '--|--|--' + '\t\t' + '--|--|--')

    print(board3d[4] + '|' + board3d[5] + '|' + board3d[6] + '\t\t' + board3d[
        13] + '|' + board3d[14] + '|' + board3d[15] + '\t\t' + board3d[22] + '|' +
          board3d[23] + '|' + board3d[24])
    print('--|--|--' + '\t\t' + '--|--|--' + '\t\t' + '--|--|--')

    print(board3d[7] + '|' + board3d[8] + '|' + board3d[9] + '\t\t' + board3d[
        16] + '|' + board3d[17] + '|' + board3d[18] + '\t\t' + board3d[25] + '|' +
          board3d[26] + '|' + board3d[27])
    print()


def check_win(player_moves):

    flag = 0
    for combination in win_combinations:
        counter = 0
        for element in player_moves:
            if element in combination:
                if counter == 2:
                    flag = 1
                counter += 1
    return flag

def choice_validation(player_choice):
    valid = 1
    if not player_choice.isnumeric():
        valid = 0
    else:
        if int(player_choice) < 1 or int(player_choice) > 27 or board3d[int(player_choice)] == " \033[1;4;34mX\033[0m" or board3d[int(player_choice)] == " \033[1;4;35mO\033[0m":
            valid = 0
    return valid

def main():
    first_player = input("Enter The First Player Name : ")
    second_player = input("Enter The Second Player Name : ")
    first_player_moves = []
    second_player_moves = []
    first_player_score = 0
    second_player_score = 0
    print("Shufelling....")
    for i in tqdm(range(20), colour = 'GREEN'):
        time.sleep(0.1)
    shuffle = random.randint(0,1)
    if shuffle == 0:  
        print(first_player," \033[1;4;34mWill Play First\033[0m")
        first_player_token = " \033[1;4;34mX\033[0m"
        second_player_token = " \033[1;4;35mO\033[0m"
    else:
        print(second_player," \033[1;4;35mWill Play First\033[0m")
        first_player_token = " \033[1;4;34mO\033[0m"
        second_player_token = " \033[1;4;35mX\033[0m"
    for i in range(shuffle,28):
        draw()
        if i%2 == 1:
            choice = input("Dear, " + second_player + ", In Which Cell Do You Want To Put Your " + second_player_token + " ? >> ")
            valid_choice = choice_validation(choice)
            while valid_choice == 0:
                print("\033[91mnot valid...try again\033[0m")
                choice = input("Dear, " + second_player + ", In Which Cell Do You Want To Put Your " + second_player_token  + " ? >> ")
                valid_choice = choice_validation(choice)
            board3d[int(choice)] = second_player_token
            second_player_moves.append(int(choice) - 1)
            win = check_win(second_player_moves)
            if win == 1:
                draw()
                print(second_player," \033[32mIs The Winner\033[0m")
                second_player_score+=1
                print("The Score Is : ",first_player_score," For",first_player)
                print("The Score Is : ", second_player_score, " For", second_player)
                print()
                con = input("\033[1;35mDo You Want To Continue ?\033[0m [\033[32mY\033[0m/\033[91mN\033[0m] > ")
                while con != 'y' and con != 'n':
                    print("You Must Enter Only \033[32my\033[0m Or \033[91mn\033[0m ")
                    con = input("\033[1;35mDo You Want To Continue ?\033[0m [\033[32mY\033[0m/\033[91mN\033[0m] > ")
                if con == 'y':
                    print("\033[32mWe Are Starting a new round\033[0m")
                    first_player_moves = []
                    second_player_moves = []
                    i = 0
                    defaut_board()
                else:
                    print("\033[1;33mThank You For Playing, Good BYE!!!\033[0m ")
                    return first_player, second_player, first_player_score, second_player_score
                    exit()
        else:
            choice = input("Dear, " + first_player + ", In Which Cell Do You Want To Put Your " + first_player_token + " ? >> ")
            valid_choice = choice_validation(choice)
            while valid_choice == 0:
                print("\033[91mnot valid...try again\033[0m")
                choice = input("Dear, " + first_player + ", In Which Cell Do You Want To Put Your " + first_player_token + " ? >> ")
                valid_choice = choice_validation(choice)
            board3d[int(choice)] = first_player_token
            first_player_moves.append(int(choice) - 1)
            win = check_win(first_player_moves)
            if win == 1:
                draw()
                print(first_player," \033[32mIs The Winner\033[0m")
                first_player_score+=1
                print("\033[1;33mThe Score Is :\033[0m ",first_player_score," For",first_player)
                print("\033[1;33mThe Score Is :\033[0m ", second_player_score, " For", second_player)
                print()
                con = input("\033[1;35mDo You Want To Continue ?\033[0m [\033[32mY\033[0m/\033[91mN\033[0m] > ")
                while con != 'y' and con != 'n':
                    print("You Must Enter Only \033[32my\033[0m Or \033[91mn\033[0m ")
                    con = input("\033[1;35mDo You Want To Continue ?\033[0m [\033[32mY\033[0m/\033[91mN\033[0m] > ")
                if con == 'y':
                    print("\033[32mWe Are Starting a new round\033[0m")
                    first_player_moves = []
                    second_player_moves = []
                    i = 0
                    defaut_board()
                else:
                    print("\033[1;33mThank You For Playing, Good BYE!!!\033[0m ")
                    if first_player_score > second_player_score:
                        winner = first_player
                    elif first_player_score < second_player_score:
                        winner = second_player
                    else:
                        winner = 'tie'
                    return first_player, second_player, first_player_score, second_player_score, winner
                    exit()


first_player, second_player, first_player_score, second_player_score, winner = main()

############ END MAIN SECTION ######################



############  DONT CHANGE IT PLEASSE WITHOUT REASON!!!  ###############
#####MYSQL DB INSERT SECTION 
print("Insertting data to \033[91mMySQL\033[0m database")
print(first_player, second_player, first_player_score, second_player_score, winner)

sql = "INSERT INTO game_score (player1_name, player2_name, player1_score, player2_score, winer) VALUES (%s, %s, %s, %s, %s )"
val = (first_player, second_player, first_player_score, second_player_score, winner)
mycursor.execute(sql, val)

connection.commit()

print(mycursor.rowcount, "record inserted.")
print("Data to \033[91mMYSQL\033[0m successfully inserted!!! ")



#####Mongo DB INSERT SECTION 
print(first_player, second_player, first_player_score, second_player_score, winner)

print("Insertting data to \033[32mMongoDB\033[0m database")
#print(P1,P2,P1s,P2s,W)



print(first_player, second_player, first_player_score, second_player_score, winner)


collection.insert_one({"first player name": first_player,
                       "second player name": second_player,
                       "first player score": first_player_score,
                       "second player score": second_player_score,
                       "Winner": winner})

print("Data to \033[32mMongoDB\033[0m successfully inserted!!! ")

############# THE END!!!!





