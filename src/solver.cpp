#include <nonograms_solver/solver.hpp>

NonogramSolver::NonogramSolver()
{
    std::cout << "NonogramSolver constructor" << std::endl;
    size_n_ = 0;
    row_ = {};
    column_ = {};
}

std::ostream& operator<<(std::ostream& os, const NonogramSolver& rhs)
{

    os << "Solution \n";
    for(auto &row : rhs.solution_)
    {
        std::string data_to_print = "\t";
        for(auto &value : row)
        {
            if(value == rhs.UNDEFINED)
                data_to_print += "U ";
            else if (value == rhs.WHITE)
                data_to_print += "W ";
            else if (value == rhs.BLACK)
                data_to_print += "B ";
        }
        data_to_print+= "\n";
        os << data_to_print;
    }
    return os;
}

NonogramSolver::NonogramSolver(const std::vector<std::vector<int>>& nonogram_data)
{
    if(!nonogram_data.empty())
    {
        size_n_ = nonogram_data.front().front();

        if(checkIfDataIsCorrect(nonogram_data))
        {
            std::cout << "Data Correct" << std::endl;
            generateMatrixSolution();
            row_ = {nonogram_data.begin() + 1, nonogram_data.begin() + size_n_ + 1};

            int index = {};
            for(auto & data : row_)
            {
                row_values_index_.emplace_back(std::accumulate(data.begin(), data.end(), 0), index++);
            }
            std::sort(row_values_index_.begin(), row_values_index_.end(),lambda::sortedPairDescendingOrder<int,int>());

            column_ = {nonogram_data.begin() + size_n_ + 1, nonogram_data.end()};
            index = {};
            for(auto & data : column_)
            {
                column_values_index_.emplace_back(std::accumulate(data.begin(), data.end(), 0), index++);
            }
            std::sort(column_values_index_.begin(), column_values_index_.end(), lambda::sortedPairDescendingOrder<int,int>());
        }
        else
        {
            std::cout << "Data Incorrect" << std::endl;
            throw std::invalid_argument("Bad data input, Check the data");
        }
    }
}


bool NonogramSolver::checkIfDataIsCorrect(const std::vector<std::vector<int>>& nonogram_data)
{
    int total_length_vector = size_n_*2 + 1;
    std::cout << total_length_vector << " " << nonogram_data.size() << std::endl;
    if( total_length_vector == nonogram_data.size() )
    {
        int counter {};
        for (auto & data : nonogram_data)
        {
            int sum_of_elems = std::accumulate(data.begin(), data.end(), 0);
            if(sum_of_elems > size_n_)
            {
                return false;
            }
        }
    }
    else
    {
        return false;
    }
    return true;
}

void NonogramSolver::solve()
{
    int row_index = {};
    int column_index = {};
    std::vector<int> data_to_check;
    std::vector<int> square_data; 

    if (row_values_index_[row_index].first >= column_values_index_[column_index].first)
    {
        data_to_check = getRowByIndex(row_values_index_[row_index].second);
        square_data = row_.at(row_values_index_.at(row_index).second);
    }
    else
    {
        data_to_check = getColumnByIndex(column_values_index_[column_index].second);
        square_data = column_.at(column_values_index_.at(column_index).second);
    }

    printVector(data_to_check);

    estimatePermutations(data_to_check, square_data);

    if (row_index >= size_n_)
        row_index = 0;

    if (column_index >= size_n_)
        column_index = 0;
    
}


void NonogramSolver::generateMatrixSolution()
{
    std::vector<std::vector<int>> solutions_(size_n_, std::vector<int>(size_n_,UNDEFINED));
    solution_ = solutions_;
}

std::vector<int> NonogramSolver::getRowByIndex(int index)
{
    if( index < size_n_ )
    {
        return solution_.at(index);
    }
    else
    {
        throw std::invalid_argument("getRowByIndex -> index must be less than size");
    }

}

