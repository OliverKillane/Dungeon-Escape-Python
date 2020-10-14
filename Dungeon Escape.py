#DUNGEON ESCAPE V2

#Constant declaration

gametitle = '''██████╗ ██╗   ██╗███╗   ██╗ ██████╗ ███████╗ ██████╗ ███╗   ██╗    ███████╗███████╗ ██████╗ █████╗ ██████╗ ███████╗
██╔══██╗██║   ██║████╗  ██║██╔════╝ ██╔════╝██╔═══██╗████╗  ██║    ██╔════╝██╔════╝██╔════╝██╔══██╗██╔══██╗██╔════╝
██║  ██║██║   ██║██╔██╗ ██║██║  ███╗█████╗  ██║   ██║██╔██╗ ██║    █████╗  ███████╗██║     ███████║██████╔╝█████╗  
██║  ██║██║   ██║██║╚██╗██║██║   ██║██╔══╝  ██║   ██║██║╚██╗██║    ██╔══╝  ╚════██║██║     ██╔══██║██╔═══╝ ██╔══╝  
██████╔╝╚██████╔╝██║ ╚████║╚██████╔╝███████╗╚██████╔╝██║ ╚████║    ███████╗███████║╚██████╗██║  ██║██║     ███████╗
╚═════╝  ╚═════╝ ╚═╝  ╚═══╝ ╚═════╝ ╚══════╝ ╚═════╝ ╚═╝  ╚═══╝    ╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝     ╚══════╝
                                                                                                                   '''

scorefile = "Dungeon Escape Scores.txt"
gamemap = '''       ╔═════╗╔═╗                         
 ╔═══╗ ║     ╚╝ ║                         
 ║   ║ ║     ╔══╝                         
 ╚╗B╔╝ ╚═╗G╔═╝                            
  ║ ║    ║ ║                              
╔═╝B╚═╗╔═╝G╚═╗╔════════════╗              
║     ╚╝     ║║           W╚              
║     ╔╗R  BK╚╝            ╔              
╚═╗Y╔═╝║     ╔╗B           ║              
  ║ ║  ╚═╗B╔═╝╚═╗O╔════════╝              
  ║X║    ║ ║    ║ ║                       
  ║X║  ╔═╝B╚═╗╔═╝O╚═╗                     
  ║X║  ║     ║║    B╚════╗                
  ║X║  ║     ║║     ╔══╗ ║                
  ║ ║  ║M╔═══╝╚═════╝  ║ ║                
╔═╝ ╚═╗║M║     ╔═══╗ ╔═╝B╚═╗╔═════╗       
║    B╚╝B║     ║  Y╚═╝     ╚╝     ║       
║     ╔══╝     ║   ╔═╗Y   R╔╗R    ║       
╚═════╝        ╚╗R╔╝ ║     ║╚═╗S╔═╝       
                ║ ║  ╚═════╝  ║ ║         
       ╔═════╗╔═╝R╚═╗╔═════╗  ║ ║  ╔═╗    
       ║    B╚╝     ║║    G╚══╝S╚══╝O║    
       ║     ╔╗B   M╚╝M    ╔╗G   O╔══╝    
       ╚═╗G╔═╝║     ╔═╗B╔══╝╚═════╝       
         ║ ║  ╚═╗Y╔═╝ ║ ║                 
         ║ ║  ╔═╝Y╚═╗                     
         ║ ╚══╝     ║                     
         ╚════╗G    ║                     
              ║     ║                     
              ╚╗SH╔═╝                     '''

#Imports:
from time import gmtime, strftime, time, sleep
from operator import itemgetter
from random import choice, randint

def mainmenu():
    print(gametitle)
    while True:
        user_request = input("PLEASE SELECT AN OPTION:\n(1) - TUTORIAL\n(2) - SCORES\n(3) - PLAY GAME\n(4) - CREDITS\n(5) - EXIT\nSELECT:  ").strip()
        if user_request == "1":
            print("In this game you must escape the dungeon by typing in commands to; move, gather items, and perform actions.\n")
        elif user_request == "2":
            print("SCORES:")
            print(general.getscores() + "\n")
        elif user_request == "3":
            user_result = Game()
            general.writescore(user_result.player.name, user_result.player.score)
            del user_result
        elif user_request == "4":
            print("This game was a collaboration between Jon Snedden and Oliver Killane, and storyline development guidance from Evrim Muharrem.\n")
        elif user_request == "5":
            quit()
    
