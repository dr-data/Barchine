//Barchine Arduino Sample Code
//Created by:: Diego Bonilla, 2016

//Sample script for handling serial input from pi for drink order

//Some variables
boolean action = false;
boolean negation=false;
boolean even = false;
int num=0;
//Limit allows for a drink to contain up to specified max ingredients (Go crazy)
static int MAX = 20;
int positions[MAX];
int amounts[MAX];

void setup() {
//Set serial baud rate
  Serial.begin(9600);

//Sample data allows for 6 alcohols and 6 mixers represented by LED's on pins 30-41
  for(int i=30;i<=41;i++){
    pinMode(i,OUTPUT);
  }
//Setting blank values for array data
    for(int i=0;i<MAX;i++){
    positions[i]=0;
    amounts[i]=0;
  }
}

void loop() {
  //If drink order was recieved, send collected data to pouring system
  if(action){
    //Some troubleshooting information
    /*Serial.print("Positions: ");
    for(int i=0;i<MAX;i++)Serial.print(positions[i]);
    Serial.print('\n');
    Serial.print("Amounts: ");
    for(int i=0;i<MAX;i++)Serial.print(amounts[i]);
    Serial.print('\n');*/
    createDrink();
  }
}

//Listen for, and parse incoming serial data
//Incoming data is in format (INGREDIENT_INDEX , POUR_REPETITIONS)
//even variable toggles between index and pour amount to populate respective array
void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
if(inChar!='\n' && inChar!='!' && inChar!='-'){
    if(even){
      amounts[num]=(inChar - '0');
      num++;
      even = false;
      }
    else {
      //Special treatment, store char as its negative value
      if(negation==true)positions[num]=(inChar - '0')*-1;
      else positions[num]=(inChar - '0');
      even = true;
      negation=false;
      }
    }
    //Check if incoming char is a negation symbol, therefore toggle variable for special treatment of next incoming char
else if(inChar=='-'){
  negation=true;
}
//End of order reached (Denoted by '!' symbol), allow order to be processed
else if(inChar=='!'){
  negation=false;
  even=false;
  num=0;
  action=true;
}
  }
}
//NOTE: pin value addition off by one since storage starts from position 1 to allow negative values for mixers
void createDrink() {

//Alcohol will be positive integer, while mixers will be negative
for(int i=0;i<MAX;i++){

//If alcohol is required
if(positions[i]>0){
//Repeat for amount required to make beverage
  for(int r=0;r<amounts[i];r++){
        digitalWrite(positions[i]+29,HIGH);
    delay(1000);
    digitalWrite(positions[i]+29,LOW);
    delay(500);
    }
  }
//If mixer is required
if(positions[i]<0){
//Repeat for amount required to make beverage
    for(int r=0;r<amounts[i];r++){
    digitalWrite((positions[i]*-1)+35,HIGH);
    delay(1000);
    digitalWrite((positions[i]*-1)+35,LOW);
    delay(500);
    }
  } 
}
//Reset drink instruction set
    for(int i=0;i<=19;i++){
    positions[i]=0;
    amounts[i]=0;
  }
//Drink is complete, return to loop
    action = false;
}

