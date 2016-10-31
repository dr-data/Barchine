#Diego Bonilla 2016 Bartending machine console script

#Import the py script which handles logic
import barchine_logic
import sys

#create drink recipe ingredients structure
class part(object):
    def __init__(self,name,amount):
        self.name=name
        self.amount=amount

#Commands: load,save,verify,list,edit,add,delete,help,exit

#Launch print out
print 'Barchine::Made by Diego Bonilla, 2016'
print 'type "help" to list all commands'
user = ''
#Main console loop
while(user!='exit'):

    #Display warning for empty data sets
    if(barchine_logic.empty_liquids()==True):
        print '#### NO WAREHOUSE LOADED ####'
    if(barchine_logic.empty_menu()==True):
        print '#### NO MENU LOADED ####'
    
    #get user input
    user = raw_input('')
    
    #run loading function
    if (user=='load'):
        barchine_logic.load_warehouse()
        barchine_logic.load_menu()
        
    #run saving function
    if (user=='save'):
        if(barchine_logic.empty_liquids()==False & barchine_logic.empty_menu()==False):
            if(barchine_logic.saveData()==True):
                print 'Data saved'
        else:
            print '#### MISSING DATA SETS ####'
            
    #Verification call to verify the various aspects of the system data
    if (user=='verify'):
        print'Verifying...'
        print'----------Low Volumes----------'
        barchine_logic.stockLevels()
        print'----------Invalid Menu Choices----------'
        barchine_logic.validMenu()
        print'Data Check'
        print(barchine_logic.dataCheck())
        
    #run console data listing function
    if (user=='list'):
        barchine_logic.console_print_liquids()
        print ''
        #if(barchine_logic.validMenu()==True):
        barchine_logic.console_print_menu()

    #Place an order
    if (user=='order'):
        if(barchine_logic.empty_liquids()==False & barchine_logic.empty_menu()==False):
            order = raw_input('What would you like to order?').strip()
            if(barchine_logic.transmit(order)):
                print 'Drink order successful'
            else:
                print 'Order Failed'
        else:
                print 'No data loaded'
            
    #run edit mode
    if(user=='edit'):
        new_name = 'EMPTY'
        var = raw_input('edit "ingredient" or "drink"?: ').strip()
        if(var=='drink'):
            old_name = raw_input('Enter name of drink to edit: ').strip()
            if(barchine_logic.check_menu(old_name)):
                while(var!='exit'):
                    print'Enter "exit" to leave edit mode'
                    var = raw_input('Enter one of the following to edit: name,recipe: ').strip()
                    if(var=='name'):
                        new_name = raw_input('Enter new name: ').strip()
                    if(var=='recipe'):
                        new_recipe = barchine_logic.get_recipe(old_name)
                        for num in range(len(new_recipe)):
                            var = raw_input('Edit '+str(new_recipe[num].name)+'? (y/n): ').strip()
                            if(var=='y'):
                                var = raw_input("Enter new name: ").strip()
                                new_recipe[num].name = str(var)
                                var = raw_input("Enter new amount (in mL): ").strip()
                                new_recipe[num].amount = int(var)
                #error check empty data
                if(new_name=='EMPTY'):
                    new_name=old_name
                #submit edits to function
                barchine_logic.edit_drink(old_name,new_name,new_recipe)
            else:
                print 'Drink DNE'
        if(var=='ingredient'):
            #some temp variables
            family='EMPTY';name='EMPTY';amount=-1;pos=-1;cost=-1
            old_name = raw_input('Enter name of ingredient to edit: ').strip()
            if(barchine_logic.check_ingredient(old_name)):
                while(var!='exit'):
                    print'Enter "exit" to leave edit mode'
                    var = raw_input('Enter one of the following to edit: family,name,amount,pos,cost: ').strip()
                    if(var=='family'):
                        var = raw_input('Enter new family (mixer or alcohol): ').strip()
                        family = var
                    if(var=='name'):
                        var = raw_input('Enter new name: ').strip()
                        name = var
                    if(var=='amount'):
                        var = raw_input('Enter new amount (in mL): ').strip()
                        amount = int(var)
                    if(var=='pos'):
                        var = raw_input('Enter new pos (Reference machine labelling): ').strip()
                        pos = int(var)
                    if(var=='cost'):
                        var = raw_input('Enter new price (per 25mL): ').strip()
                        cost = float(var)
                #submit edits to function
                barchine_logic.edit_liquid(old_name,family,name,amount,pos,cost)
                
    #run add entry mode
    if(user=='add'):
        var = raw_input('add "ingredient" or "drink"?: ')
