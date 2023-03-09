
# importing the required module
import matplotlib.pyplot as plt
  
# x axis values - pl
x = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]
# corresponding y axis values - time
y = [153.22, 152.70, 155.53, 158.16, 162.72, 170.37, 175.46, 185.05, 194.52]
  
# plotting the points 
plt.plot(x, y)
  
plt.xlabel('Probability of Loss')
plt.ylabel('% of Channel Utilization')
  
# giving a title to my graph
plt.title('% of Channel Utilization V/s Pl')
  
# function to show the plot
plt.show()