std::vector<int> NonogramSolver::getColumnByIndex(int index)
{
    std::vector<int> column(size_n_);
    if(index < size_n_)
    {
        for(int i {0}; i < size_n_; ++i)
        {
            column[i] = solution_.at(i).at(index);
        }

        return column;
    }
    else
    {
        throw std::invalid_argument("getRowByIndex -> index must be less than size");
    }
}

std::vector<int> NonogramSolver::estimatePermutations(const std::vector<int> &data_to_check, const std::vector<int> &square_data)
{
    std::vector<int> final_permutation;
    if(square_data.size() == 1 && square_data.front() == size_n_)
    {
        std::vector<int> all_values_black (size_n_, StateData::BLACK);
        final_permutation = all_values_black;
    }
    else
    {
        std::vector< std::vector<int>> all_permutations_;
        int max_number_of_white_spaces = size_n_ - (std::accumulate(square_data.begin(), square_data.end(), 0));

        for(int i{1}; i <= max_number_of_white_spaces; ++i)
        {
            std::vector<int> initial_permutation{};
            for(const auto & data : square_data)
            {
                std::vector<int> black(data, StateData::BLACK);
                initial_permutation.insert(initial_permutation.end(), black.begin(), black.end());
                if(initial_permutation.size() < size_n_)
                {
                    int white_square = i;
                    if(size_n_ - initial_permutation.size() < white_square)
                        white_square = size_n_ - initial_permutation.size();

                    std::vector<int> white(white_square, StateData::WHITE);
                    initial_permutation.insert(initial_permutation.end(), white.begin(), white.end());
                }
            }

            while(initial_permutation.size() < size_n_)
            {
                initial_permutation.push_back(StateData::WHITE);
            }

            addPermutation(all_permutations_, initial_permutation);

            std::vector<int> secondary_permutation = initial_permutation;
            std::rotate(secondary_permutation.rbegin(), secondary_permutation.rbegin()+1, secondary_permutation.rend());
            while (secondary_permutation != initial_permutation)
            {
                if(checkPermutation(secondary_permutation, square_data))
                {   
                    addPermutation(all_permutations_, secondary_permutation);
                }
                std::rotate(secondary_permutation.rbegin(), secondary_permutation.rbegin()+1, secondary_permutation.rend());
            }  
        }

        std::cout << std::endl;
        for(auto j : all_permutations_)
        {
            printVector(j);
        }

        final_permutation = math::sumAllColumnsMatrix(all_permutations_);

        printVector(final_permutation);
        std::cout << "Tranformation " << std::endl;
        tranformPermutation(final_permutation);
        printVector(final_permutation);
    }
    return final_permutation;
}

bool NonogramSolver::checkPermutation(const std::vector<int> &data_to_check, const std::vector<int> &square_data)
{
    std::vector<int> number_black_square = square_data;
    int counter = 0;
    
    for(int i{}; i < data_to_check.size(); ++i)
    {
        if(data_to_check[i] == StateData::BLACK)
        {
            counter++;
        }

        if(data_to_check[i] == StateData::WHITE || i == data_to_check.size() - 1)
        {
            if(counter != 0)
            {
                auto it = std::find(number_black_square.begin(), number_black_square.end(), counter);
                if (it != number_black_square.end())
                {
                    number_black_square.erase(it);
                }
                counter = 0;
            }
        }
    }
    return number_black_square.empty();
}

void NonogramSolver::addPermutation(std::vector<std::vector<int>> &all_permutations, const std::vector<int> &permutation_to_add)
{
    auto it = std::find_if(all_permutations.begin(), all_permutations.end(), lambda::checkifVectorOfVectorContainsAVector<int>(permutation_to_add));
    if(it == all_permutations.end())
    {
        all_permutations.push_back(permutation_to_add);
    }

}

void NonogramSolver::tranformPermutation(std::vector<int> &permutation_to_tranform)
{
    std::transform(permutation_to_tranform.begin(), permutation_to_tranform.end(), permutation_to_tranform.begin(), 
        [this](int value)
        {
            if(value == 0)
            {
                return  StateData::WHITE;
            }
            else if (value == this->size_n_)
            {
                return  StateData::BLACK;
            }
            else
            {
                return  StateData::UNDEFINED;
            }
        });
}
