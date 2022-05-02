#include "ros/ros.h"
#include <sstream>

#include "nonograms_solver/solver.hpp"


int main(int argc, char **argv)
{
  ros::init(argc, argv, "nonograms_solver");
  std::vector<std::vector<int>> nonogram_data{
    {5},
    {1},{5},{1},{5},{1, 1},
    {5},{1, 1},{1, 1},{1, 25},{1, 2}
  };
  NonogramSolver solver(nonogram_data);


  return 0;
}
