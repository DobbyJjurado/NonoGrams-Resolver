#include "ros/ros.h"
#include <sstream>

#include "nonograms_solver/solver.hpp"


int main(int argc, char **argv)
{
  ros::init(argc, argv, "nonograms_solver");
  /*std::vector<std::vector<int>> nonogram_data{
    {5},
    {1},{5},{1},{5},{1, 1},
    {5},{1, 1},{1, 1},{1, 1},{1, 2}
  };
  */
  /*std::vector<std::vector<int>> nonogram_data{
    {10},
    {2, 1},{2, 1},{2, 1},{2, 1},{2, 1}, {3, 1},{2, 1},{2, 1},{2, 1},{2, 1},
    {2, 1},{2, 1},{2, 1},{2, 1},{2, 1}, {3, 1},{2, 1},{2, 1},{2, 1},{2, 1}
  };*/

  std::vector<std::vector<int>> nonogram_data{
    {4},
    {1},{1},{1},{1},
    {1},{1},{1},{1}
  };
  NonogramSolver solver(nonogram_data);

  std::cout << solver << std::endl;

  solver.solve();

  return 0;
}
