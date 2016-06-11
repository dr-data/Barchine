#Diego Bonilla 2016 Bartending machine framework
import os.path
import sys

#create structure for ingredients
class ingredient(object):
    def __init__(self,family,name,amount,pos,cost):
        self.family=family
        self.name=name
        self.amount=amount
        self.pos=pos
        self.cost=cost
#create structure for drinks
class drink(object):
    def __init__(self,name,recipe):
        self.name=name
        self.recipe=recipe
#create part structure
class part(object):
    def __init__(self,name,amount):
        self.name=name
        self.amount=amount
        
#global variables
liquids = []
menu = []

def start():
    print 'starting up...'
    print 'checking warehouse'
    if os.path.isfile('warehouse.txt'):
        print 'warehouse found'
        f = open('warehouse.txt', 'r')
        print 'generating liquids list'
        for line in f:
            data = line.split('|')
            new = ingredient(data[0],data[1],int(data[2]),int(data[3]),float(data[4]))
            liquids.append(new)
        print 'loaded the following ingredients:'
        for num in range(len(liquids)):
            print str(liquids[num].family)+','+str(liquids[num].name)+','+str(liquids[num].amount)+','+str(liquids[num].pos)+',$'+str(liquids[num].cost)
    else:
        print 'warehouse not found!'
        sys.exit
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
        print 'generating menu'
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
        #print menu[1].recipe[1].amount
        print 'loaded the following menu:'
        for num in range(len(menu)):
            print ' '
            print(str(menu[num].name))
            for num2 in range(len(menu[num].recipe)):
                print(str(menu[num].recipe[num2].name)+','+str(menu[num].recipe[num2].amount))
    else:
        print 'menu not found!'
        sys.exit

def verify():
    print'Verifying...'
    print'----------Low Volumes----------'
    stockLevels()
    print'----------Invalid Menu Choices----------'
    validMenu()
    
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
    if(tally==0):print 'Nothing invalid'
#retrieve level from stock given name
def getLevel(name):
    for num in range(len(liquids)):
        if(liquids[num].name==name):return liquids[num].amount
#retrieve cost from stock given name
def getCost(name):
    for num in range(len(liquids)):
        if(liquids[num].name==name):return liquids[num].cost
#Edit data for liquids and menu using console
def editStockConsole():
    var = raw_input('Edit liquid or drink: ')
    if(var=='liquid'):
        var = raw_input('Please enter item to edit: ')
        for num in range(len(liquids)):
            if(var==liquids[num].name):
                print'You selected: '+str(liquids[num].name)
                print'Enter DONE to exit edit mode OR list to list all data'
                while(var!='DONE'):
                    var = raw_input('Enter one of the following to edit: family,name,amount,pos: ')
                    if(var=='family'):
                        var = raw_input('Enter new family (mix or alcohol): ')
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
                    if(var=='list'):printOutConsole()
    if(var=='drink'):
        var = raw_input('Please enter item to edit: ')
        for num in range(len(menu)):
            if(var==menu[num].name):
                print'You selected: '+str(menu[num].name)
                print'Enter DONE to exit edit mode OR list to list all data'
                while(var!='DONE'):
                    var = raw_input('Enter one of the following to edit: name,recipe: ')
                    if(var=='name'):
                        var = raw_input('Enter new name: ')
                        menu[num].name = var
                    if(var=='recipe'):
                        for num2 in range(len(menu[num].recipe)):
                            var = raw_input('Edit '+str(menu[num].recipe[num2].name)+'? (y/n)');
                            if(var=='y'):
                                var = raw_input("Enter new name: ")
                                menu[num].recipe[num2].name = var
                                var = raw_input("Enter new amount (in mL): ")
                                menu[num].recipe[num2].amount = int(var)
                    if(var=='list'):printOutConsole()
#calculate the total cost of a drink provided the name
def calcCost(drink):
    total=0
    for num in range(len(drink.recipe)):
        total += getCost(drink.recipe[num].name)*(drink.recipe[num].amount/25)
    return 'Cost: $'+str(total)
    
def printOutConsole():
    print'-----Stock-----'
    for num in range(len(liquids)):
            print 'Type: '+str(liquids[num].family)+', Name: '+str(liquids[num].name)+', Amount: '+str(liquids[num].amount)+'mL, Storage Position: '+str(liquids[num].pos)+', Cost: $'+str(liquids[num].cost)
    print'-----Menu-----'
    for num in range(len(menu)):
            print ' '
            print(str(menu[num].name))
            print calcCost(menu[num])
            for num2 in range(len(menu[num].recipe)):
                print(str(menu[num].recipe[num2].name)+'::'+str(menu[num].recipe[num2].amount)+'mL')
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
def testData():
    #test ingredients
    a = ingredient('alcohol','vodka',100,0)
    b = ingredient('mix','orange',20,1)
    c = ingredient('alcohol','gin',350,2)
    d = ingredient('mix','tonic',500,3)
    #--------------------------------------------
    liquids = [a,b,c]
    f = open('warehouse.txt', 'w')
    for num in range(len(liquids)):
            f.write(str(liquids[num].family)+','+str(liquids[num].name)+','+str(liquids[num].amount)+','+str(liquids[num].pos)+'\n')
    f.close()
    #--------------------------------------------
    #test drink 1 (gin and tonic)
    #define ingredients
    q = part('gin',25)
    qq = part('tonic',50)
    x_arr = [q,qq]
    #define drink
    x = drink('gin and tonic',x_arr)
    #test drink 2 (vodka and orange)
    #define ingredients
    w = part('vodka',25)
    ww = part('orange',100)
    y_arr = [w,ww]
    #define drink
    y = drink('vodka and orange',y_arr)
        #test drink 3 (vodka)
    #define ingredients
    v = part('vodka',25)
    z_arr = [v]
    #define drink
    z = drink('vodka',z_arr)
    #--------------------------------------------
    menu = [x,y,z]
    f = open('menu.txt', 'w')
    for num in range(len(menu)):
            f.write(str(menu[num].name)+'\n')
            for num2 in range(len(menu[num].recipe)):
                f.write(str(menu[num].recipe[num2].name)+','+str(menu[num].recipe[num2].amount)+',')
            f.write('\n')
    f.close()
    #--------------------------------------------

#Running protocols
    
start()
verify()
printOutConsole()
saveData()
