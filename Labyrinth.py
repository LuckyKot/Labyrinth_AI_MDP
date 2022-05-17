import copy


#Class table that generates and maintains the 2D list
#initializes with 1 variable n, which is the dimensions of the 2D list: nxn
#get len returns length
#print_table prints the current table according to format
#populate_cells substitues integers 0 in the table with an item of class Cell() described below
#init_PNS stands for initialize Stone Positive terminal Negative terminal and does exactly that
#sets these items to their places as the Cell() objects
class Table:
    def __init__(self, n):
        self.table=[]
        for i in range(n):
            self.table.append([])
            for j in range (n):
                self.table[i].append(0)
    
    def get_len(self):
        return len(self.table)
    
    def print_table(self): 
        for i in range(len(self.table)):
            for j in range(len(self.table)):
                if self.table[i][j].to_string()==None:
                    print('{0:>6}'.format('STONE'),',',sep='',end='')
                else:
                    print('{0:>6}'.format(format(self.table[i][j].to_string())),',',sep='',end='')
            print('\n')
            
    def populate_cells(self):
        for i in range(len(self.table)):
            for j in range(len(self.table)):
                if self.table[i][j]==0:
                    temp=Cell()
                    self.table[i][j]=temp
            
    def init_PNS(self,p,n,s):
        temp = Cell()
        temp.update_cell(p[2],'n')
        self.table[p[0]][p[1]]=temp
        temp2 = Cell()
        temp2.update_cell(n[2],'n')
        self.table[n[0]][n[1]]=temp2
        temp3 = Cell()
        temp3.update_cell('STONE','')
        self.table[s[0]][s[1]]=temp3
        
#Class Cell describes one item of the table that, according to the assignment, must have a direction and a value
#init sets the value to 0 and the default direction is n
#update cell just allows to set these items to custom values
#get_val just returns value
#get_dir just returns direction
#to_string translates the Cell() object to string for final output

class Cell:
    def __init__(self):
        self.value=0
        self.direction='n'
    
    def update_cell(self,val,d):
        self.value=val
        self.direction=d
        
    def get_val(self):
        return self.value
    
    def get_dir(self):
        return self.direction
    
    def to_string(self):
        if not self.value=='STONE':
            return str(format(self.value,'.2f'))+'('+self.direction+')'
        
#an MDP function that starts the whole process, mainly responsible for iterations
def mdp_start(grid,iterations,noise,discount,p,n):
    for i in range(iterations):
        mdp(grid,noise,discount,p,n)
        print('Iteration:',i+1)
        grid.print_table()
        print('---------------------------------------------------------')

#the actual MDP begins here, sets pi, pj, ni, nj for future comfortable use
#creates a snapshot of a grid so we work with one state of a grid at a time and NOT update it as we go
#this fixes the problem of it going sequentially from left to right, top to bottom and some values 
#(the bottom or right ones) get updated right away while top and left ones wait for their update in next iteration
#which is not good
#then it starts to work on each cell, as mentioned before, left to right, top to bottom
def mdp(grid,noise,discount,p,n):
    pi=p[0]
    pj=p[1]
    ni=n[0]
    nj=n[1]
    
    temp_grid=Table(grid.get_len())
    temp_grid.table=copy.deepcopy(grid.table)
    
    for i in range(grid.get_len()):
            for j in range(grid.get_len()):
                calculate_values(grid,temp_grid,i,j,noise,discount,pi,pj,ni,nj)
    grid.table=copy.deepcopy(temp_grid.table)

#function that calculates values and determines the direction for each cell
#maintains an array of length 4 where each place represents a direction
#0-north, 1-east, 2-west,3-south
#gather values for each direction and picks the best one, directly changing the value
#on the grid by the end of the function
def calculate_values(grid,temp_grid,i,j,noise,discount,pi,pj,ni,nj):
    options=[0,0,0,0]
    
    if not (pi==i and pj==j) and not (ni==i and nj==j) and not (grid.table[i][j].get_val()=='STONE'):
        n = calculate_north(grid,i,j,noise,discount)
        options[0]=n
        
        e = calculate_east(grid,i,j,noise,discount)
        options[1]=e

        w = calculate_west(grid,i,j,noise,discount)
        options[2]=w

        s = calculate_south(grid,i,j,noise,discount)
        options[3]=s
        
        if options.index(max(options)) == 0:
            temp=Cell()
            temp.update_cell(max(options),'n')
            temp_grid.table[i][j]=temp
        elif options.index(max(options)) == 1:
            temp=Cell()
            temp.update_cell(max(options),'e')
            temp_grid.table[i][j]=temp
        elif options.index(max(options)) == 2:
            temp=Cell()
            temp.update_cell(max(options),'w')
            temp_grid.table[i][j]=temp
        elif options.index(max(options)) == 3:
            temp=Cell()
            temp.update_cell(max(options),'s')
            temp_grid.table[i][j]=temp

