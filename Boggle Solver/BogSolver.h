//class definition for the primary Solver

#include "BogWordList.h"
#include "dictionary.h"

/* Two 2D arrays, one of the boggle board, the other a bool array? */

class BogSolver
{
    public:
        /* 
        * Preconditions: None, a BogSolver instance is made
        * Postconditions: All private variables of the BogSolver class are
        * preset. A "" is inserted into the solutions dictionary so that it 
        * exists. Dynamic array board is set to NULL.
        */
        BogSolver();
        /* Destructor, doesn't do anything. Nothing to delete. */
        ~BogSolver();
        
        /* 
        * Preconditions: alphabetic strings of words is being funneled into the 
        * program. The sentinel telling the function to stop reading in strings
        * is a "."
        * Postconditions: the private Dictionary dict is filled with "words" by
        * way of the Dictionary's public insert function.
        */
        bool readDict();
        
        /* 
        * Preconditions: Two ints are funnelled in, (row and column numbers)
        * then the matching succession of characters is funnelled in. 
        * Postconditions: A 2D dynamic array of ROW height and COL wide is
        * created. The array is of type BogLett and each BogLett is given the
        * character cinned and has its private variables row and col set. All
        * BogLetts are preset to visited = false.
        */
        bool readBoard();
        
        /*
        * Preconditions: readDict and readBoard must have been called so that
        * characters exist to manipulate and check.
        * Postconditions: Wrapper function for completely solving the board, so 
        * Dictionary solutions is filled with viable solutions found, the 
        * wordlist queue is filled with BogWords, and the BogWordList
        * Allsolutions is occupied by all found viable words.
        * Description: Nested for loops pass each BogLett ("tile") as a possible
        * word with that BogLett's character as the first letter. The DFS does a
        * recursive search on that first letter passed utilizing a empty BogWord
        * that it recurses and adds to.
        */
        bool solve(); //search board for words in dict
        
        /* 
        * Preconditions: none
        * Postconditions: none
        * Description: it returns the number of words found.
        */
        int numWords();
        
        /* 
        * Preconditions: none
        * Postconditions: none
        * Description: it returns the number of words found of length len.
        * Note: To take of the Qu, it adds the running tally of number of Qs to
        * the number of letters in that word. This will count Qs as "two"
        * letters with the 'U'.
        */
        int numWords(int len); //number of words of length len
        
        /*
        * Preconditions: solve() has been run so that Allsolutions exists in
        * some form.
        * Postconditions: none
        * Returns: A BogWordList* that points to a copy of the list found when
        * solve is found.
        */
        BogWordList* getWords();
        
        /*
        * Preconditions: solve() has been run so that Allsolutions exists in
        * some form.
        * Postconditions: none
        * Returns: A BogWordList* that points to a copy of the Allsolutions
        * list however only words of length len are copied and exist in the
        * returned BogWordList*.
        */
        BogWordList* getWords(int len);
        
        /*
        * Preconditions: none
        * Postconditions: none
        * Description: prints every BogWord solution found in HBF.
        * Ex for just "RAT": 
        *       < R 1 2 A 1 1 T 0 1 >
        *       < > //signifies end of solutions list.
        */
        void printWords();
       
        /*
        * Preconditions: none
        * Postconditions: none
        * Description: prints every BogWord solution found in HBF of length len.
        * Ex for command of lengths "3", just "RAT": 
        *       < R 1 2 A 1 1 T 0 1 >
        *       < > //signifies end of solutions list.
        */
        void printWords(int len);
        
        /*
        * Preconditions: none.
        * Postconditions: none.
        * Description: Prints all solution words without coordinates separated
        * by end of lines.
        */
        void listWords();
        
        /* 
        * Preconditions: none.
        * Postconditions: none.
        * Description: Prints all solutions of length len without coordinates
        * separated by end of lines.
        */
        void listWords(int len); //just the text of length len, no coordinates
        
    private:
        /* Dictionary filled with the funnelled in acceptable words. */
        Dictionary dict; 
        
        /* A Dictionary that gets filled with solutions as they are found. This
        * prevents the same word from being entered twice. */
        Dictionary solutions;
        
        /* Core Boggle Board, 2 D dynamic array of BogLetts */
        BogLett** board;
        
        /* Private int variables that store the matrix dimensions upon
        * creation.*/
        int ROW, COL;
        
        /* Increments every time a new solution is found when solving. */
        int totalwordCount;
        
        /* List of solutions found. Struct contains array of BogWords and
        * numWords */
        BogWordList Allsolutions;
        
        /* Temporary list of words found. As words are found, BogWords get
        * pushed on to the queue. Later they are popped off and put
        * Allsolutions BogWord array. */
        queue<BogWord> wordlist; //the list of found words
        
        /*
        * Preconditions: passed a bog board BogLett with a character and 
        * position. Temp is a empty BogWord that is updated as the DFS recurses
        * and increments/decrements attempts.
        * Postconditions: recordSolution is called and given actual BogWords to 
        * record. In this manner, the recording structures, Allsolutions and 
        * wordlist queue are fed viable words and filled. 
        */
        void DFS(BogLett tile, BogWord* temp);
        
        /* 
        * Preconditions: board exists of dimensions ROW and COL
        * Postconditions: All BogLetts' visited booleans are false.
        * Description: loops through board and sets all visit booleans to false.
        */
        void resetBools();
        
        /*
        * Preconditions: passed a BogWord with a string word set within it.
        * Postconditions: If the word isn't already in the solution dictionary,
        * then the BogWord is added to it, and pushed onto to the queue of found
        * solutions. Private class variable, totalwordCount is also incremented.
        */
        void recordSolution(BogWord word); 
        
        /* 
        * Precondition: Allsolutions private BogWordList in a BogSolver points
        * to NULL, and doesn't really exist. wordlist queue is inhabited by
        * BogWords.
        * Postcondition: Allsolutions has been created number of words found
        * large, and is filled with BogWord solutions. wordlist queue is now
        * empty.
        */
        void constructBogWordList();
        
        /* convertString(string s)
        * Passed the input for a dictionary, filters out numbers or
        * non-alphabetic characters, and converts all char to uppercase.
        * Returns: the newly converted to UPPER string
        */
        string convertString(string s); 
};
        