#adding a new drink recipe
        if(var=='drink'):
            #Temp variables
            name = 'EMPTY'
            recipe = []
            ingredient = part('EMPTY',0.0)
            #get input for various parameters
            var = raw_input('Enter drink name: ').strip()
            name = var
            var = raw_input('How many ingredients?').strip()
            for num in range(0,int(var)):
                ingre_name = raw_input('Enter name of ingredient: ').strip()
                amount = raw_input('Enter amount of ingredient in mL: ').strip()
                recipe.append(part(ingre_name,int(amount)))
            #send name and recipe to function
            barchine_logic.add_menu(name,recipe)
            print ('Added drink: '+str(name))
            for num in range(len(recipe)):
                print (str(recipe[num].name)+', '+str(recipe[num].amount)+'mL')
#adding a new ingredient
        if(var=='ingredient'):
            #get input for various parameters
            temp_family = raw_input('Enter family of ingredient (alcohol or mixer): ').strip()
            temp_name = raw_input('Enter name of ingredient: ').strip()
            temp_amount = raw_input('Enter amount in storage (mL): ').strip()
            temp_position = raw_input('Enter hardware position of ingredient: ').strip()
            temp_cost = raw_input('Enter cost of drink per 25mL: ').strip()
            #send collected data to function
            barchine_logic.add_ingredient(temp_family,temp_name,temp_amount,temp_position,temp_cost)
            print 'Added ingredient:'
            print 'Type: '+str(temp_family)+', Name: '+str(temp_name)+', Amount: '+str(temp_amount)+'mL, Storage Position: '+str(temp_position)+', Cost: $'+str(temp_cost)

    #run delete entry mode
    if(user=='delete'):
        var = raw_input('delete "ingredient" or "drink"?: ').strip()
        if(var=='drink'):
            var = raw_input('Enter name of menu item to delete: ').strip()
            if(barchine_logic.check_menu(var)):
                check = raw_input('Confirm delete ['+var+'] (y/n): ').strip()
                if(check=='y'):
                        barchine_logic.delete_menu(var)
                        print ('Deleted: '+var)
            else:
                print 'Menu item DNE'
        if(var=='ingredient'):
            var = raw_input('Enter name of ingredient to delete: ').strip()
            if(barchine_logic.check_ingredient(var)):
                check = raw_input('Confirm delete ['+var+'] (y/n): ').strip()
                if(check=='y'):
                        barchine_logic.delete_ingredient(var)
                        print ('Deleted: '+var)
            else:
                print 'Ingredient DNE'
        
    #print out list of commands with description
    if (user=='help'):
        print 'load - Load data for ingredients from warehouse.txt'
        print '     - Load data for drinks from menu.txt'
        print 'save - Save drinks menu and ingredients to a file'
        print 'verify - Check for low stock and invalid drink recipes'
        print 'list - List a full ingredients list and menu list with relevant data points'
        print 'order - Order a drink (Default, sending to Arduino via Serial)'
        print 'edit - Edit entries for both drinks and ingredients'
        print 'add - Add a new drink or ingredient to the system'
        print 'delete - Remove a drink or ingredient from the system'
        print 'help - List all console commands with description'
        print 'exit - Exit and close program'
sys.exit




