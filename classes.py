import numpy as np
import pandas as pd
from random import random, randint, uniform, choice
import matplotlib.pyplot as plt
import time

class Agent:
    #
    def __init__(self, 
                 name: str, 
                 x_init: float, 
                 y_init: float, 
                 max_speed: float, 
                 color: list, 
                 lim_age: int, 
                 gene_dominance: float,
                 borders_x: list, 
                 borders_y: list):
        # 
        self.name = name
        self.x_init = x_init
        self.y_init = y_init
        self.x = x_init
        self.y = y_init
        self.color = color
        self.max_speed = max_speed
        self.lim_age = lim_age
        self.gene_dominance = gene_dominance
        self.borders_x = borders_x
        self.borders_y = borders_y
        self.age = 0
        self.alive = True
        
    def move(self):
        xmin_border = self.borders_x[0]
        xmax_border = self.borders_x[1]
        ymin_border = self.borders_y[0]
        ymax_border = self.borders_y[1]
        
        x_direction, y_direction = self.max_speed*np.random.uniform(-1, 1, 2)
        
        if (self.x + x_direction > xmax_border) or (self.x + x_direction < xmin_border):
            self.x -= x_direction
        else:
            self.x += x_direction
            
        if (self.y + y_direction > ymax_border) or (self.y + y_direction < ymin_border):
            self.y -= y_direction
        else:
            self.y += y_direction
        
    def grow(self):
        self.age += 1
        if self.age >= self.lim_age:
            self.alive = False



class Agent_system:
    
    def __init__(self, 
                 colors: int, 
                 max_speed: float, 
                 lim_age: int, 
                 dist_inter: float,
                 borders_x: list, 
                 borders_y: list):
        
        self.date = 0
        self.colors = colors
        self.max_speed = max_speed
        self.lim_age = lim_age
        self.dist_inter = dist_inter
        self.borders_x = borders_x
        self.borders_y = borders_y
        self.population = None
        self.cemetery = []
        self.alive_population = 0
        self.total_population = 0
    
    def init_population(self, N: int):

        self.population = [Agent(i, 
                                 uniform(self.borders_x[0], self.borders_x[1]),
                                 uniform(self.borders_y[0], self.borders_y[1]), 
                                 self.max_speed, 
                                 choice(self.colors), 
                                 self.lim_age, 
                                 random(),
                                 self.borders_x, 
                                 self.borders_y)
                          for i in range(N)]
        
        self.alive_population = N
        self.total_population = N
            
    def pass_time(self):
        self.date += 1
        for agent in self.population:
            if agent.alive:
                agent.grow()
            else:
                self.cemetery.append(agent)
                self.population.remove(agent)
                self.alive_population = len(self.population)
                
            
    def move(self):
        for agent in self.population:
            if agent.alive:
                agent.move() 
            
    def distance(self, agent1: Agent, agent2: Agent):
        x1 = agent1.x
        x2 = agent2.x
        y1 = agent1.y
        y2 = agent2.y
        
        return np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
        
    def simulate(self, T: int):
        
        fig, ax = plt.subplots()
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')        
        for t in range(T):
            self.move()
            self.pass_time()
            for agent1 in self.population:
                for agent2 in self.population:
                    if agent1 != agent2 and self.distance(agent1, agent2) <= self.dist_inter:
                        if agent1.gene_dominance >= agent2.gene_dominance:
                            dominant_color = agent1.color
                        else:
                            dominant_color = agent2.color
            
                        new_agent = Agent(self.total_population + 1, 
                                         (agent1.x + agent2.x)/2,
                                         (agent1.y + agent2.y)/2, 
                                         self.max_speed, 
                                         dominant_color, 
                                         self.lim_age, 
                                         random(),
                                         self.borders_x, 
                                         self.borders_y)
                        self.population.append(new_agent)
                        self.alive_population = len(self.population)
                        self.total_population += 1
                
            X = [agent.x for agent in self.population]
            Y = [agent.y for agent in self.population]
            colors = [agent.color for agent in self.population]
            
            # Plot the point
            plt.scatter(X, Y, c = colors)
            plt.xlim(self.borders_x[0], self.borders_x[1])
            plt.ylim(self.borders_y[0], self.borders_y[1])
            # Display the plot and clear the previous one
            display(fig)
            clear_output(wait=True)

            # Pause for a short duration
            time.sleep(0.1)

            # Clear the current axis
            ax.cla()

        # Close the plot after the loop
        plt.close()
                            
