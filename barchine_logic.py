#Diego Bonilla 2016 Bartending machine logic
import os.path
import sys

#create structure for ingredients
# Family (Alcohol or Mixer), Name of ingredient, Amount in system, Positioning based on hardware setup, Cost per 25mL
#Structure in save file:
#   alcohol|bourbon|750|0|1.57
class ingredient(object):
    def __init__(self,family,name,amount,pos,cost):
        self.family=family
        self.name=name
        self.amount=amount
        self.pos=pos
        self.cost=cost
        
#create structure for drinks
#Name of drink, array of drink ingredients (See next structure)
#Structure in save file (2 lines for 1 drink):
#gin and tonic
#gin|50|tonic|100
class drink(object):
    def __init__(self,name,recipe):
        self.name=name
        self.recipe=recipe
        
#create drink recipe ingredients structure
#Name of ingredient, Amount designated by drink (mL)
class part(object):
    def __init__(self,name,amount):
        self.name=name
        self.amount=amount
        
#global variables to store ingredients list and menu list
liquids = []
menu = []

#load data from warehouse save file
def load_warehouse():
    print 'checking warehouse'
    if os.path.isfile('warehouse.txt'):
        print 'warehouse found'
        f = open('warehouse.txt', 'r')
        print 'generating liquids list'
        for line in f:
            data = line.split('|')
            new = ingredient(data[0],data[1],int(data[2]),int(data[3]),float(data[4]))
            liquids.append(new)
    else:
        print 'warehouse not found!'
        sys.exit

#load data from menu save file
def load_menu():
    print 'checking menu'
    if os.path.isfile('menu.txt'):
        print 'menu found'
        #get total lines
        num_lines=0
        with open('menu.txt') as infp:
            for line in infp:
               if line.strip():
                  num_lines += 1
        f = open('menu.txt', 'r')
        print 'generating menu list'
        for num in range(0,num_lines/2):
            recipe = []
            title = f.readline().rstrip('\n')
            #print 'adding '+title
            line = f.readline()
            data = line.split('|')
            #print data
            for num2 in range(0,len(data)-1,2):
                recipe.append(part(data[num2],int(data[num2+1])))
                #print data[num2]+' '+data[num2+1]
            menu.append(drink(title,recipe))
    else:
        print 'menu not found!'
        sys.exit

#Verification call to verify the various aspects of the system data
def verify():
    print'Verifying...'
    print'----------Low Volumes----------'
    stockLevels()
    print'----------Invalid Menu Choices----------'
    if(validMenu()):
        print 'None invalid'
    
#Check for low stock levels
def stockLevels():
    tally = 0
    for num in range(len(liquids)):
        if(liquids[num].family=='alcohol'):
            if(liquids[num].amount<=75):
                print str(liquids[num].name)+' '+str(liquids[num].amount)+'ml'
                tally+=1
        else:
            if(liquids[num].amount<=200):
                print str(liquids[num].name)+' '+str(liquids[num].amount)+'ml'
                tally+=1
    if(tally==0):print 'None Low'

#ensure that menu items are valid and can be made with provided liquids
def validMenu():
    tally = 0
    for num in range(len(menu)):
        for num2 in range(len(menu[num].recipe)):
            if(getLevel(menu[num].recipe[num2].name)<menu[num].recipe[num2].amount):
                print str(menu[num].name)+' is missing '+str(menu[num].recipe[num2].name)
                tally+=1
    if(tally==0):
        return True
    else:
        return False
    
#retrieve level from stock given name
def getLevel(name):
    for num in range(len(liquids)):
        if(liquids[num].name==name):return liquids[num].amount
        
#retrieve cost from stock given name
def getCost(name):
    for num in range(len(liquids)):
        if(liquids[num].name==name):return liquids[num].cost

