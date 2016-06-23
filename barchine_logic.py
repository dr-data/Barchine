#Diego Bonilla 2016 Bartending machine logic
import os.path
import sys

#create structure for ingredients
# Family (Alcohol or Mixer), Name of ingredient, Amount in system, Positioning based on hardware setup, Cost per 25mL
#Structure in save file:
#alcohol|bourbon|750|0|1.57
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

#add a drink to the menu
def add_menu():
    #Temp variables
    name = 'EMPTY'
    recipe = []
    ingredient = part('EMPTY',0.0)
    #get input for various parameters
    var = raw_input('Enter drink name: ')
    name = var
    var = raw_input('How many ingredients?')
    for num in range(0,int(var)):
        ingre_name = raw_input('Enter name of ingredient: ')
        amount = raw_input('Enter amount of ingredient in mL: ')
        recipe.append(part(ingre_name,int(amount)))
    #combine all collected data into drink object
    new_drink = drink(name,recipe)
    print ('Added drink: '+str(new_drink.name))
    for num in range(len(recipe)):
        print (str(new_drink.recipe[num].name)+', '+str(new_drink.recipe[num].amount)+'mL')
    menu.append(new_drink)
    
#add an ingredient to the stock
def add_ingredient():
    #get input for various parameters
    temp_family = raw_input('Enter family of drink (alcohol or mixer): ')
    temp_name = raw_input('Enter name of drink: ')
    temp_amount = raw_input('Enter amount in storage (mL): ')
    temp_position = raw_input('Enter hardware position of ingredient: ')
    temp_cost = raw_input('Enter cost of drink per 25mL: ')
    new_ingredient = ingredient(temp_family,temp_name,int(temp_amount),int(temp_position),float(temp_cost))
    liquids.append(new_ingredient)
    print 'Added ingredient:'
    print 'Type: '+str(new_ingredient.family)+', Name: '+str(new_ingredient.name)+', Amount: '+str(new_ingredient.amount)+'mL, Storage Position: '+str(new_ingredient.pos)+', Cost: $'+str(new_ingredient.cost)

#delete a menu option
def delete_menu():
    var = raw_input('Enter name of menu item to delete: ')
    for num in range(len(menu)):
        if(menu[num].name==var):
            check = raw_input('Confirm delete ['+menu[num].name+'] (y/n): ')
            if(check=='y'):
                menu.pop(num)
                return

#delete an ingredient
def delete_ingredient():
    var = raw_input('Enter name of ingredient to delete: ')
    for num in range(len(liquids)):
        if(liquids[num].name==var):
            check = raw_input('Confirm delete ['+liquids[num].name+'] (y/n): ')
            if(check=='y'):
                liquids.pop(num)
                return
                
#Edit a drinks information
def edit_drink():
    found = False
    print 'EDIT MODE : Type "exit" to leave at any time'
    var = raw_input('Enter name of drink to edit: ')
    if(var=='exit'):
        return True
    for num in range(len(menu)):
            if(var==menu[num].name):
                found = True
                print'You selected: '+str(menu[num].name)
                print'Enter "exit" to leave edit mode'
                while(var!='exit'):
                    var = raw_input('Enter one of the following to edit: name,recipe: ')
                    if(var=='name'):
                        var = raw_input('Enter new name: ')
                        menu[num].name = var
                    if(var=='recipe'):
                        for num2 in range(len(menu[num].recipe)):
                            var = raw_input('Edit '+str(menu[num].recipe[num2].name)+'? (y/n): ');
                            if(var=='y'):
                                var = raw_input("Enter new name: ")
                                menu[num].recipe[num2].name = var
                                var = raw_input("Enter new amount (in mL): ")
                                menu[num].recipe[num2].amount = int(var)
    if(found==False):
        print 'Ingredient DNE'
        return False
    
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
                print'Enter "exit" to leave edit mode'
                while(var!='exit'):
                    var = raw_input('Enter one of the following to edit: family,name,amount,pos,cost: ')
                    if(var=='family'):
                        var = raw_input('Enter new family (mixer or alcohol): ')
                        liquids[num].family = var
                    if(var=='name'):
                        var = raw_input('Enter new name: ')
                        liquids[num].name = var
                    if(var=='amount'):
                        var = raw_input('Enter new amount (in mL): ')
                        liquids[num].amount = int(var)
                    if(var=='pos'):
                        var = raw_input('Enter new pos (Reference machine labelling): ')
                        liquids[num].pos = int(var)
                    if(var=='cost'):
                        var = raw_input('Enter new price (per 25mL): ')
                        liquids[num].cost = float(var)
    if(found==False):
        print 'Ingredient DNE'
        return False

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
