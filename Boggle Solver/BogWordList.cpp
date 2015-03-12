//implementation for struct functions defined in BogWordList.h

#include "BogWordList.h"

//////////////////////////////////// BOGLETT ///////////////////////////////////
/*
* Overloaded constructor that presets character c to the passed letter
* and the position row and col to the passed ints.
*/
BogLett::BogLett(char c, int row, int col)
{
    c = c;
    row = row;
    col = col;
    visited = false;
}

/* Default constructor */
BogLett::BogLett()
{
    visited = false;
    row = 0;
    col = 0;
}

////////////////////////////////// BOGWORD /////////////////////////////////////

/* Default constructor */
/* Creates an array of BogLetts INIT_LETTSIZE large. */
BogWord::BogWord()
{
    numLetts = 0;
    word = "";
    numQs = 0;
    letts = new BogLett[INIT_LETTSIZE];
    currentCapacity = INIT_LETTSIZE;
}

/* Copy constructor */
BogWord::BogWord(const BogWord &w)
{
    word = w.word;
    numLetts = w.numLetts;
    numQs = w.numQs;
    currentCapacity = w.currentCapacity;
    letts = new BogLett[currentCapacity];
    for(int i = 0; i < numLetts; i++)
    {
       letts[i] = w.letts[i];
    }
}

/* Assignment operator */
/* Overwrites the BogWord "=" sign to allow setting BogWords equal to other 
* BogWords. Describes how the array of BogLetts are transferred. 
*/
BogWord& BogWord::operator=(const BogWord &w)
{
    if(this != &w)
    {
        word = w.word;
        numLetts = w.numLetts;
        numQs = w.numQs;
        currentCapacity = w.currentCapacity;
        for(int i = 0; i < numLetts; i++)
        {
            letts[i] = w.letts[i];
        }
    }
    return* this;
}

/*
* Preconditions: passed tile has an array of BogLetts and other variable 
* quantities.
* Postconditions: If the array of BogLetts needed expanding, it is expanded
* by MULTIPLIER. The last empty index in the array of BogLetts is given the
* passed BogLett. Number of letts is incremented, and if the passed BogLett
* was a 'Q', then the numQs variable is incremented. The for loop updates
* the private word string to reflect the changes in its array of BogLetts.
*/
void BogWord::updateWord(BogLett tile)
{
    if(currentCapacity <= numLetts)
    {
        expandLetts();
    }
    letts[numLetts] = tile;
    numLetts++;
    word = "";
    if(tile.c == 'Q') numQs++;
    
    for(int i = 0; i < numLetts; i++)
    {
        word += letts[i].c;
        if(letts[i].c == 'Q')
        {
            word += 'U';
        }
    }
}

/*
* Preconditions: passed tile has an array of BogLetts and other occupied
* variable quantities.
* Postconditions: The number of letts in the array is decremented by one,
* and if the letter was a Q, the numQs is also decremented. The word is 
* rebuilt according to these word length changes, again taking into account
* the possible QU.
*/
void BogWord::decrement()
{
    numLetts--;
    if(word[numLetts] == 'Q')
    {
        numQs--;
    }
    word = "";
    for(int i = 0; i < numLetts; i++)
    {
        word += letts[i].c;
        if(letts[i].c == 'Q')
        {
            word += 'U';
        }
    }
}

/* 
* Precondition: A BogWord's array of letts is to capacity. Need to expand array.
* Postcondition: the array of letts is increased by a factor of MULTIPLIER, and 
* the currentCapacity is similarly updated.
*/
bool BogWord::expandLetts()
{
    BogLett* temp = new BogLett[currentCapacity*MULTIPLIER];
    if(temp == NULL) return false;
    
    for(int i = 0; i < currentCapacity; i++)
    {
        temp[i] = letts[i];
    }
    delete[] letts;
    letts = temp;
    currentCapacity *= MULTIPLIER;
    return true;
}

/* 
* Precondition: none
* Postcondition: couts the BogWord in HBF
*/
void BogWord::printBogWord()
{
    for(int i = 0; i < numLetts; i++)
    {
        cout << letts[i].c;
        if(letts[i].c == 'Q')
        {
            cout << 'U';
        }
        cout << " " << letts[i].row << " ";
        cout << letts[i].col << " ";
    }
}



BogWord::~BogWord()
{
    delete[] letts;
}