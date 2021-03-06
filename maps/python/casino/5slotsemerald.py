#SlotMachine configuration file
#to make a new kind of slot machine, copy this file, change the settings and point the slotmachine to the new file.
#5 Reel Emerald Slots
#FYI - This one uses an object for cointype and not the money code :)

import Crossfire
import CFGamble
import CFItemBroker

activator=Crossfire.WhoIsActivator()
activatorname=activator.Name
whoami=Crossfire.WhoAmI()
#gets slot name and adds map name for unique jackpot
slotname= '%s#%s' %(whoami.Name,whoami.Map.Path)
x=activator.X
y=activator.Y

cointype = "emerald" #What type of coin is this slotmachine using?
minpot = 5000 #Minimum slot jackpot size
maxpot = 10000 #Maxiumum slot jackpot size
cost = 10 #Price of usage

#Change the items on the slot spinner or the number of items.
slotlist = ["pearl", "pearl", "pearl", "pearl", "pearl", "pearl", "pearl", "mithril", "mithril", "mithril", "mithril", "mithril", "mithril", "Diamond", "Diamond", "Diamond", "Diamond", "Diamond", "RubY", "RubY", "RubY", "RubY", "SaPphIrE", "SaPphIrE", "SaPphIrE", "AmETHYsT", "AmETHYsT", "EMERALD"]

spinners = 5 #How many spinners on the slotmachine?

Slots=CFGamble.SlotMachine(slotname,slotlist,minpot,maxpot)

object = activator.CheckInventory(cointype)
if (object):
    pay = CFItemBroker.Item(object).subtract(cost)
    if (pay):
       Slots.placebet(cost)
       results = Slots.spin(spinners)
       pay = 0
       pot = Slots.checkslot()
       activator.Write('%s' %results, 7)
       for item in results:
          #match all but two - pays out by coin e.g 3 to 1 or 4 to 1
          if results.count(item) == 3:
             if item == "pearl":
                pay = 1
             elif item == "mithril":
                pay = 2
             elif item == "Diamond":
                pay = 3
             elif item == "RubY":
                pay = 4
             elif item == "SaPphIrE":
                pay = 5
             elif item == "AmETHYsT":
                pay = 6
             elif item == "EMERALD":
                pay = 10
             else:
                break
             activator.Write("%d %ss, a minor win!" %(3,item))
             payoff = cost*pay
             Slots.payoff(payoff)
             id = activator.Map.CreateObject(cointype, x, y)
             CFItemBroker.Item(id).add(payoff)
             if payoff == 1:
                message = "you win %d %s!" %(payoff,cointype)
             else:
                message = "You win %d %ss!!" %(payoff,cointype)
             break
          elif results.count(item) == spinners:
             #all match - pays out as percent of pot
             activator.Write('%d %ss, a Major win!' %(spinners,item))
	     if item == "pearl":
                pay = .15
             elif item == "mithril":
                pay = .25
             elif item == "Diamond":
                pay = .3
             elif item == "RubY":
                pay = .4
             elif item == "SaPphIrE":
                pay = .5
             elif item == "AmETHYsT":
                pay = .6
             elif item == "EMERALD":
                pay = 1
             payoff = pot*pay
             Slots.payoff(payoff)
             id = activator.Map.CreateObject(cointype, x, y)
             CFItemBroker.Item(id).add(payoff)
             if payoff == 1:
                message = "you win %d %s!" %(payoff,cointype)
             else:
                message = "You win %d %ss!!" %(payoff,cointype)
             break
          else:
             message = "Better luck next time!"
       activator.Write(message)
       activator.Write("%d in the Jackpot, Play again?" %Slots.checkslot())
    else:
       activator.Write("Sorry, you do not have enough %ss" %(cointype))
else:
   activator.Write("Sorry, you do not have any %ss" %(cointype))
