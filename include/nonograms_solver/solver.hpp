#ifndef NONOGRAMS_SOLVER_H
#define NONOGRAMS_SOLVER_H

#include <vector>
#include <iostream>
#include <numeric>
#include <algorithm>

#include "functions.h"


class NonogramSolver
{
    enum StateData
    {
        UNDEFINED = -1,
        WHITE,
        BLACK
    };

public:

    NonogramSolver();
    NonogramSolver(const std::vector<std::vector<int>>& nonogram_data);
    ~NonogramSolver(){};

    // Getter
    int getSize(){return size_n_;}

    void solve();

    friend std::ostream& operator<<(std::ostream& os, const NonogramSolver& dt);
    
private:

    bool checkIfDataIsCorrect(const std::vector<std::vector<int>>& nonogram_data);
    std::vector<int> getRowByIndex(int index);
    std::vector<int> getColumnByIndex(int index);
    void generateMatrixSolution();    

    std::vector<int> estimatePermutations(const std::vector<int> &data_to_check, const std::vector<int> &square_data);
    bool checkPermutation(const std::vector<int> &data_to_check, const std::vector<int> &square_data);
    void addPermutation(std::vector<std::vector<int>> &all_permutations, const std::vector<int> &permutation_to_add);
    void tranformPermutation(std::vector<int> &permutation_to_tranform);

    int size_n_;
    std::vector<std::vector<int>> row_;
    std::vector<std::pair<int, int>> row_values_index_;

    std::vector<std::vector<int>> column_;
    std::vector<std::pair<int, int>> column_values_index_;
    
    std::vector<std::vector<int>> solution_;
};




#endif // NONOGRAMS_SOLVER_H