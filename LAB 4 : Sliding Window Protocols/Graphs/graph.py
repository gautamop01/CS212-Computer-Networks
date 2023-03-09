
# importing the required module
import matplotlib.pyplot as plt
  
# x axis values - pl
x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
# corresponding y axis values - time
y = [2993,	4002, 6254, 7402, 9955, 13918, 17788, 27244, 56137]
  
# plotting the points 
plt.plot(x, y)
  
plt.xlabel('Probability of Loss')
plt.ylabel('Time Taken')
  
# giving a title to my graph
plt.title('Time Taken v/s Pl')
  
# function to show the plot
plt.show()