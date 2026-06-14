#World Cup Simulator
import random
print("Welcome to the World Cup Simulator! 🎉🏆⚽")

morale = 50
strength = 50
injuries = 0

#Group Stages
group_win = 0
group_loss = 0

frequency = 0

#Pre-tournament preparation
print("\n")
print("Pre-tournament preparation...")

while frequency < 3:
    choice = int(input("Choose the pre-tournament preparation activity (1: Training, 2: Friendly Matches, 3: Recovery): "))
    match choice:
        case 1:
            morale += 10
            strength += 15
            injuries += 2
            frequency += 1
        
        case 2:
            morale += 15
            strength += 10
            injuries += 4
            frequency += 1
        
        case 3:
            morale += 5
            strength += 7
            injuries -= 3
            
            if injuries < 0:
                injuries = 0
            frequency += 1
            
        case 4:
            #Buying better players?
            pass
        
        case _:
            print("Invalid choice! Please selcet a valid option")
            
    
    
print("------Teams stats------")
print(f"Morale: {morale}")
print(f"Strength: {strength}")
print(f"Injuries: {injuries}")

#Group Stage Matches (3)
print("\n")
print("Beginning the Group stage Matches...")

for match in range(1,4):
    print(f"Match {match}")
    
    if injuries > 5:
        print("Too many players injured. Forfeit the match")
        group_loss += 1
        continue
    
    if strength > 70 and morale > 70:
        print(f"Your team wins match {match}!🎊🎊")
        group_win += 1
    else:
        print(f"Your team loses match {match}")
        group_loss += 1
        
    if group_win == 0:
        print("Your team has been eliminated from the Group Stage")
        break


#KnockOut Stage
knockout_stages = [
    "Round of 16",
    "Quarter-final", 
    "Semi-final",
    "Final"
] 

if group_win >= 2:
    print("\n")
    print("Beginning the Knockout Stage...")
    
    still_in_tournament = True
    
    for stage in knockout_stages:
        if not still_in_tournament:
            break
        
        print(f"\n Playing {stage}...")
        match_outcome = random.choice(['W', 'L'])
        
        if match_outcome == "L":
            still_in_tournament = False
            
            if stage == "Final":
                print("You lost the World Cup ☹️. Try again next time")
            else:
                print(f"You dropped out of the tournament at the {stage} stage")
                
        else:
            if stage == "Final":
                print("You won the World Cup🥳! You are the Champions🎶🎵 ")
            else:
                print("Victory! You advanced to the next stage")
                
            
else:
    print("\nFailed to qualify passed the group stage")


        
    