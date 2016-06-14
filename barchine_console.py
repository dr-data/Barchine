#Diego Bonilla 2016 Bartending machine main hub

#Import the py script which handles logic
import barchine_logic
import sys

#Commands: load,save,verify,list,edit,help,exit

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
    #run verify function
    if (user=='verify'):
        barchine_logic.verify()
    #run console data listing function
    if (user=='list'):
        barchine_logic.print_liquids()
        print ''
        if(barchine_logic.validMenu()==True):
            barchine_logic.print_menu()
    #run edit mode
    if(user=='edit'):
        var = raw_input('edit "ingredient" or "drink"?: ')
        if(var=='drink'):
            while True:
                if(barchine_logic.edit_menu()==True):
                    break
        else:
            while True:
                if(barchine_logic.edit_liquid()==True):
                    break
    #print out list of commands with description
    if (user=='help'):
        print 'load - Load data for ingredients from warehouse.txt'
        print '     - Load data for drinks from menu.txt'
        print 'save - Save drinks menu and ingredients to a file'
        print 'verify - Check for low stock and invalid drink recipes'
        print 'list - List a full ingredients list and menu list with relevant data points'
        print 'edit - Edit entries for both drinks and ingredients'
        print 'help - List all console commands with description'
        print 'exit - Exit and close program'
sys.exit




