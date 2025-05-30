from sortedcontainers import SortedList

sorted_list = SortedList([1, 2, 4, 4, 6])
idx_1 = sorted_list.bisect_left(4)
idx_2 = sorted_list.bisect_right(4)
print(idx_1, idx_2)  # Output: 2 4
    
intervals = [[-26367, 21713], [78364, 83654], [47452, 59227], [-83978, -34722], [74215, 79227], [1812, 65107], [-31597, 41895], [8636, 82430], [67919, 95584], [-44569, 37990], [79819, 99497], [28331, 55617], [-18128, 72897], [61814, 78044], [2440, 4423], [32765, 61916], [42496, 50186], [16490, 33361], [-26304, 9388], [-62841, -3270], [-41330, 76055], [-43214, 68229], [-52601, -32695], [-26387, 64343], [61192, 86796], [-75595, 23210], [-3826, 1139], [-7564, 44389], [-18247, 89663], [28995, 29185], [60554, 96221], [-10587, 99261], [-87316, 4111], [-40934, 60964], [62138, 92657], [-14583, 47602], [25061, 90809], [74122, 83820], [10659, 69965], [90119, 94561], [83797, 90504], [44430, 76428], [83907, 92696], [79148, 97120], [-22021, 57582], [-22629, -8797], [2774, 48966], [-5778, 95115], [24459, 52959], [20593, 25164], [22240, 90392], [49717, 99051], [-89765, 86778], [-29899, 11738], [76429, 79453], [28674, 61144], [-54707, 95606], [-93222, -6289], [-39862, 24936], [-68719, 40602], [93969, 99437], [-12293, -273], [-47586, 91070], [63875, 65188], [-1244, 1440], [69510, 97699], [-82435, -77785], [47266, 57577], [-5025, 77779], [52664, 67737], [-3504, 23360], [15136, 58349], [-96109, -3254], [-69406, -3392], [-44483, 81638], [95414, 99689], [13761, 24815], [-75733, 82493], [23789, 49062], [-31364, -28487], [90111, 97485], [84890, 94093], [19548, 36761], [-2563, 13012], [-28270, 67066], [82810, 97972], [81659, 90563], [74911, 99170], [-79638, 660], [-9735, 81792], [-4051, 42956], [60991, 86725], [9343, 26954], [-63627, 14407], [-77607, 58896], [3530, 41372], [-53699, 57154], [89860, 92305], [-86482, 62405], [3950, 26476]]
sorted_list_lists = SortedList(intervals)

start = -96886
end = -58886
idx_l = sorted_list_lists.bisect_left([start, 0]) -1  # position of the first element smaller then start
idx_r = sorted_list_lists.bisect_right([end, 0])
print(f'idx_l = {idx_l}')
print(f'idx_r = {idx_r}')


idx_l = 0 if idx_l < 0 else idx_l
idx_r = -2 if idx_r > len(sorted_list_lists) else idx_r
print(f'idx_l = {idx_l}')
print(f'interval[{idx_l}] = {sorted_list_lists[idx_l]}')
print(f'idx_r = {idx_r}')
print(f'interval[{idx_r}] = {sorted_list_lists[idx_r]}')