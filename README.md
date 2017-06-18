# MazeSolver
**It solves a maze**  

## The Maze
The maze must fit the following rules:  
1. Walls and corridors will be 1px sized
2. Must be framed with walls
3. Starting point will be at y=0 and the finishing point at the bottom of the maze
4. walls are black
5. corridors are white
6. The maze will be provide as an rgb image in a png file.

## How it works
The first thing it does is looking for nodes. A node is a pixel, which is at an intersection of 2 or more corridors. This way I only check the nodes, preventing unnecessary tracking of useless nodes.  
Once it founds all the nodes, creates the connections between them, a connection can exist between 2 nodes if there aren't walls or other nodes between them (the connections are more or less the corridors of the maze but they get cut at nodes).  
Now that every node is connected I implemented A\* algorithm to find the shortest path depending on the length of a node's connections.  

## Just show me images
**ok**  

Here we got a maze of 40x40 (reescaled images for this, irl is everything 1px wide)  
<p align="center">
  <img alt="Maze" src="http://i.imgur.com/RnQTlpA.png" />
</p>  

In this other image we can see the nodes (red), and connections (blue)
<p align="center">
  <img alt="Maze nodes and connections" src="http://i.imgur.com/AiDFaLK.png" />
</p>  

And finally here we got the shortest path to the goal  
<p align="center">
  <img alt="Maze path" src="http://i.imgur.com/4OoJGzc.png" />
</p>  

### Now 401px
<p align="center">
  <img alt="Maze" src="http://i.imgur.com/Iq8d7M8.png" />
</p>
<p align="center">
  <img alt="Maze nodes and connections" src="http://i.imgur.com/swRUrcR.png" />
</p>  
<p align="center">
  <img alt="Maze path" src="http://i.imgur.com/PNA8ImD.png" />
</p>  

## Try it by yourself  
There are more mazes to tryout at the folder `mazes`, try them editing the initialization Maze line at `maze_solver.py`
