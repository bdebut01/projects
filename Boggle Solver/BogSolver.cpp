//implementation for BogSolver.h class

#include "BogSolver.h"

////////////////////////////////////////////////////////////////////////////////
////////////////////////////// CONSTRUCTORS/DECONSTRUCTORS /////////////////////
////////////////////////////////////////////////////////////////////////////////

/* 
* Preconditions: None, a BogSolver instance is made
* Postconditions: All private variables of the BogSolver class are
* preset. A "" is inserted into the solutions dictionary so that it 
* exists. Dynamic array board is set to NULL.
*/
BogSolver::BogSolver()
{
    board = NULL;
    totalwordCount = 0;
    ROW = 0;
    COL = 0;
    string s = "";
    solutions.insert(s);
}

//Destructor
BogSolver::~BogSolver()
{
}    

//////////////////////////////////////////////////////////////////////////////
////////////////////// PUBLIC FUNCTIONS //////////////////////////////////////
//////////////////////////////////////////////////////////////////////////////

/* 
* Preconditions: alphabetic strings of words is being funneled into the 
* program. The sentinel telling the function to stop reading in strings
* is a "."
* Postconditions: the private Dictionary dict is filled with "words"
* by way of the Dictionary's public insert function. Additionally, the s is
* converted to all uppercase alphabetic letters via convertString(s).
*/
bool BogSolver::readDict()
{
    string s;
    do 
    {
        cin >> s;
        dict.insert(convertString(s));
    } while(s != ".");
    return true;
}

/* 
* Preconditions: Two ints are funnelled in, (row and column numbers)
* then the matching succession of characters is funnelled in. 
* Postconditions: A 2D dynamic array of ROW height and COL wide is
* created. The array is of type BogLett and each BogLett is given the
* character cinned and has its private variables row and col set. All
* BogLetts are preset to visited = false.
*/
bool BogSolver::readBoard()
{
    int row, col;
    char c;
    cin >> row >> col;
    ROW = row;
    COL = col;
    board = new BogLett*[ROW];
    for(int i = 0; i < ROW; i++)
    {
        board[i] = new BogLett[COL];
        for(int j = 0; j < COL; j++)
        {
            cin >> c;
            board[i][j].c = toupper(c);
            board[i][j].row = i;
            board[i][j].col = j;
            board[i][j].visited = false;
        }
    }
    return true;
}

/*
* Preconditions: readDict and readBoard must have been called so that
* characters exist to manipulate and check.
* Postconditions: Wrapper function
* for completely solving the board, so Dictionary solutions is filled with
* viable solutions found, the wordlist queue is filled with BogWords, and the
* BogWordList Allsolutions is occupied by all found viable words.
* Description: Nested for loops pass each BogLett ("tile") as a possible
* word with that BogLett's character as the first letter. The DFS does a
* recursive search on that first letter passed utilizing a empty BogWord
* that it recurses and adds to.
*/
bool BogSolver::solve()
{
    for(int i = 0; i < ROW; i++)
    {
        for(int j = 0; j < COL; j++)
        {
            BogWord* temp = new BogWord;
            
            DFS(board[i][j], temp);
            resetBools(); //reset the board's 'visited' booleans to false
        }
    }
    constructBogWordList(); //converts wordlist into a BogWordList
    return true;
}

/* 
* Preconditions: none
* Postconditions: none
* Description: it returns the number of words found.
*/
int BogSolver::numWords()
{
    return totalwordCount;
}

/* 
* Preconditions: none
* Postconditions: none
* Description: it returns the number of words found of length len.
* Note: To take of the Qu, it adds the running tally of number of Qs to the 
* number of letters in that word. This will count Qs as "two" letters with
* the 'U'.
* Returns: the number of words of length len.
*/
int BogSolver::numWords(int len)
{
    int count = 0;
    for(int i = 0; i < Allsolutions.numWords; i++)
    {
        if((Allsolutions.words[i].numLetts +
            Allsolutions.words[i].numQs) == len)
        {
            count++;
        }
    }
    return count;
}

/*
* Preconditions: solve() has been run so that Allsolutions exists in
* some form.
* Postconditions: none
* Returns: A BogWordList* that points to a copy of the list found when
* solve is found.
*/
BogWordList* BogSolver::getWords()
{
    if(board == NULL) return NULL;
    BogWordList* temp = new BogWordList;
    temp->words = new BogWord[totalwordCount];
    temp->numWords = Allsolutions.numWords;
    
    for(int i = 0; i < totalwordCount; i++)
    {
        temp->words[i] = Allsolutions.words[i];
    }
    return temp;
}

/*
* Preconditions: solve() has been run so that Allsolutions exists in
* some form.
* Postconditions: none
* Returns: A BogWordList* that points to a copy of the Allsolutions
* list however only words of length len are copied and exist in the
* returned BogWordList*.
*/
BogWordList* BogSolver::getWords(int len)
{
    BogWordList* temp = getWords();
    BogWordList* temp2 = new BogWordList;
    temp2->words = new BogWord[totalwordCount];
    temp2->numWords = 0;
    
    for(int i = 0; i < totalwordCount; i++)
    {
        if((temp->words[i].numLetts +
            temp->words[i].numQs) == len)
        {
            temp2->words[temp2->numWords] = temp->words[i];
            temp2->numWords++;
        }
    }
    return temp2;   
}

