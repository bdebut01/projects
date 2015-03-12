#include <iostream>
using namespace std;

void printWord(string word, int points);

int main()
{
    string success;
    string word;
    int score = 0;
    int wordCount = 0;
    do
    {
        cin >> success;
        cin >> word;
        unsigned int size = word.size();
        if(success == "OK")
        {
            if(size == 3 || size == 4)
            {
                printWord(word, 1);
                score++;
            }
            if(size == 5)
            {
                printWord(word, 2);
                score += 2;
            }
            if(size == 6)
            {
                printWord(word, 3);
                score += 3;
            }
            if(size == 7)
            {
                printWord(word, 5);
                score += 5;
            }
            if(size >= 8)
            {
                printWord(word, 11);
                score += 11;
            }
            wordCount++;
        }
        else
        {
            cout << 0 << " " << success << " " << word << endl;
        } 
    } while(!cin.eof());
    cout << wordCount << " " << "words" << " " << score << " points" << endl;  
}

//Prints a correct word.
void printWord(string word, int points)
{
    cout << points << " OK " << word << endl;
}