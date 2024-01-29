The data is from Amanda, before the best model

Because the ic3 doesn't have any clue, so we duplicate data of ic9 to ic3. later we will use the other data to replace ic3.

Each folder should include 10 files:

Heat map:
1. con_hikerbf1_t11.csv			-> con_t11.csv

Clue heat map:
2. con_hiker_bf1_clue1.csv		-> con_clue1.csv
3. con_hiker_bf1_clue2.csv		-> con_clue2.csv
4. con_hiker_bf1_clue12.csv		-> con_clue12.csv
5. con_hiker_bf1_final.csv		-> con_final.csv

Trajctory:
6. traj_hiker_bf1.csv			-> traj.csv

Clue trajectory:
7. clue1index_hiker_bf1.csv		-> traj_clue1.csv
8. clue2index_hiker_bf1.csv		-> traj_clue2.csv
9. clue12index_hiker_bf1.csv		-> traj_clue12.csv
10. finalindex_hiker_bf1.csv		-> traj_final.csv


We have 1 training scenario, 8 experiment scenario
28 participants
each participants have 8 scenario
each participants have 4 visualization*2 duplicate

We need to counterbalance 8 scenario
we also need to counterbalance the 4 visualizations

4 8x8 latin square: pick 28 out of 32 scenario
14 4x4 latin square: 28 2x4 visualization

Visualization:
List after first shuffle: [[3, 1, 2, 0], [2, 0, 1, 3], [0, 1, 2, 3], [1, 0, 2, 3], [1, 3, 2, 0], [1, 0, 3, 2], [1, 2, 3, 0], [2, 1, 3, 0], [0, 2, 1, 3], [0, 2, 3, 1], [3, 2, 0, 1], [3, 1, 0, 2], [0, 1, 3, 2], [1, 3, 0, 2], [1, 2, 0, 3], [0, 3, 1, 2], [2, 3, 1, 0], [2, 1, 0, 3], [3, 0, 2, 1], [3, 2, 1, 0], [0, 3, 2, 1], [2, 3, 0, 1], [3, 0, 1, 2], [2, 0, 3, 1], [3, 2, 1, 0], [1, 0, 3, 2], [3, 1, 0, 2], [2, 1, 0, 3], [0, 1, 2, 3], [0, 2, 1, 3], [0, 1, 3, 2], [0, 3, 2, 1], [1, 3, 2, 0], [3, 0, 2, 1], [3, 2, 0, 1], [2, 3, 1, 0], [1, 2, 3, 0], [2, 1, 3, 0], [2, 0, 1, 3], [1, 3, 0, 2], [1, 0, 2, 3], [3, 0, 1, 2], [0, 3, 1, 2], [2, 0, 3, 1], [2, 3, 0, 1], [1, 2, 0, 3], [3, 1, 2, 0], [0, 2, 3, 1], [3, 2, 0, 1], [2, 3, 0, 1], [2, 0, 1, 3], [1, 0, 3, 2], [3, 2, 1, 0], [0, 3, 2, 1], [2, 1, 0, 3], [1, 2, 3, 0]]
size 56

scenariodetails, use LPMEXPS
koster10, use LPMEXPS2: ic 1,3,4,6,10,12,13,14 training: ic5
