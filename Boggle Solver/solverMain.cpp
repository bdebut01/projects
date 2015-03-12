//main function for the solver

//compile solver with: g++ -Wall -Wextra -g solverMain.cpp BogSolver.cpp
// dictionary.o -o bbsolver
#include "BogSolver.h"

int main()
{
    BogSolver solver;
    
    solver.readDict();
    solver.readBoard();
    solver.solve();
    solver.printWords();
    return 0;
}