class general:
    def genmap():
        raw_map = gamemap.split("\n")
        final_map = [[list()] * 6] * 30
        final_map = [[line[7 * sector : 7 * sector + 7] for sector in range(0,6)] for line in raw_map]
        return final_map
            
        
    def display_status(player):
        if len(player.items) > 0:
            print("INVENTORY:")
            for index in range(0, len(player.items)):
                print("(" + str(index + 1) + ") - " + player.items[index])
        print("HEALTH:   " + str(player.health) + "%")
    
    def probability(maximum):
        return choice(sum([[i] * (maximum - i) for i in range(0, maximum)],[])) * choice([-1,1]) * 10 ** -1
    
    def check_int(required, minimum, maximum):
        try:
            required = int(required)
            if required >= minimum and required <= maximum:
                return True
            else:
                return False
        except ValueError:
            return False
        
    def getscores():
        file = open(scorefile, "r")
        raw_scores = file.readlines()
        file.close()
        scores = [{"name" : item.split("\t")[0], "score" : int(item.split("\t")[1]), "datetime" : item.split("\t")[3].strip("\n")} for item in raw_scores]
        scores = sorted(scores, key = itemgetter("score"))
        output = str()
        for index in range(0, len(scores)):
            output += "(" + str(index+1) + ") - " + scores[index]["name"].upper() + " " * max(12 - len(scores[index]["name"]), 0) + str(scores[index]["score"] // 60) + " MINUTES " + str(scores[index]["score"] % 60) + " SECONDS " + "\t" + scores[index]["datetime"].upper() + "\n"
        return output
            
        
    def writescore(name, score):
        file = open(scorefile, "a")
        file.write("\n" + name + "\t" + str(int(score)) + "\t\t" + strftime("%H:%M, %x", gmtime()))
        file.close()

        
class Player():
    def __init__(self):
        self.health = 100
        self.name = self.setname()
        self.score = time()
        self.items = list()
        self.attrs = ["SOCK_AVAILABLE", "BACON_AVAILABLE", "FEAST_AVAILABLE", "POTION_AVAILABLE", "BLACK_KEY_AVAILABLE", "AXE_AVAILABLE", "SWORD_AVAILABLE", "POISON_DAGGER_AVAILABLE","ORANGE_KEY_AVAILABLE","PORK_AVAILABLE","DEATH_POTION_AVAILABLE","SHINY_KEY_AVAILABLE"]

    def setname(self):
        temp_name = input("PLEASE ENTER A NAME FROM 3 - 9 CHARACTERS:  ").strip()
        while not len(temp_name) >= 3 or not len(temp_name) <= 9:
            print("ERROR - NAME IS AN INCORRECT LENGTH")
            temp_name = input("PLEASE ENTER A NAME FROM 3 - 9 CHARACTERS:  ").strip()
        return temp_name

class Events(general):
    def __init__(self, player, opponent):
        self.player = player
        self.completed = False
        self.opponents = {"WIZARD" :{"NAME" : "MAGICAL WIZARD","HEALTH": 100, "ATTACKS" :[{"TEXT" : "HARMFUL SPELL", "DAMAGE" : 20, "CHANCE" : 40},{"TEXT" : "STICK WHACK", "DAMAGE" : 15, "CHANCE" : 45}, {"TEXT" : "FLAMING BALLS", "DAMAGE" : 30, "CHANCE" : 15}]},
                        "MONSTER" :{"NAME" : "UGLY MONSTER","HEALTH" : 100, "ATTACKS" : [{"TEXT" : "BITE", "DAMAGE" : 30, "CHANCE" : 15}, {"TEXT" : "HARD SHOVE", "DAMAGE" : 10, "CHANCE" : 40}, {"TEXT" : "CLAW SWIPE", "DAMAGE" : 25, "CHANCE" : 25},{"TEXT" : "ACID SPIT", "DAMAGE" : 30, "CHANCE" : 20}]},
                          "REAPER" :{"NAME" : "GRIM REAPER","HEALTH": 100, "ATTACKS" :[{"TEXT" : "GHOSTLY GRAPPLE", "DAMAGE" : 30, "CHANCE" : 25},{"TEXT" : "REAPER\'S REVENGE", "DAMAGE" : 40, "CHANCE" : 25}, {"TEXT" : "SCYTHE SWIPE", "DAMAGE" : 20, "CHANCE" : 50}]},
                          "GHOUL" : {"NAME" : "GROSS GHOUL","HEALTH": 100, "ATTACKS" :[{"TEXT" : "PARANORMAL PUNCH", "DAMAGE" : 40, "CHANCE" : 10},{"TEXT" : "SLY SLAP", "DAMAGE" : 20, "CHANCE" : 40},{"TEXT" : "SLITHERING SLASH", "DAMAGE" : 30, "CHANCE" : 30},{"TEXT" : "SHIVER SIDESWIPE", "DAMAGE" : 35, "CHANCE" : 25}]}
                        }
        #Monster format: "" :{"NAME" : "","HEALTH": 0, "ATTACKS" :[{"TEXT" : "", "DAMAGE" : 0, "CHANCE" : 0}]}
        
        self.player_options = [{"TEXT" : "SWORD STAB", "DESCR" : "Stab your sword into the belly of the beast.", "DAMAGE" : 35, "REQ_ATTRS" : ["SWORD_TAKEN"], "DISPOSABLE" : False, "REMOVE" : ["SWORD_TAKEN", "SHINY SWORD"]},
                               {"TEXT" : "AXE SWING", "DESCR" : "Swing your mighty sharp axe at the beast.", "DAMAGE" : 30, "REQ_ATTRS" : ["AXE_TAKEN"], "DISPOSABLE" : False, "REMOVE" : ["AXE_TAKEN","SHARP AXE"]},
                               {"TEXT" : "SOCK SMASH", "DESCR" : "Attack the beast with a mysterious sock.", "DAMAGE" : 20, "REQ_ATTRS" : ["SOCK_TAKEN"], "DISPOSABLE" : False,"REMOVE" : ["SOCK_TAKEN","OLD SOCK"]},
                               {"TEXT" : "BLACK KEY STAB", "DESCR" : "Thrust the black key into the monster's underside.", "DAMAGE" : 15, "REQ_ATTRS" : ["BLACK_KEY_TAKEN"], "DISPOSABLE" : False,"REMOVE" : []},
                               {"TEXT" : "BACON BREAKFAST", "DESCR" : "Consume the bacon to gain health.","DAMAGE" : -20, "REQ_ATTRS" : ["BACON_TAKEN"], "DISPOSABLE" : True,"REMOVE" : [ "BACON_TAKEN","DELICIOUS BACON"]},
                               {"TEXT" : "MAGICAL MEDICINE", "DESCR" : "Drink your magical potion to heal.", "DAMAGE" : -40, "REQ_ATTRS" : ["POTION_TAKEN"], "DISPOSABLE" : True,"REMOVE" : [ "POTION_TAKEN", "MAGICAL POTION"]},
                               {"TEXT" : "VORATIOUS VOMIT", "DESCR" : "Unconsume your previous feast.", "DAMAGE" : 15, "REQ_ATTRS" : ["FEAST_TAKEN"], "DISPOSABLE" : True,"REMOVE" : ["FEAST_TAKEN"]},
                               {"TEXT" : "POISONOUS DAGGER", "DESCR" : "Cut the enemy with your poison laced dagger.", "DAMAGE" : 30, "REQ_ATTRS" : ["POISON_DAGGER_TAKEN"], "DISPOSABLE" : False, "REMOVE" : ["POISON_DAGGER_TAKEN", "POISONOUS DAGGER"]},
                               {"TEXT" : "ORANGE KEY STAB", "DESCR" : "Thrust the orange key into the monster's underside.", "DAMAGE" : 15, "REQ_ATTRS" : ["ORANGE_KEY_TAKEN"], "DISPOSABLE" : False, "REMOVE" : ["ORANGE_KEY_TAKEN", "ORANGE KEY"]},
                               {"TEXT" : "SALTY PORK", "DESCR" : "Eat the pork to gain health.", "DAMAGE" : -20, "REQ_ATTRS" : ["PORK_TAKEN"], "DISPOSABLE" : True, "REMOVE" : ["PORK_TAKEN", "SALTY PORK"]},
                               {"TEXT" : "SHINY KEY STAB", "DESCR" : "Thrust the shiny key into the monster's underside.", "DAMAGE" : 20, "REQ_ATTRS" : ["SHINY_KEY_TAKEN"], "DISPOSABLE" : False, "REMOVE" : ["SHINY_KEY_TAKEN", "SHINY KEY"]},
                               {"TEXT" : "POTION OF DEATH", "DESCR" : "Cover the opponent in the deathly potion.", "DAMAGE" : 40, "REQ_ATTRS" : ["DEATH_POTION_TAKEN"], "DISPOSABLE" : True, "REMOVE" : ["DEATH_POTION_TAKEN", "POTION OF DEATH"]}
                               ]
        #option format: {"TEXT" : "", "DESCR" : "", "DAMAGE" : 0, "REQ_ATTRS" : [""], "DISPOSABLE" : False, "REMOVE" : ["", ""]}
        self.opponent = self.opponents[opponent]
        self.battle()
    
    def battle(self):
        while self.player.health > 0 and self.opponent["HEALTH"] > 0:
            self.monster_move()
            if not self.player.health > 0:
                break
            print("\n")
            self.player_move()
            print("\n")
        if self.opponent["HEALTH"] == 0:
            print("YOU KILLED THE " + self.opponent["NAME"] + " AND ARE VICTORIOUS!")
            self.completed = True
            if self.player.health + 40 <= 100:
                print("YOUR HEALTH IS BOOSTED BY 40 TO " + str(self.player.health + 40) + ".")
            else:
                print("YOUR HEALTH IS BOOSTED BY " + str(100 - self.player.health) + " TO 100")
            self.player.health = min(self.player.health + 40, 100)
        else:
            print("YOU DIE AT THE " + self.opponent["NAME"] + "\'S HAND!")
            
    def monster_move(self):
        option = randint(1,100)
        for index in range(0, len(self.opponent["ATTACKS"])):
            if option - self.opponent["ATTACKS"][index]["CHANCE"] <= 0:
                option = self.opponent["ATTACKS"][index]
                break
            else:
                option -= self.opponent["ATTACKS"][index]["CHANCE"]

        delta_player_health = randint(int(option["DAMAGE"] * 0.8), int(option["DAMAGE"] * 1.2))
        if self.player.health - delta_player_health < 0:
            delta_player_health = self.player.health
        print(self.opponent["NAME"] + " USES " + option["TEXT"]  + " TO DO " + str(delta_player_health) + " DAMAGE.")
        self.player.health -= delta_player_health
        print("YOU ARE NOW AT " + str(self.player.health) + " HEALTH OUT OF 100.")
            
    def player_move(self):
        allowed_options = [option for option in self.player_options if all(required_attribute in self.player.attrs for required_attribute in option["REQ_ATTRS"])]
        allowed_options = sorted(allowed_options, key = itemgetter("DAMAGE"), reverse = True)
        for index in range(0, len(allowed_options)):
            if allowed_options[index]["DAMAGE"] >= 0:
                print("(" + str(index + 1) + ") - " + allowed_options[index]["TEXT"].upper() + "  \t - " + allowed_options[index]["DESCR"].upper() + "(ROUGHLY " + str(allowed_options[index]["DAMAGE"]) + " DAMAGE)")
            else:
                print("(" + str(index + 1) + ") - " + allowed_options[index]["TEXT"].upper() + "  \t - " + allowed_options[index]["DESCR"].upper() + "(ROUGHLY " + str(-1 * allowed_options[index]["DAMAGE"]) + " HEALING)")
        print("(S) - For status.")
        user_request = input("OPTION:    ")
        while not general.check_int(user_request, 1, len(allowed_options)):
            if user_request.lower() == "s":
                general.display_status(self.player)
            else:
                print("ERROR - INVALID REQUEST")
            if len(allowed_options) == 0:
                print("NO OPTIONS AVALIBLE")
                break
            user_request = input("OPTION:    ")
        if user_request.isnumeric():
            user_request = allowed_options[int(user_request) - 1]
            if user_request["DAMAGE"] > 0:
                delta_opponent_health = randint(int(user_request["DAMAGE"] * 0.8), int(user_request["DAMAGE"] * 1.2))
                if self.opponent["HEALTH"] - delta_opponent_health < 0:
                    delta_opponent_health = self.opponent["HEALTH"]
                print("YOU DEALT THE " + self.opponent["NAME"] + " " + str(delta_opponent_health) + " DAMAGE WITH " + user_request["TEXT"] + ".")
                self.opponent["HEALTH"] = self.opponent["HEALTH"] - delta_opponent_health
            else:
                delta_player_health = randint(int(-1 *user_request["DAMAGE"] * 0.8), int(-1 *user_request["DAMAGE"] * 1.2))
                if delta_player_health + self.player.health > 100:
                    delta_player_health = 100 - self.player.health
                print("YOU USED THE " + user_request["TEXT"] + " AND GAINED " + str(delta_player_health) + " HEALTH.")
                self.player.health += delta_player_health

            if user_request["DISPOSABLE"]:
                for item in user_request["REMOVE"]:
                    if item in self.player.items:
                        self.player.items.remove(item)
                    else:
                        self.player.attrs.remove(item)
            else:
                if randint(0,9) == 0:
                    for item in user_request["REMOVE"]:
                        if item in self.player.items:
                            self.player.items.remove(item)
                            print(item + " HAS BROKEN AND IS NO LONGER USABLE.")
                        else:
                            self.player.attrs.remove(item)
        print(self.opponent["NAME"] + "\'S HEALTH AT " + str(self.opponent["HEALTH"]) + " OUT OF 100.")

class Game(Events, Player, general):
    def __init__(self):
        self.player = Player()
        self.current_room = self.A
        return self.play()

    def displaymap(self):
        game_map = general.genmap()
        rooms = [["C","A","B","","",""],
                 ["D","E","F","F","",""],
                 ["H","G","J","L","",""],
                 ["H","I","K","L","M",""],
                 ["","N","O","P","Q","T"],
                 ["","N","","","",""]
                 ]
        output = str()
        output += "╔" + "═" * 42 + "╗\n"
        for line in range(0,30):
            output += "║"
            for sector in range(0,6):
                if rooms[line // 5][sector] in self.player.attrs:
                    output += game_map[line][sector]
                else:
                    output += " " * 7
            output += "║\n"
        output += "╚" + "═" * 42 + "╝"
        print(output)
    
    def play(self):
        while self.player.health > 0 and not self.current_room == "COMPLETE":
            self.current_room = self.current_room()
            print("\n")
        if self.current_room == "COMPLETE":
            print("FREEDOM ATTAINED\nTHANK YOU FOR PLAYING DUNGEON ESCAPE\nCOMPLETED IN:   " + str((time() - self.player.score) // 60) + "MINUTES AND " + str(int((time() - self.player.score) % 60)) + " SECONDS")
            self.player.score = time() - self.player.score
        else:
            print("GAME OVER\n\n")
            self.player.score = 0

    def action_selection(self, options):
        #Each options comes in form {"descr" : , "item_req" : , "attr_req" : , "func" : }
        for option in options:
            if not all(item in self.player.items for item in option["item_req"]):
                options.remove(option)
            if not all(item in self.player.attrs for item in option["attr_req"]):
                options.remove(option)
        
        for i in range(0, len(options)):
            print("(" + str(i + 1) + ") - " + options[i]["descr"])
        print("(S) - For status.\n(M) - For map.")
        user_request = input("SELECT OPTION:    ").strip()
        while not general.check_int(user_request, 1, len(options)):
            if user_request.lower() == "s":
                general.display_status(self.player)
                for i in range(0, len(options)):
                    print("(" + str(i + 1) + ") - " + options[i]["descr"])
                print("(S) - For status.\n(M) - For map.")
            elif user_request.lower() == "m":
                self.displaymap()
                for i in range(0, len(options)):
                    print("(" + str(i + 1) + ") - " + options[i]["descr"])
                print("(S) - For status.\n(M) - For map.")
            else:
                print("ERROR - PLEASE SELECT A VALID OPTION")
            user_request = input("SELECT OPTION:    ")
        return options[int(user_request) - 1]["func"]

    def A(self):
        #The start room.
        if "A" in self.player.attrs:
            print("You look about the cold dark room you started in.")
        else:
            print("You wake up, cold and disoriented in a dark room.")
            self.player.attrs.append("A")
        if "SWORD_AVAILABLE" in self.player.attrs:
            print("There is a large broadsword on the floor")
        print("To your right is a cupboard, to the left an old green door.")
        while True:
            result = self.action_selection([{"descr" : "Pick up the sword.", "item_req" : [], "attr_req" : ["SWORD_AVAILABLE"], "func" : "1"},{"descr" : "Go out the green door.", "item_req" : [], "attr_req" : [], "func" : self.E},{"descr" : "Open the dark cupboard in the corner of the room.", "item_req" : [], "attr_req" : [], "func" : self.B}])
            if result == "1":
                self.player.items.append("SHINY SWORD")
                self.player.attrs.remove("SWORD_AVAILABLE")
                self.player.attrs.append("SWORD_TAKEN")
            else:
                return result
        
    def B(self):
        #The cupboard in the start room.
        print("You open the cupboard.")
        if "SOCK_TAKEN" in self.player.attrs:
            print("It smells as if it once contained an old sock")
        else:
            print("It contains an old sock")
                
        if not "B" in self.player.attrs:
            self.player.attrs.append("B")
        else:
            print("You nostalgise about how great this cupboard was last time you opened it.")
        while True:
            result = self.action_selection([{"descr" : "Close the cupboard.", "item_req" : [], "attr_req" : [], "func" : self.A},{"descr" : "Take the old sock", "item_req" : [], "attr_req" :["SOCK_AVAILABLE"] , "func" : "1"}])
            if result == "1":
                self.player.items.append("OLD SOCK")
                self.player.attrs.remove("SOCK_AVAILABLE")
                self.player.attrs.append("SOCK_TAKEN")
            else:
                return result
        
        
    def C(self):
        print("You enter a dingey room with a single door")
        if "C" in self.player.attrs:
            print("You can remeber a being in a room like this previously.")
        else:
            self.player.attrs.append("C")
        while True:
            if "AXE_AVAILABLE" in self.player.attrs:
                print("There is an axe resting against one wall of the room, even better its been sharpened")
            result = self.action_selection([{"descr" : "Take the axe.", "item_req" : [], "attr_req" : ["AXE_AVAILABLE"], "func" : "1"},{"descr" : "Exit by the door.", "item_req" : [], "attr_req" : [], "func" : self.D}])
            if result == "1":
                self.player.items.append("SHARP AXE")
                self.player.attrs.remove("AXE_AVAILABLE")
                self.player.attrs.append("AXE_TAKEN")
            else:
                return result
        
    def D(self):
        if "D" in self.player.attrs:
            print("You enter a bacon smelling room, you have been here before")
        else:
            print("You enter another dark room, but this once smells delicious")
            self.player.attrs.append("D")
        if "BACON_AVAILABLE" in self.player.attrs:
            print("There is a delicious peice of bacon hanging from a string from the ceiling.")
        
        print("There are 3 doors leading in and out of the room, one red, one brown and one yellow")

        while True:
            result = self.action_selection([{"descr" : "Take the bacon.", "item_req" : [], "attr_req" : ["BACON_AVAILABLE"], "func" : "1"},{"descr" : "Open the red door", "item_req" : [], "attr_req" : [], "func" : self.E},{"descr" : "Open the brown door.", "item_req" : [], "attr_req" : [], "func" : self.C},{"descr" : "Open the yellow door.", "item_req" : [], "attr_req" : [], "func" : self.H}])
            if result == "1":
                print("You take the bacon.")
                self.player.items.append("DELICIOUS BACON")
                self.player.attrs.remove("BACON_AVAILABLE")
                self.player.attrs.append("BACON_TAKEN")
            else:
                if result == self.H:
                    print("As you enter the door you fall down a long slide, crashing throught the door onto the floor of the next room. \nThe door mysteriously slams shut behind you.") 
                return result
            
    def E(self):
        #The room adjacent to the starter room.
        if "E" in self.player.attrs:
            print("You re-enter the room adjacent to the dark room you started in.")
        else:
            print("You enter another dark room - and hear a noise somewhere beyond.")
            self.player.attrs.append("E")
        print("There is a door on each of the four sides, one green, one red, one blue and one black.")
        if "BLACK KEY" in self.player.items:
            print("You have the key to the black door, and all the others are unlocked")
        else:
            print("You try the handle of each door, all are unlocked, except for the black door")
        result = self.action_selection([{"descr" : "Open the green door", "item_req" : [], "attr_req" : [], "func" : self.A},{"descr" : "Open the red door", "item_req" : [], "attr_req" : [], "func" : self.D},{"descr" : "Open the blue door", "item_req" : [], "attr_req" : [], "func" : self.G},{"descr" : "Open the black door with your key", "item_req" : ["BLACK KEY"], "attr_req" : [], "func" : self.F}])
        return result
        
    def F(self):
        if not "MONSTER_VANQUISHED" in self.player.attrs:
            print("You enter a larger castle dining hall, with tables all set prepared for a feast and every candles lit.\nIt almost looks idilic, provided you ignore the monster eyeing up your flesh from the throne.")
            monster_game = Events(self.player, "MONSTER")
            self.player = monster_game.player
            if monster_game.completed:
                self.player.attrs.append("MONSTER_VANQUISHED")
            del monster_game
            return self.F
        else:
            if not "F" in self.player.attrs:
                print("Having vanquished the beast you feel fufilled in life. However you are hungry")
                self.player.attrs.append("F")
            else:
                print("You enter the dining hall of what you now presume is some sort of subterrainian castle. \nYou've been here before.")
            print("There is a black door, a large orange door, and a small white door.")
            while True:
                if not "FEAST_AVAILABLE" in self.player.attrs:
                    print("There is also lots of food left on the tables.")
                result = self.action_selection([{"descr" : "Feast on the food." , "item_req" : [], "attr_req" : ["FEAST_AVAILABLE"], "func" : "1"},{"descr" : "Open the white door", "item_req" : [], "attr_req" : [], "func" : "2"},{"descr" : "Open the orange door", "item_req" : [], "attr_req" : [], "func" : self.J},{"descr" : "Open the black door.", "item_req" : [], "attr_req" : [], "func" : self.E}])
                if result == "1":
                    print("You over-eat, and lose " + str(min(20, self.player.health)) + "health as a result.")
                    self.player.health = max(0, self.player.health - 25)
                    self.player.attrs.remove("FEAST_AVAILABLE")
                    self.player.attrs.append("FEAST_TAKEN")
                elif result == "2":
                    print("You fall to your death into a makeshift latrine as the rotten wooden facets break.")
                    self.player.health = 0
                    break
                else:
                    return result
        
    def G(self):
        print("You enter a large atrium, it like many of the other rooms smells very bad. There are only two doors, one blue and one mauve.")
        if "G" in self.player.attrs:
            print("You remember being in this very atrium before")
        else:
            print("You notice that there is a faint ray of light coming from the ceiling.")
            self.player.attrs.append("G")
        while True:
            if "BLACK_KEY_AVAILABLE" in self.player.attrs:
                print("There is a large black key on the floor.")
            result = self.action_selection([{"descr" : "Pick up the key." , "item_req" : [], "attr_req" : ["BLACK_KEY_AVAILABLE"], "func" : "1"},{"descr" : "Open the blue door", "item_req" : [], "attr_req" : [], "func" : self.E},{"descr" : "Open the mauve door", "item_req" : [], "attr_req" : [], "func" : self.I}])
            if result == "1":
                self.player.items.append("BLACK KEY")
                self.player.attrs.remove("BLACK_KEY_AVAILABLE")
                self.player.attrs.append("BLACK_KEY_TAKEN")
            else:
                return result
        
        
    def H(self):
        if not "WIZARD_VANQUISHED" in self.player.attrs:
            wizard_game = Events(self.player,"WIZARD")
            self.player = wizard_game.player
            if wizard_game.completed:
                self.player.attrs.append("WIZARD_VANQUISHED")
            del wizard_game
            return self.H
        else:
            print("Having defeated the wizard you stand back. \nThe room is abandoned and one door has been jammed shut with one brown door open.")
            if "POTION_AVAILABLE" in self.player.attrs:
                print("There is a potion on the floor in the corner")
            if "H" in self.player.attrs:
                print("You have been here before.")
            else:
                self.player.attrs.append("H")
            while True:
                result = self.action_selection([{"descr" : "Take potion" , "item_req" : [], "attr_req" : ["POTION_AVAILABLE"], "func" : "1"},{"descr" : "Open brown door.", "item_req" : [], "attr_req" : [], "func" : self.I}])
                if result == "1":
                    self.player.items.append("MAGICAL POTION")
                    self.player.attrs.remove("POTION_AVAILABLE")
                    self.player.attrs.append("POTION_TAKEN")
                else:
                    return result
            
        
    def I(self):
        print("You enter a small and crampt room, there are only two doors, one mauve and one brown.")
        if "I" in self.player.attrs:
            print("You recognise this room from before.")
        else:
            self.player.attrs.append("I")
        result = self.action_selection([{"descr" : "Open the brown door.", "item_req" : [], "attr_req" : [], "func" : self.H},{"descr" : "Open the mauve door.", "item_req" : [], "attr_req" : [], "func" : self.G}])
        return result

        
    def J(self):
        if "J" in self.player.attrs:
            print("You enter a narrrow, musty hallway, you have been here before.")
        else:
            print("You enter an odd smelling, musty, narrow corrdior.")
            self.player.attrs.append("J")
        result = self.action_selection([{"descr" : "Open the orange door.", "item_req" : [], "attr_req" : [], "func" : self.F},{"descr" : "Open the brown door.", "item_req" : [], "attr_req" : [], "func" : self.L}])
        return result

    def K(self):
        print("You enter a dingey room, with a low ceiling.")
        if "K" in self.player.attrs:
            print("You can remember being here before, it still smells just as bad.")
        else:
            print("It smells awful.")
            self.player.attrs.append("K")
        if "POISON_DAGGER_AVAILABLE" in self.player.attrs:
            print("There is a poison laced dagger on the floor.")
        while True:
            result = self.action_selection([{"descr" : "Pick up the poisonous dagger.", "item_req" : [], "attr_req" : ["POISON_DAGGER_AVAILABLE"], "func" : "1"}, {"descr" : "Open the red door.", "item_req" : [], "attr_req" : [], "func" : self.O}])
            if result == "1":
                self.player.items.append("POISONOUS DAGGER")
                self.player.attrs.remove("POISON_DAGGER_AVAILABLE")
                self.player.attrs.append("POISON_DAGGER_TAKEN")
            else:
                return result
            

    def L(self):
        print("You enter a dark and dingey atrium.")
        if "L" in self.player.attrs:
            print("You remember being here before")
        else:
            self.player.attrs.append("L")
        if "ORANGE_KEY_AVAILABLE" in self.player.attrs:
            print("There is an orange key on the floor.")
        while True:
            result = self.action_selection([{"descr" : "Take the orange key.", "item_req" : [], "attr_req" : ["ORANGE_KEY_AVAILABLE"], "func" : "1"},{"descr" : "Open the brown door.", "item_req" : [], "attr_req" : [], "func" : self.J},{"descr" : "Open the yellow door.", "item_req" : [], "attr_req" : [], "func" : self.K},{"descr" : "Open the red door.", "item_req" : [], "attr_req" : [], "func" : self.M}])
            if result == "1":
                self.player.items.append("ORANGE KEY")
                self.player.attrs.remove("ORANGE_KEY_AVAILABLE")
                self.player.attrs.append("ORANGE_KEY_TAKEN")
            elif result == self.K:
                print("As you walk toward the yellow door you fall through a trapdoor in the floor.")
                return self.K
            else:
                return result
        #{"descr" : "", "item_req" : [], "attr_req" : [], "func" : self.}

    def M(self):
        if not "REAPER_VANQUISHED" in self.player.attrs:
            reaper_game = Events(self.player, "REAPER")
            self.player = reaper_game.player
            if reaper_game.completed:
                self.player.attrs.append("REAPER_VANQUISHED")
            del reaper_game
            return self.M
        else:
            if "M" in self.player.attrs:
                print("You re-enter the baige, dusty, musty room.")
            else:
                print("You recover after defeating the reaper, and notice the room around you to be baige and musty.")
            print("There are two doors, one red, one silver.")
            self.player.attrs.append("M")
            result = self.action_selection([{"descr" : "Open the red door.", "item_req" : [], "attr_req" : [], "func" : self.L},{"descr" : "open the silver door.", "item_req" : [], "attr_req" : [], "func" : self.Q}])
            return result
    
    def N(self):
        print("You enter what must've been an armoury some time ago. \nThere is a blue door and a green door on two adjacent sides of the room.")
        if "N" in self.player.attrs:
            print("You have been here before, you remember the smell.")
        else:
            print("You hate the smell of this room.")
            self.player.attrs.append("N")
        if "PORK_AVAILABLE" in self.player.attrs:
            print("Theres a nice peice of salty pork on a plate, lying in the corner of the room.")
        while True:
            result = self.action_selection([{"descr" : "Take the pork." , "item_req" : [], "attr_req" : ["PORK_AVAILABLE"], "func" : "1"},{"descr" : "Open the blue door.", "item_req" : [], "attr_req" : [], "func" : self.O},{"descr" : "Open the green door.", "item_req" : [], "attr_req" : [], "func" : self.R}])
            if result == "1":
                self.player.items.append("SALTY PORK")
                self.player.attrs.remove("PORK_AVAILABLE")
                self.player.attrs.append("PORK_TAKEN")
            else:	
                return result

    def O(self):
        print("You enter a tall, wide, hall with a domed ceiling. \nThere are four doors, one red, one mauve, one blue and one yellow.")
        if "O" in self.player.attrs:
            print("You remeber this place from before, but the smell seems to have degraded since then.")
        else:
            print("It smells rather nice for a deserted, rotting dungeon.")
            self.player.attrs.append("O")
        result = self.action_selection([{"descr" : "Open the blue door.", "item_req" : [], "attr_req" : [], "func" : self.N},{"descr" : "Open the red door.", "item_req" : [], "attr_req" : [], "func" : self.K},{"descr" : "Open the mauve door.", "item_req" : [], "attr_req" : [], "func" : self.P},{"descr" : "Open the yellow door.", "item_req" : [], "attr_req" : [], "func" : self.R}])
        return result

    def P(self):
        print("You enter a dingey hallway, one door is mauve, one green and one brown.")
        if "P" in self.player.attrs:
            print("You are getting deja-vu about this room, but then again, at this point are we still even counting the dingey rooms?")
        else:
            print("This room, like all others before, smells mostly awful.")
            self.player.attrs.append("P")
        result = self.action_selection([{"descr" : "Open the brown door.", "item_req" : [], "attr_req" : [], "func" : "1"},{"descr" : "Open the green door.", "item_req" : [], "attr_req" : [], "func" : self.Q},{"descr" : "Open the mauve door.", "item_req" : [], "attr_req" : [], "func" : self.O}])
        if result == "1":
            print("You fallt through the floorboards to your death.")
            self.player.health = 0
            return self.O
        else:
            return result
    def Q(self):
        print("You enter a hallway, with low ceilings, there are 3 doors, green, silver and orange.")
        if "Q" in self.player.attrs:
            print("You've been in this hallway before.")
        else:
            print("It looks like literally every hallway you've seen over the course of this sad, short game.")
            self.player.attrs.append("Q")
        if "DEATH_POTION_AVAILABLE" in self.player.attrs:
            print("There is a deadly concoction on the floor.")
        while True:
            result = self.action_selection([{"descr" : "Pick up the deathy potion", "item_req" : [], "attr_req" : ["DEATH_POTION_AVAILABLE"], "func" : "1"},{"descr" : "Open the green door.", "item_req" : [], "attr_req" : [], "func" : self.P},{"descr" : "Open the orange door with the orange key.", "item_req" : [], "attr_req" : ["ORANGE_KEY_TAKEN"], "func" : self.T},{"descr" : "Open the silver door.", "item_req" : [], "attr_req" : [], "func" : self.M}])
            if result == "1":
                self.player.items.append("POTION OF DEATH")
                self.player.attrs.remove("DEATH_POTION_AVAILABLE")
                self.player.attrs.append("DEATH_POTION_TAKEN")
            else:
                return result
                
    def R(self):
        if not "GHOUL_VANQUISHED" in self.player.attrs:
            ghoul_game = Events(self.player, "GHOUL")
            self.player = ghoul_game.player
            if ghoul_game.completed:
                self.player.attrs.append("GHOUL_VANQUISHED")
            return self.R
        else:
            if "R" in self.player.attrs:
                print("You stumble back and take in the room. Its dark, and smells musty.")
            else:
                print("You enter a dark, musty room.")
                self.player.attrs.append("R")
            print("There are two doors, one green and one yellow.")
            result = self.action_selection([{"descr" : "Open the green door.", "item_req" : [], "attr_req" : [], "func" : self.N},{"descr" : "Open the yellow door.", "item_req" : [], "attr_req" : [], "func" : self.O},{"descr" : "Shiny door with the shiny key.", "item_req" : [], "attr_req" : ["SHINY_KEY_TAKEN"], "func" : self.S}])
            return result

    def S(self):
        print("You step to ward the door, open and observe...")
        sleep(1)
        print("...as the sun climbs over the horizon, and you feel the fresh air...")
        sleep(1)
        print("...you notice a sausage factory dumping its toxic waste only 100 or so metres away.")
        sleep(1)
        print("Cursing the damned sausages, you walk out into freedom at last.")
        return "COMPLETED"
        

    def T(self):
        print("You enter a dark, dank, janitor's cabinet.")
        if "T" in self.player.attrs:
            print("You have been here before.")
        else:
            print("Its too crampt for comfort.")
            self.player.attrs.append("T")
        if "SHINY_KEY_AVAILABLE" in self.player.attrs:
            print("There is a shiny key on a shelf.")
        while True:
            result = self.action_selection([{"descr" : "Take the shiny key.", "item_req" : [], "attr_req" : ["SHINY_KEY_AVAILABLE"], "func" : "1"},{"descr" : "Exit the closet by the orange door.", "item_req" : [], "attr_req" : [], "func" : self.Q}])
            if result == "1":
                self.player.items.append("SHINY KEY")
                self.player.attrs.remove("SHINY_KEY_AVAILABLE")
                self.player.attrs.append("SHINY_KEY_TAKEN")
            else:
                return result
    
mainmenu()

