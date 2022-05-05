#ifndef FUNCTIONS_H
#define FUNCTIONS_H


template<typename T>
inline void printVector(T &v)
{
    std::cout << "[ ";
    for(const auto & item : v) 
    {
        std::cout << item << ", ";
    }
    std::cout << "\b\b ]" << std::endl;
}


namespace lambda
{
    template<typename T, typename B>
    inline auto sortedPairDescendingOrder()
    {
        return [](const std::pair<T,B> &a,
                    const std::pair<T,B> &b){ return a.first > b.first; };
    }

    template<typename T>
    inline auto checkifVectorOfVectorContainsAVector(std::vector<T> vector_to_check)
    {
        return [vector_to_check](std::vector<T> v){return v == vector_to_check; }; 
    }
}

namespace math
{
    inline int sumColumnMatrix(const std::vector<std::vector<int>> &matrix, int index)
    {
        int sum {0};
        for(auto &row : matrix)
        {
            sum += row[index];
        }

        return sum;
    }

    inline std::vector<int> sumAllColumnsMatrix(const std::vector<std::vector<int>> &matrix)
    {
        std::vector<int> columns {};
        for(int i{0}; i < matrix.front().size(); ++i)
        {
            columns.push_back(sumColumnMatrix(matrix, i));
        }

        return columns;

    }

}




#endif // FUNCTIONS_H