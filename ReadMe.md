![example](1.png)
On the left, a path is calculated given the maze image on the right. Red represents the start point, and blue represents the target. The dimensions are 20x17.


environment.py the environment simulation os map<br/>
evo_algo.py evolution algorithm body<br/>
ground.py EA runs on a flat ground map without obstackles<br/>
main.py run EA<br/>
plot.py run EA and Breadth-First Search and plot the runtime<br/>
read_map.py transform a image map into a nest list, store them in *.npy files<br/>
<br/>
BFS/ BFS algorithm<br/>
map/01/ the map that simulates a real world scenario with obstackles<br/>
map/02/ the map that simulates a maze<br/>
<br/>
start_state.npy start-position<br/>
destination_state.npy destination-position<br/>
map_table.npy map data<br/>
<br/>

technical report is here:\
https://github.com/bsyh/path-planing-using-EA/blob/main/report.pdf

