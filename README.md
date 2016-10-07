# Barchine
A python based framework to do all the background computing for a mechanized bartending machine.

###Current Features:
  - Store alcoholic beverages and mixers in a txt
  - Store drink recipes in a txt
  - Alcohol and Mixer data (Type: Alcohol or mixer, Name, Volume, Position ID, Cost per 25mL)
  - Drink data (name, recipe array containing ingredients with name and respective volume for drink recipe)
  - Calculate the cost of each drink recipe
  - Save and load drink recipes and ingredients from txt files
  - Error checking system
   - Check for low stock
   - Check for drinks which are missing or have insufficient ingredients
   - Verify no storage overlap, or naming conflicts
  - Serial communication to arduino for drink order
  - Console navigation
  - Sample Arduino code for raspberry pi to arduino serial communication for Barchine

