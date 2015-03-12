//implementation for BogValidator.h

#include "BogValidator.h"

/* Default constructor 
* Establishes inputs as a Dictionary by inserting "" into it.
*/
BogValidator::BogValidator()
{
    string s = "";
    inputs.insert(s);
}

/* Destructor */
BogValidator::~BogValidator()
{
}

/* 
* Preconditions: empty Dictionary dict exists
* Postconditions: dict is filled with viable words
*/
bool BogValidator::readDict()
{
    return solver.readDict();
}

/* 
* Preconditions: none
* Postconditions: board has been read in and exists within the private
* variable BogSolver solver. 
*/
bool BogValidator::readBoard()
{
    return solver.readBoard();
}

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
void BogValidator::checkWords()
{
    string word = "";
    solver.solve();
    do
    {
        cin >> word;
        word = convertString(word);
        if(isValid(word))
        {
            cout << "OK " << word << endl;
        }
        else
        {
            cout << "NO " << word << endl;
        }
        
    } while(!cin.eof());
}

/* 
* Preconditions: passed string is not an empty string.
* Postconditions: The passed string word is added to the inputs
* dictionary. Function returns whether or not the word was already added
* or not.
*/
bool BogValidator::isValid(string s)
{
    unsigned int size = s.size();
    BogWordList* list = solver.getWords(size);
    for(int i = 0; i < list->numWords; i++)
    {
        if(s == list->words[i].word && !inputs.isWord(s))
        {
            inputs.insert(s);
            return true;
        }
    }
    return false;
}

/* convertString(string s)
* Passed the input for a dictionary, filters out numbers or
* non-alphabetic characters, and converts all char to uppercase.
* Returns: the newly converted to UPPER string
*/
string BogValidator::convertString(string s)
{
    string clean = "";
    unsigned int length = s.size();
    if(s == "") return s; //if empty string is passed, return empty
    for(unsigned int i = 0; i < length; i++)
    {
        if(isalpha(s[i]))
        {
            clean += toupper(s[i]);
        }
    }
    return clean;
}