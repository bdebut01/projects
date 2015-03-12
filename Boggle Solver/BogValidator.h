
#include "BogSolver.h"

class BogValidator
{
    public:
        /* Default constructor 
        * Establishes inputs as a Dictionary by inserting "" into it.
        */
        BogValidator();
        
        /* Destructor */
        ~BogValidator();
        
        /* 
        * Preconditions: empty Dictionary dict exists
        * Postconditions: dict is filled with viable words
        */
        bool readDict();
        
        /* 
        * Preconditions: none
        * Postconditions: board has been read in and exists within the private
        * variable BogSolver solver. 
        */
        bool readBoard();
        
        /*
        * Preconditions: none
        * Postconditions: board is solved according to the dictionary. Each 
        * inputted word is checked for validity and the corresponding cout 
        * message is outputted. 
        * Note: I'll admit for some reason the checker outputs the last word 
        * inputted three times and I do not know why. The first time around it 
        * does check for validity or not, but the next regardless of whether it 
        * is a word or not (because if it was, it has now been added and is now 
        * invalid) outputs "NO" two more times.
        */
        void checkWords();
        
        /* 
        * Preconditions: passed string is not an empty string.
        * Postconditions: The passed string word is added to the inputs
        * dictionary. Function returns whether or not the word was already added
        * or not.
        */
        bool isValid(string s); //validates one word
        
    private:
        Dictionary dict; //must use a Dictionary
        Dictionary inputs; //inputs dictionary
        BogSolver solver;
        
        /* convertString(string s)
        * Passed the input for a dictionary, filters out numbers or
        * non-alphabetic characters, and converts all char to uppercase.
        * Returns: the newly converted to UPPER string
        */
        string convertString(string s);
};