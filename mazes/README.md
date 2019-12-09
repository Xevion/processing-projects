# mazes

## About

Projects that generate mazes using various algorithms. Developed primarily in 2018-2019. All of these are generating simple square mazes, just using different algorithms and occasionally a little twist. Original sketch names have been preserved.

## Sketches

- **MazeGenV2** Second maze generation attempt. First *working* maze implementation. Recursive Backtracker algorithm.

![MazeGenV2 Gif](./MazeGenV2_1.gif)

- **MazeGenSolve** - Maze gen with a completed path shown after. Recursive Backtracker algorithm for Generation, A* algorithm for pathfinding (very similar in theory). Exceptionally similar to the Growing Tree algorithm in implementation (1-2 line change).

![MazeGenSolve Gif](./MazeGenSolve_1.gif)

- **MazeGenBinaryTree** - Binary Tree algorithm. Creates a grid equal to the minimum of the mouse coordinates (increasing from the top-left). Requires some editing to make sure it doesn't automatically crash if you click near the center to bottom-right.

![MazeGenBinaryTree Gif](./MazeGenBinaryTree_1.gif)

- **MazeGenGrowingTree** - Growing Tree algorithm. Grows centered on where your mouse clicks (originally from a randomized position).

![MazeGenGrowingTree Gif](./MazeGenGrowingTree_1.gif)

- **MazeGenKruskal** - Kruskal Tree algorithm

![MazeGenKruskal Gif](./MazeGenKruskal_1.gif)

- **MazeGenSidewinder** - Sidewinder algorithm. A little bit buggy at the end, but properly implemented none the less. I had difficulty implementing this, and thus never got around to figuring out how to remove those boxes. Before recording, I modified it to properly show the erroring boxes, otherwise they would never be visible.

![MazeGenSideWinder Gif](./MazeGenSidewinder_1.gif)

- **MazeClustersCreator** - Not so much a maze as a interesting side-project when developing my maze generators. Somewhat buggy.

![Maze Clusters Creator Gif](./MazeClustersCreator_1.gif)