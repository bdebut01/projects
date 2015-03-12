//definition of the BogWordList 

#include <iostream>
#include <queue>
using namespace std;

const int INIT_LETTSIZE = 12;
const int MULTIPLIER = 2;

struct BogLett // a tile
{
    /*
    * Overloaded constructor that presets character c to the passed letter
    * and the position row and col to the passed ints.
    */
    BogLett(char c, int row, int col);
    
    /* Default constructor */
    BogLett();
    
    char c;
    int row, col;
    bool visited;
};

struct BogWord 
{
    /* Default constructor that creates an array of BogLetts INIT_LETTSIZE big*/
    BogWord();
    
    /* Copy constructor */
    BogWord(const BogWord &w);
    
    /* Assignment operator */
    BogWord& operator=(const BogWord &w); //assignment operator
    
    /*
    * Preconditions: passed tile has an array of BogLetts and other variable 
    * quantities.
    * Postconditions: If the array of BogLetts needed expanding, it is expanded
    * by MULTIPLIER. The last empty index in the array of BogLetts is given the
    * passed BogLett. Number of letts is incremented, and if the passed BogLett
    * was a 'Q', then the numQs variable is incremented. The for loop updates
    * the private word string to reflect the changes in its array of BogLetts.
    */
    void updateWord(BogLett tile);
    
    /*
    * Preconditions: passed tile has an array of BogLetts and other occupied
    * variable quantities.
    * Postconditions: The number of letts in the array is decremented by one,
    * and if the letter was a Q, the numQs is also decremented. The word is 
    * rebuilt according to these word length changes, again taking into account
    * the possible QU.
    */  
    void decrement();
    
    /*
    * Precondition: A BogWord's array of letts is to capacity. Need to expand
    * array.
    * Postcondition: the array of letts is increased by a factor of MULTIPLIER,
    * and the currentCapacity is similarly updated.
    */
    bool expandLetts(); //expand dynamic array of letts
    
    /* 
    * Precondition: none
    * Postcondition: couts the BogWord in HBF
    */
    void printBogWord();
           
    string word;
    int numLetts;
    int numQs;
    int currentCapacity;
    BogLett* letts;//points to dynamic array of letters (BogLetts)
 
    ~BogWord(); //destructor
};

struct BogWordList
{
    int numWords;
    BogWord* words;
};