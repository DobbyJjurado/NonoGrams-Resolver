#include <nonograms_solver/solver.hpp>
NonogramSolver::NonogramSolver()
{
    size_n_ = 0;
    row_ = {};
    column_ = {};
}

NonogramSolver::NonogramSolver(const std::vector<std::vector<int>>& nonogram_data)
{
    if(!nonogram_data.empty())
    {
        size_n_ = nonogram_data.front().front();

        if(checkIfDataIsCorrect(nonogram_data))
        {
            std::cout << "Data Correct" << std::endl;
        }
        else
        {
            std::cout << "Data Incorrect" << std::endl;
        }
    }

}


bool NonogramSolver::checkIfDataIsCorrect(const std::vector<std::vector<int>>& nonogram_data)
{
    bool is_correct {false};
    int total_length_vector = size_n_*2 + 1;
    if( total_length_vector == nonogram_data.size() )
    {
        int counter {};
        for (auto & data : nonogram_data)
        {
            int sum_of_elems = std::accumulate(data.begin(), data.end(), 0);
            std::cout << "Counter Total " << counter++ << " -> " << sum_of_elems << std::endl;
            if(sum_of_elems > size_n_)
            {
                break;
            }

        }
        is_correct = true;
    }

    return is_correct;

}