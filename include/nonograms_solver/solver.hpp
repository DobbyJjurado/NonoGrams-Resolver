#ifndef NONOGRAMS_SOLVER_H
#define NONOGRAMS_SOLVER_H

#include <vector>
#include <iostream>
#include <numeric>

class NonogramSolver
{

public:
    NonogramSolver();
    NonogramSolver(const std::vector<std::vector<int>>& nonogram_data);
    ~NonogramSolver(){};

private:

    int size_n_;

    bool checkIfDataIsCorrect(const std::vector<std::vector<int>>& nonogram_data);

    std::vector<bool> row_;
    std::vector<bool> column_;
    std::vector<std::vector<int>> solution_;
};




#endif // NONOGRAMS_SOLVER_H