#Edit a drinks information
def edit_drink():
    found = False
    temp_obj = menu[0]
    backup_index = 0
    print 'EDIT MODE : Type "exit" to leave at any time'
    var = raw_input('Enter name of drink to edit: ')
    if(var=='exit'):
        return True
    for num in range(len(menu)):
            if(var==menu[num].name):
                found = True
                print'You selected: '+str(menu[num].name)
                #Create temporary object and backup index
                tmp_obj = menu[num]
                backup_index = num
                print'Enter "exit" to leave edit mode'
                while(var!='exit'):
                    var = raw_input('Enter one of the following to edit: name,recipe: ')
                    if(var=='name'):
                        var = raw_input('Enter new name: ')
                        tmp_obj.name = var
                    if(var=='recipe'):
                        for num2 in range(len(menu[num].recipe)):
                            var = raw_input('Edit '+str(menu[num].recipe[num2].name)+'? (y/n): ');
                            if(var=='y'):
                                var = raw_input("Enter new name: ")
                                tmp_obj.recipe[num2].name = var
                                var = raw_input("Enter new amount (in mL): ")
                                tmp_obj.recipe[num2].amount = int(var)
    if(found==False):
        print 'Ingredient DNE'
        return False
    var = raw_input('Save changes? (y/n): ')
    if(var=='y'):
        print 'Saving changes...'
        menu[backup_index].name = tmp_obj.name
        menu[backup_index].recipe = tmp_obj.recipe
        saveData()
        return True
    else:
        print 'TEMP NAME'+str(temp_obj.name)
        print 'REAL NAME'+str(menu[backup_index].name)
        return True
    
#Edit an ingredients information
def edit_liquid():
    found = False
    print 'EDIT MODE : Type "exit" to leave at any time'
    var = raw_input('Enter name of ingredient: ')
    if(var=='exit'):
        return True
    for num in range(len(liquids)):
            if(var==liquids[num].name):
                found = True
                print'You selected: '+str(liquids[num].name)
                #Create temporary obj and backup index
                tmp_obj = liquids[num]
                backup_index = num
                print'Enter "exit" to leave edit mode'
                while(var!='exit'):
                    var = raw_input('Enter one of the following to edit: family,name,amount,pos,cost: ')
                    if(var=='family'):
                        var = raw_input('Enter new family (mixer or alcohol): ')
                        tmp_obj.family = var
                    if(var=='name'):
                        var = raw_input('Enter new name: ')
                        tmp_obj.name = var
                    if(var=='amount'):
                        var = raw_input('Enter new amount (in mL): ')
                        tmp_obj.amount = int(var)
                    if(var=='pos'):
                        var = raw_input('Enter new pos (Reference machine labelling): ')
                        tmp_obj.pos = int(var)
                    if(var=='cost'):
                        var = raw_input('Enter new price (per 25mL): ')
                        tmp_obj.cost = float(var)
    if(found==False):
        print 'Ingredient DNE'
        return False
    var = raw_input('Save changes? (y/n): ')
    if(var=='y'):
        liquids[backup_index].family = tmp_obj.family
        liquids[backup_index].name = tmp_obj.name
        liquids[backup_index].amount = tmp_obj.amount
        liquids[backup_index].pos = tmp_obj.pos
        liquids[backup_index].cost = tmp_obj.cost
        saveData()
        return True
    else:
        return True

#calculate the total cost of a drink provided the name
def calcCost(drink):
    total=0
    for num in range(len(drink.recipe)):
        total += getCost(drink.recipe[num].name)*(drink.recipe[num].amount/25)
    return 'Cost: $'+str(total)

#List all data for menu items
def print_menu():
    print'-----Menu-----'
    for num in range(len(menu)):
            print ' '
            print(str(menu[num].name))
            print calcCost(menu[num])
            for num2 in range(len(menu[num].recipe)):
                print(str(menu[num].recipe[num2].name)+'::'+str(menu[num].recipe[num2].amount)+'mL')
                
#List all data for stored liquids
def print_liquids():
    print'-----Stock-----'
    for num in range(len(liquids)):
            print 'Type: '+str(liquids[num].family)+', Name: '+str(liquids[num].name)+', Amount: '+str(liquids[num].amount)+'mL, Storage Position: '+str(liquids[num].pos)+', Cost: $'+str(liquids[num].cost)
            
#Save all the ingredients information and menu information to the appropriate files
def saveData():
    f = open('warehouse.txt', 'w')
    for num in range(len(liquids)):
            f.write(str(liquids[num].family)+'|'+str(liquids[num].name)+'|'+str(liquids[num].amount)+'|'+str(liquids[num].pos)+'|'+str(liquids[num].cost)+'\n')
    f.close()
    f = open('menu.txt', 'w')
    for num in range(len(menu)):
        f.write(str(menu[num].name)+'\n')
        for num2 in range(len(menu[num].recipe)):
            f.write(str(menu[num].recipe[num2].name)+'|'+str(menu[num].recipe[num2].amount)+'|')
        f.write('\n')
    f.close()
    return True

#Check for empty liquids list
def empty_liquids():
    if(len(liquids)==0):
        return True
    else:
        return False

#Check for empty menu list
def empty_menu():
    if(len(menu)==0):
        return True
    else:
        return False