#Here are the actual calculation functions
#they check for restrictions such as walls and stones
#then calculates with respect to noise and time penalty
def calculate_north(grid,i,j,noise,discount):    
    temp=grid.table[i][j]
    
    if i-1>=0   and not grid.table[i-1][j].get_val()=='STONE':
        temp2=grid.table[i-1][j]
        value_north=(1-noise)*temp2.get_val()*discount
    else:
        value_north=(1-noise)*grid.table[i][j].get_val()*discount
        
    if j-1>=0   and not grid.table[i][j-1].get_val()=='STONE':
        temp3=grid.table[i][j-1]
        value_west=(noise/2)*temp3.get_val()*discount
    else:
        value_west=(noise/2)*grid.table[i][j].get_val()*discount
        
    if j+1<grid.get_len() and not grid.table[i][j+1].get_val()=='STONE':
        temp4=grid.table[i][j+1]
        value_east=(noise/2)*temp4.get_val()*discount
    else:
        value_east=(noise/2)*grid.table[i][j].get_val()*discount
        
    final_value=value_north+value_west+value_east
        
    return final_value
    
def calculate_east(grid,i,j,noise,discount):
    temp=grid.table[i][j]
    if j+1<grid.get_len()   and not grid.table[i][j+1].get_val()=='STONE':
        temp2=grid.table[i][j+1]
        
        value_east=(1-noise)*temp2.get_val()*discount
        
    else:
        value_east=(1-noise)*grid.table[i][j].get_val()*discount
    if i-1>=0   and not grid.table[i-1][j].get_val()=='STONE':
        temp3=grid.table[i-1][j]
        value_north=(noise/2)*temp3.get_val()*discount
    else:
        value_north=(noise/2)*grid.table[i][j].get_val()*discount
        
    if i+1<grid.get_len() and not grid.table[i+1][j].get_val()=='STONE':
        temp4=grid.table[i+1][j]
        value_south=(noise/2)*temp4.get_val()*discount
    else:
        value_south=(noise/2)*grid.table[i][j].get_val()*discount
        
        
    final_value=value_east+value_north+value_south

    
    return final_value

def calculate_west(grid,i,j,noise,discount):
    temp=grid.table[i][j]
    if j-1>=0   and not grid.table[i][j-1].get_val()=='STONE':
        temp2=grid.table[i][j-1]
        value_west=(1-noise)*temp2.get_val()*discount
    else:
        value_west=(1-noise)*grid.table[i][j].get_val()*discount
    if i-1>=0   and not grid.table[i-1][j].get_val()=='STONE':
        temp3=grid.table[i-1][j]
        value_north=(noise/2)*temp3.get_val()*discount
    else:
        value_north=(noise/2)*grid.table[i][j].get_val()*discount
    if i+1<grid.get_len()   and not grid.table[i+1][j].get_val()=='STONE':
        temp4=grid.table[i+1][j]
        value_south=(noise/2)*temp4.get_val()*discount
    else:
        value_south=(noise/2)*grid.table[i][j].get_val()*discount
        
    final_value=value_west+value_north+value_south
        
    return final_value

def calculate_south(grid,i,j,noise,discount):
    temp=grid.table[i][j]
    if i+1<grid.get_len()   and not grid.table[i+1][j].get_val()=='STONE':
        temp2=grid.table[i+1][j]
        value_south=(1-noise)*temp2.get_val()*discount
    else:
        value_south=(1-noise)*grid.table[i][j].get_val()*discount
    if j-1>=0   and not grid.table[i][j-1].get_val()=='STONE':
        temp3=grid.table[i][j-1]
        value_west=(noise/2)*temp3.get_val()*discount
    else:
        value_west=(noise/2)*grid.table[i][j].get_val()*discount
    if j+1<grid.get_len()   and not grid.table[i][j+1].get_val()=='STONE':
        temp4=grid.table[i][j+1]
        value_east=(noise/2)*temp4.get_val()*discount
    else:
        value_east=(noise/2)*grid.table[i][j].get_val()*discount
        
    final_value=value_south+value_west+value_east
        
    return final_value


#The final start() function
def start():
    #values to build the 'labyrinth' and rules
    #-------------------------------------------------
    stoneLocation=[2, 8]  #[row, column]
    positiveTerminalLocation = [0,9,2]  #[row, column, reward value]
    negativeTerminalLocation = [1,9, -2]  #[row, column, reward value]
    iteration=30
    noise=0.15
    discount=0.91
    #-------------------------------------------------
    test=Table(10)
    test.init_PNS(positiveTerminalLocation,negativeTerminalLocation,stoneLocation)
    test.populate_cells()
    print('Iteration:initial')
    test.print_table()
    print('---------------------------------------------------------')
    mdp_start(test,iteration,noise,discount,positiveTerminalLocation,negativeTerminalLocation)
    print('Iteration:final')
    test.print_table()
    print('---------------------------------------------------------')



start()



