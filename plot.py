import read_map
import BFS.bfs
import main
import matplotlib.pyplot as plt
import time

x, y_EA, y_BFS = [], [], []
for dimension in range(1000,1500,40):
    # increase dimension of map step by step
    read_map.make_map(dimension,dimension)

    x.append(dimension)

    # record time for EA
    EA_start_time = time.time()
    main.main()
    EA_end_time = time.time()
    EA_runtime = EA_end_time - EA_start_time
    y_EA.append(EA_runtime)

    # record time for BFS
    BFS_start_time = time.time()
    BFS.bfs.bfs()
    BFS_end_time = time.time()
    BFS_runtime = BFS_end_time - BFS_start_time
    y_BFS.append(BFS_runtime)

    print("now dimension is",dimension)

# plot the figure
upper_bound = max(max(y_BFS),max(y_EA))
plt.plot(x, y_BFS,'r',x,y_EA,'b')
plt.axis([1000, 1510, 0, upper_bound])
plt.savefig( 'compare.png')
plt.show()