/*
* Preconditions: Allsolutions has at least one solution in it.
* Postconditions: none
* Description: prints every BogWord solution found in HBF.
* Ex for just "RAT": 
*       < R 1 2 A 1 1 T 0 1 >
*       < > //signifies end of solutions list.
*/
void BogSolver::printWords()
{
    for(int i = 0; i < Allsolutions.numWords; i++)
    {
        cout << "< ";
        Allsolutions.words[i].printBogWord();
        cout << " >" << endl;
    }
    cout << "< >" << endl;
}

/*
* Preconditions: Allsolutions has at least one solution in it.
* Postconditions: none
* Description: prints every BogWord solution found in HBF of length len.
* Ex for command of lengths "3", just "RAT": 
*       < R 1 2 A 1 1 T 0 1 >
*       < > //signifies end of solutions list.
*/
void BogSolver::printWords(int len)
{
    BogWordList* temp = getWords(len);
    for(int i = 0; i < temp->numWords; i++)
    {
        cout << "< ";
        temp->words[i].printBogWord();
        cout << " >" << endl;
    }
    cout << "< >" << endl;
}

/*
* Preconditions: none.
* Postconditions: none.
* Description: Prints all solution words without coordinates separated
* by end of lines.
*/
void BogSolver::listWords()
{
    for(int i = 0; i < Allsolutions.numWords; i++)
    {
        cout << Allsolutions.words[i].word << endl;
    }
}

/* 
* Preconditions: none.
* Postconditions: none.
* Description: Prints all solutions of length len without coordinates
* separated by end of lines.
*/
void BogSolver::listWords(int len)
{
    BogWordList* temp = getWords(len);
    for(int i = 0; i < temp->numWords; i++)
    {
        cout << temp->words[i].word << endl;
    }
}
            

////////////////////////////////////////////////////////////////////////////////
////////////////////// PRIVATE FUNCTIONS ///////////////////////////////////////
////////////////////////////////////////////////////////////////////////////////

/*
* Preconditions: passed a bog board BogLett with a character and 
* position. Temp is a empty BogWord that is updated as the DFS recurses
* and increments/decrements attempts.
* Postconditions: recordSolution is called and given actual BogWords to 
* record. In this manner, the recording structures, Allsolutions and 
* wordlist queue are fed viable words and filled. 
* Notes: The nested for loop and if statements all work together to essentially
* posit that the only BogLetts that are recursed on are neighbors and not the
* BogLett currently getting evaluated. 
*/
void BogSolver::DFS(BogLett tile, BogWord* temp)
{
    board[tile.row][tile.col].visited = true;
    temp->updateWord(tile);
    if(temp->numLetts > 2 && dict.isWord(temp->word))
    {
        recordSolution(*temp);
    }

    for(int i = tile.row - 1; i <= tile.row + 1; i++)
    {
        for(int j = tile.col - 1; j <= tile.col + 1; j++)
        {
            if(i >= 0 && i < ROW && j >= 0 && j < COL) //stay within dimensions
            {
                if(!board[i][j].visited)
                {
                    if(dict.isPrefix(temp->word + board[i][j].c))
                    {
                        DFS(board[i][j], temp);
                    }
                }
            }
        }
    }
    temp->decrement();
    board[tile.row][tile.col].visited = false;
}

/* 
* Preconditions: board exists of dimensions ROW and COL
* Postconditions: All BogLetts' visited booleans are false.
* Description: loops through board and sets all visit booleans to false.
*/
void BogSolver::resetBools()
{
    for(int i = 0; i < ROW; i++)
    {
        for(int j = 0; j < COL; j++)
        {
            board[i][j].visited = false;
        }
    }
}

/*
* Preconditions: passed a BogWord with a string word set within it.
* Postconditions: If the word isn't already in the solution dictionary,
* then the BogWord is added to it, and pushed onto to the queue of found
* solutions. Private class variable, totalwordCount is also incremented.
*/
void BogSolver::recordSolution(BogWord word)
{
    string completeword = word.word;
    if(!solutions.isWord(completeword)) //if word isn't already found
    {
        solutions.insert(completeword); //add to string list of solutions (dict)
        wordlist.push(word); //push BogWord onto solution queue
        totalwordCount++;
    } return;
}

/* 
* Precondition: Allsolutions private BogWordList in a BogSolver points to NULL,
* and doesn't really exist. wordlist queue is inhabited by BogWords.
* Postcondition: Allsolutions has been created number of words found large, and
* is filled with BogWord solutions.
*/
void BogSolver::constructBogWordList()
{
    Allsolutions.numWords = totalwordCount;
    Allsolutions.words = new BogWord[totalwordCount];
    for(int i = 0; i < totalwordCount; i++) //tranfer over all solutions in Q
    {
        Allsolutions.words[i] = wordlist.front();
        wordlist.pop();
    }
    return;
}

/* convertString(string s)
* Passed the input for a dictionary, filters out numbers or
* non-alphabetic characters, and converts all char to uppercase.
* Returns: the newly converted to UPPER string
*/
string BogSolver::convertString(string s)
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