# Barchine
A python based framework to do all the background computing for a mechanized bartending machine.

###Current Features:
  - Store alcoholic beverages and mixers in a txt
  - Store drink recipes in a txt
  - Alcohol and Mixer data (Type: Alcohol or mixer, Name, Volume, Position ID, Cost per 25mL)
  - Drink data (name, recipe array containing ingredients with name and respective volume for drink recipe)
  - Calculate the cost of each drink recipe
  - Save and load drink recipes and ingredients from txt files
  - Check for low stock
  - Check for drinks which are missing or have insufficient ingredients
  - Console navigation
  - Add/Delete/Edit menu entries and ingredient entries
  
###Upcoming Features:
  - Error checking system to ensure data read from memory file follows proper logic (no overlapping on storage positions, duplicate names)
  - Create GUI system for end user operation with access to console settings
