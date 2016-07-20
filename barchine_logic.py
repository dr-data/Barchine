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
    
#Check for low stock levels
#return true if all is ok
#--------------------------------FIX FUNCTION-------------------------------------#
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
    if(tally==0):return True
    else:
        return False

#ensure that menu items are valid and can be made with provided liquids
#--------------------------------FIX FUNCTION-------------------------------------#
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

#ensure data structure in memory is valid (no duplicate names, no overlapping storage positions)
def dataCheck():
#find max storage position for each family in memory
    limit_alcohol = 0
    limit_mixer = 0
    for num in range(len(liquids)):
        if(liquids[num].family=='alcohol'):
            if(liquids[num].pos>limit_alcohol):
                limit_alcohol = liquids[num].pos
        if(liquids[num].family=='mixer'):
            if(liquids[num].pos>limit_mixer):
                limit_mixer = liquids[num].pos
    #print ('alcohol max at: '+str(limit_alcohol)+' mixer max at: '+str(limit_mixer))
#organise liquid families based on positions
    alcohol_pos_list = [None]*(limit_alcohol+1)
    mixer_pos_list = [None]*(limit_mixer+1)
    for num in range(len(liquids)):
        if(liquids[num].family=='alcohol'):
            #ensure position is not taken, if it is taken, return error
            if(alcohol_pos_list[liquids[num].pos-1]==None):
                alcohol_pos_list[liquids[num].pos-1]=liquids[num].name
            else:
                print '(alcohol) ERROR SPOT TAKEN AT: '+str(liquids[num].pos)
                print 'Resident Value: '+str(alcohol_pos_list[liquids[num].pos-1])
                print 'Value attempting to be placed'+str(liquids[num].name)
        if(liquids[num].family=='mixer'):
            if(mixer_pos_list[liquids[num].pos-1]==None):
                mixer_pos_list[liquids[num].pos-1]=liquids[num].name
            else:
                print '(mixer) ERROR SPOT TAKEN AT: '+str(liquids[num].pos)
#check for duplicate names in each family
    for num in range(len(alcohol_pos_list)):
        if(alcohol_pos_list.count(alcohol_pos_list[num])>1):
            print '[ERROR] Multiple instances of: '+str(alcohol_pos_list[num])
            return False
    for num in range(len(mixer_pos_list)):
        if(mixer_pos_list.count(mixer_pos_list[num])>1):
            print '[ERROR] Multiple instances of: '+str(mixer_pos_list[num])
            return False
    return True

#confirm if menu item exists
def check_menu(test_name):
    for num in range(len(menu)):
                 if(menu[num].name==test_name):
                     return True
    return False

#confirm if ingredient exists
def check_ingredient(test_name):
    for num in range(len(liquids)):
                 if(liquids[num].name==test_name):
                     return True
    return False

#retrieve level from stock given name
def getLevel(name):
    for num in range(len(liquids)):
        if(liquids[num].name==name):return liquids[num].amount
        
#retrieve cost from stock given name
def getCost(name):
    for num in range(len(liquids)):
        if(liquids[num].name==name):return liquids[num].cost
    return -1

#retrieve recipe
def get_recipe(test_name):
    for num in range(len(menu)):
        if(menu[num].name==test_name):
            return menu[num].recipe

#add a drink to the menu
def add_menu(name,recipe):
    #combine all collected data into drink object
    new_drink = drink(name,recipe)
    menu.append(new_drink)
    
#add an ingredient to the stock
def add_ingredient(temp_family,temp_name,temp_amount,temp_position,temp_cost):
#add data into ingredient structure
    new_ingredient = ingredient(temp_family,temp_name,int(temp_amount),int(temp_position),float(temp_cost))
    liquids.append(new_ingredient)
        
#delete a menu option
def delete_menu(name):
    for num in range(len(menu)):
        if(menu[num].name==name):
                menu.pop(num)
                return
            
#delete an ingredient
def delete_ingredient(name):
    for num in range(len(liquids)):
        if(liquids[num].name==name):
                liquids.pop(num)
                return
                
#Edit a drinks information
def edit_drink(old_name,new_name,new_recipe):
    for num in range(len(menu)):
                 if(menu[num].name==old_name):
                     if(new_name!='EMPTY'):
                         menu[num].name = new_name
                     menu[num].recipe = new_recipe
    
#Edit an ingredients information
def edit_liquid(old_name,family,name,amount,pos,cost):
    for num in range(len(liquids)):
        if(liquids[num].name==old_name):
            if(family!='EMPTY'):
                liquids[num].family=family
            if(name!='EMPTY'):       
                liquids[num].name=name
            if(amount!=-1):
                liquids[num].amount=amount
            if(pos!=-1):
                liquids[num].pos=pos
            if(cost!=-1):
                liquids[num].cost=float(cost)

#calculate the total cost of a drink provided the name
def calcCost(drink):
    total=0
    for num in range(len(drink.recipe)):
        total += getCost(drink.recipe[num].name)*(drink.recipe[num].amount/25)
    return float(total)

#List all data for menu items
def console_print_menu():
    print'-----Menu-----'
    for num in range(len(menu)):
            print ' '
            print(str(menu[num].name))
            print calcCost(menu[num])
            for num2 in range(len(menu[num].recipe)):
                print(str(menu[num].recipe[num2].name)+'::'+str(menu[num].recipe[num2].amount)+'mL')
                
#List all data for stored liquids
def console_print_liquids():
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
