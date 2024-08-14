import time
import paho.mqtt.client as mqtt
import numpy
import random

mqtc = mqtt.Client()

class GameOfLife:

   def __init__(self, N=112, M=16, T=2000):
      """ Set up Conway's Game of Life. """
      # Here we create two grids to hold the old and new configurations.
      # This assumes an N*N grid of points.
      # Each point is either alive or dead, represented by integer values of 1 and 0, respectively.
      self.N = N
      self.M = M
      self.old_grid = numpy.zeros(N*M, dtype='i').reshape(N,M)
      self.new_grid = numpy.zeros(N*M, dtype='i').reshape(N,M)
      self.T = T # The maximum number of generations
      # Set up a random initial configuration for the grid.
      clear("B")
      for i in range(0, self.N):
         for j in range(0, self.M):
            if(random.randint(0, 100) < 15):
               self.old_grid[i][j] = 1
               pixel(i,j,"Y")
            else:
               self.old_grid[i][j] = 0
      
   def live_neighbours(self, i, j):
      """ Count the number of live neighbours around point (i, j). """
      s = 0 # The total number of live neighbours.
      # Loop over all the neighbours.
      for x in [i-1, i, i+1]:
         for y in [j-1, j, j+1]:
            if(x == i and y == j):
               continue # Skip the current point itself - we only want to count the neighbours!
            if(x != self.N and y != self.M):
               s += self.old_grid[x][y]
            # The remaining branches handle the case where the neighbour is off the end of the grid.
            # In this case, we loop back round such that the grid becomes a "toroidal array".
            elif(x == self.N and y != self.M):
               s += self.old_grid[0][y]
            elif(x != self.N and y == self.M):
               s += self.old_grid[x][0]
            else:
               s += self.old_grid[0][0]
      return s

   def play(self):
      """ Play Conway's Game of Life. """

      t = 1 # Current time level
      while t <= self.T: # Evolve!
         print ("At time level %d" % t)

         # Loop over each cell of the grid and apply Conway's rules.
         for i in range(self.N):
            for j in range(self.M):
               live = self.live_neighbours(i, j)
               if(self.old_grid[i][j] == 1 and live < 2):
                  self.new_grid[i][j] = 0 # Dead from starvation.
                  pixel(i,j,"B")
               elif(self.old_grid[i][j] == 1 and (live == 2 or live == 3)):
                  self.new_grid[i][j] = 1 # Continue living.
                  pixel(i,j,"Y")
               elif(self.old_grid[i][j] == 1 and live > 3):
                  self.new_grid[i][j] = 0 # Dead from overcrowding.
                  pixel(i,j,"B")
               elif(self.old_grid[i][j] == 0 and live == 3):
                  self.new_grid[i][j] = 1 # Alive from reproduction.
                  pixel(i,j,"Y")
               #time.sleep()

         # Output the new configuration.
        
         # The new configuration becomes the old configuration for the next generation.
         self.old_grid = self.new_grid.copy()

         # Move on to the next time level
         t += 1
         time.sleep(2.5)

def pixel( x,y,color):
	mqtc.publish("foobar/flipdot/pixel", "{\"color\":\"" + color + "\",\"x\":" + str(x) + ",\"y\":" + str(y) + "}" )

def clear(color):
	mqtc.publish("foobar/flipdot/clear", color)
	time.sleep(5)

if(__name__ == "__main__"):
   mqtc.connect("mqtt.chaospott.de", 1883, 60)
   game = GameOfLife()
   game.play()
