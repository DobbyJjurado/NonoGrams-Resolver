// Bring in my package's API, which is what I'm testing
#include <nonograms_solver/solver.hpp>
// Bring in gtest
#include <gtest/gtest.h>

class NonogramSolverTest : public ::testing::Test 
{

 protected:

    void SetUp() override
    {
      solver_ = NonogramSolver();
    }

    NonogramSolver solver_;
};


TEST_F(NonogramSolverTest, Constructor)
{
  EXPECT_EQ(solver_.getSize(), 0);
}

// Run all the tests that were declared with TEST()
int main(int argc, char **argv)
{
  //UnderConstruction TODO -> All function test and read test from file
  testing::InitGoogleTest(&argc, argv);
  return RUN_ALL_TESTS();
}