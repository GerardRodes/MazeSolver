from PIL import Image
from datetime import datetime
from operator import attrgetter

CONNECTION_COLOR = (129, 212, 250)
NODE_COLOR = (244, 67, 54)



def manhattan_distance(node1, node2):
  # Returns distance between 2 nodes
  # https://en.wiktionary.org/wiki/Manhattan_distance
  return abs(node1.x - node2.x) + abs(node1.y - node2.y)



class Node(object):
  
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.visited = False
    self.connections = []
    self.g = float('inf')
    self.h = None
    self.came_from = None


  @property
  def f(self):
    return self.g + self.h

  
  def unvisited_connections(self):
    return [conn for conn in self.connections if not conn.visited]
    
    
  def __repr__(self):
    return '<Node at x:{x}, y:{y}>'.format(x=self.x, y=self.y)



class Maze(object):

  # Contains each node in the maze
  nodes = []
  # Contains each node in each row and column
  nodes_by_axis = {
    'x':{},
    'y':{},
  }

  def __init__(self, img_path):
    self.file_name = img_path.split('/')[-1]
    self.image  = Image.open(img_path)
    self.pixels = self.image.load()
    self.width, self.height = self.image.size
    
    self.find_nodes()
    self.connect_nodes()
    self.print_connections()
    self.find_path()


  def connect_nodes(self):
    for x, nodes in self.nodes_by_axis['x'].iteritems():
      for i in range(len(nodes) - 1):
        if self.are_connected(nodes[i], nodes[i+1]):
          nodes[i].connections.append(nodes[i+1])
          nodes[i+1].connections.append(nodes[i])
          
    for y, nodes in self.nodes_by_axis['y'].iteritems():
      for i in range(len(nodes) - 1):
        if self.are_connected(nodes[i], nodes[i+1]):
          nodes[i].connections.append(nodes[i+1])
          nodes[i+1].connections.append(nodes[i])


  def are_connected(self, node1, node2):
    """
      2 nodes are connected if they are at the same row/col
      and there are no walls/nodes between them
    """
    free_way = True
    for pixel in self.pixels_between(node1, node2):
      if not self.is_white(pixel[0], pixel[1]):
        free_way = False
          
    return free_way
        

  def find_nodes(self):
    """
      Loop through each pixel to check if is a node or not.
      A node is a pixel of the laberint, that is not a wall or a middle part of a corridor.
      This way we can check the important parts of the maze (nodes) and work with them.
    """
    for y in range(self.height):
      for x in range(self.width):
        if self.is_node(x, y):
          self.nodes.append( Node(x, y) )
          
          
  def is_node(self, x, y):
    """
      A node complies the following rules:
      1 - Is white
      2 - Neighbour cases:
          2.1 - has 1, 3 or 4 white neighbour (anything racist going on here)
          2.2 - if has 2 neightbours then this neigbours must have different x and different y
                just to make sure that our pixel isn't just a part of a corridor
    """
    if self.is_white(x, y):
      neighbours = self.get_neighbours(x, y)
      if len(neighbours) == 2:
        if neighbours[0][0] != neighbours[1][0] and neighbours[0][1] != neighbours[1][1]:
          self.add_node(x, y)
      else:
        self.add_node(x, y)
  
  
  def add_node(self, x, y):
    node = Node(x, y)
    self.nodes.append(node)
    
    if self.nodes_by_axis['x'].get(x, False):
      self.nodes_by_axis['x'][x].append(node)
    else:
      self.nodes_by_axis['x'][x] = [node]
      
    if self.nodes_by_axis['y'].get(y, False):
      self.nodes_by_axis['y'][y].append(node)
    else:
      self.nodes_by_axis['y'][y] = [node]
    
    
  def get_neighbours(self, x, y):
    """
      Given a coordinate, returns a list of the neighbours.
      A neigbour exists in the grid and is white
    """
    possible_pixels = [[x+1, y], [x, y+1], [x-1, y], [x, y-1]]
    return [pixel for pixel in possible_pixels
            if pixel[0] >= 0 and pixel[0] < self.width and
               pixel[1] >= 0 and pixel[1] < self.height and
               self.is_white(pixel[0], pixel[1])]


  def is_white(self, x, y):
    """
      A perfect white should be (255, 255, 255), which all together sums 765
      So i'll set that white means 715 or more, anything else will be black (wall)
    """
    return sum(int(value) for value in self.pixels[x, y]) >= 715
    
    
  def pixels_between(self, node1, node2):
    """
      Returns the pixels between 2 nodes in the same row/col
    """
    pixels_between = []
    
    if node1.x == node2.x:
      # they are at the same col
      distance = abs(node2.y - node1.y)
      for i in range(distance - 1):
        pixels_between.append([node1.x, (node1.y if node2.y > node1.y else node2.y) + i+1])
          
    elif node1.y == node2.y:
      # they are at the same row
      distance = abs(node2.x - node1.x)
      for i in range(distance - 1):
        pixels_between.append([(node1.x if node2.x > node1.x else node2.x) + i+1, node1.y])
    
    return pixels_between
  
        
  def print_path(self, node):
    output_image = self.image.copy()
    output_pixels = output_image.load()
    
    while node.came_from:
      output_pixels[node.x, node.y] = NODE_COLOR
      for pixel in self.pixels_between(node, node.came_from):
        output_pixels[pixel[0], pixel[1]] = NODE_COLOR
      node = node.came_from
    output_pixels[node.x, node.y] = NODE_COLOR
    
    output_image.save('output_path_' + self.file_name, 'PNG')
    
    
  def print_connections(self):
    self.reset_visits()
    output_image = self.image.copy()
    output_pixels = output_image.load()
    
    for node in self.nodes:
      node.visited = True
      output_pixels[node.x, node.y] = NODE_COLOR
      for connection in node.connections:
        if not connection.visited:
          for pixel in self.pixels_between(node, connection):
            output_pixels[pixel[0], pixel[1]] = CONNECTION_COLOR
      
    output_image.save('output_connections_' + self.file_name, 'PNG')
    
    
  def reset_visits(self):
    for node in self.nodes:
      node.visited = False
      
      
  def find_path(self):
    # Path finding with A*
    # https://en.wikipedia.org/wiki/A*_search_algorithm
    self.reset_visits()
    
    start = self.nodes_by_axis['y'][0][0]
    goal  = self.nodes_by_axis['y'][self.height - 1][0]
    start.visited = True
    
    print 'Start: {}'.format(start)
    print 'Goal: {}'.format(goal)
    
    current = start
    unvisited_connections = current.unvisited_connections()
    
    while unvisited_connections:
      print '\nCurrent: {}'.format(current)  
      print 'UC: {}'.format(unvisited_connections)
      
      current.g = 0
      current.h = current.h if current.h else manhattan_distance(current, goal)
      
      for connection in unvisited_connections:
        connection.g = manhattan_distance(connection, current)
        connection.h = connection.h if connection.h else manhattan_distance(connection, goal)
        connection.came_from = current
      
      current = min(unvisited_connections, key=attrgetter('f'))
      current.visited = True
      unvisited_connections = current.unvisited_connections()
      
      aux = current
      if current != goal:
        while not unvisited_connections:
          print '\nDead end at {}'.format(current)
          current = current.came_from
          if current:
            unvisited_connections = current.unvisited_connections()
          else:
            print 'No possible paths, ending...'
            self.print_path(aux)
            break
      else:
        print '\nDone!!'
        self.print_path(current)
        break
      
      
      
start = datetime.now()
Maze('mazes/combo400.png')
print 'Time elapsed: {}'.format(datetime.now() - start)