from heapq import heappop, heappushimport mathdef find_path (source_point, destination_point, mesh):    sourceBox = None    destinationBox = None    for box in mesh["boxes"]:        x1, x2, y1, y2 = box        sx, sy = source_point        dx, dy = destination_point        if x1 <= sx < x2 and y1 <= sy < y2:            print("found source")            sourceBox = box        if x1 <= dx < x2 and y1 <= dy < y2:            print("found destination")            destinationBox = box    path = []    boxes = {}    if destinationBox is None or sourceBox is None:        print('No Path')        return path, boxes.keys()    # bfs    queue = []    heappush(queue, (0, sourceBox, 'D'))    heappush(queue, (0, destinationBox, 'S'))    # S->D parent boxes    parent_forward = dict()    parent_forward[sourceBox] = None    # D->S parent boxes    parent_backward = dict()    parent_backward[destinationBox] = None    #S->D distances via boxes    distances_forward = dict()    distances_forward[sourceBox] = 0    # D->S distances via boxes    distances_backward = dict()    distances_backward[destinationBox] = 0    # S -> D points via boxes    points_forward = dict()    points_forward[sourceBox] = source_point    # D -> S points via boxes    points_backward = dict()    points_backward[destinationBox] = destination_point    while queue:        current_dist, current_box, curr_goal = heappop(queue)        if curr_goal == 'D':            current_point = points_forward[current_box]        else:            current_point = points_backward[current_box]        # print(current_box)        if current_box in parent_backward and current_box in parent_forward:            s_d_curr = current_box            d_s_curr = current_box            while s_d_curr:                path.append(points_forward[s_d_curr])                if parent_forward[s_d_curr] is not None:                    if s_d_curr == parent_forward[parent_forward[s_d_curr]]:                        path.append(points_forward[s_d_curr])                        path.append(source_point)                        break                s_d_curr = parent_forward[s_d_curr]                print("on forward:", s_d_curr)            path.reverse()            while d_s_curr:                path.append(points_backward[d_s_curr])                if parent_backward[d_s_curr] is not None:                    if d_s_curr == parent_backward[parent_backward[d_s_curr]]:                        path.append(points_backward[d_s_curr])                        path.append(destination_point)                        break                d_s_curr = parent_backward[d_s_curr]                print("on backward: ", d_s_curr)            path.append(destination_point)            print(path)            break        else:            for adj in mesh["adj"][current_box]:                dx1, dx2, dy1, dy2 = adj                cx1, cx2, cy1, cy2 = current_box                line = []  # (x1, x2, y1, y2)                if cx1 == dx2:  # top                    if (dy2 - dy1) < (cy2 - cy1):  # destination is smaller                        line = [dx2, dx2, dy1, dy2]                    else:  # current is smaller                        line = [cx1, cx1, cy1, cy2]                elif cy1 == dy2:  # left                    if (dx2 - dx1) < (cx2 - cx1):  # destination is smaller                        line = [dx1, dx2, dy2, dy2]                    else:  # current is smaller                        line = [cx1, cx2, cy1, cy1]                elif cx2 == dx1:  # bottom                    if (dy2 - dy1) < (cy2 - cy1):  # destination is smaller                        line = [dx1, dx1, dy1, dy2]                    else:  # current is smaller                        line = [cx2, cx2, cy1, cy2]                elif cy2 == dy1:  # right                    if (dx2 - dx1) < (cx2 - cx1):  # destination is smaller                        line = [dx1, dx2, dy1, dy1]                    else:  # current is smaller                        line = [cx1, cx2, cy2, cy2]                        # print(line)                # calculate the line to L, R and mid                left_most = (line[0], line[2])                right_most = (line[1], line[3])                on_point = ()                if right_most[0] - left_most[0] == 0:  # x2 - x1 , horizontal                    if current_point[1] < left_most[1]:  # y < y1                        on_point = left_most                    elif current_point[1] > right_most[1]:                        on_point = right_most                    else:                        on_point = (right_most[0], current_point[1])                else:                    if current_point[0] < left_most[0]:  # x < x1                        on_point = left_most                    elif current_point[0] > right_most[0]:                        on_point = right_most                    else:                        on_point = (current_point[0], right_most[1])                dist = math.sqrt((current_point[0] - on_point[0]) ** 2 + (current_point[1] - on_point[1]) ** 2)  # calculates the distance                pathcost = current_dist + dist                if curr_goal == 'D':                    if adj not in parent_forward or pathcost < distances_forward[adj]:                        est_dist = math.sqrt((current_point[0] - destination_point[0]) ** 2 + (current_point[1] - destination_point[1]) ** 2)                        priority = current_dist + est_dist                        boxes[adj] = "visited"                        heappush(queue, (priority, adj, curr_goal))                        distances_forward[adj] = current_dist + dist                        points_forward[adj] = on_point                        parent_forward[adj] = current_box                else:                    if adj not in parent_backward or pathcost < distances_backward[adj]:                        est_dist = math.sqrt((current_point[0] - source_point[0]) ** 2 + (current_point[1] - source_point[1]) ** 2)                        priority = current_dist + est_dist                        boxes[adj] = "visited"                        heappush(queue, (priority, adj, curr_goal))                        distances_backward[adj] = current_dist + dist                        points_backward[adj] = on_point                        parent_backward[adj] = current_box    # print("source point:", source_point)    # print("destination point: ", destination_point)    # print('found solution: ', boxes)    if sourceBox == destinationBox:        path = [source_point, destination_point]        boxes[destinationBox] = 'visted'        return path, boxes.keys()    #path points and distance calc    # distance = {}    # current_point = destination_point    # for box in boxes:    #     if boxes[box] is None:    #         # we are at the origin    #         break    #     next_box = boxes[box]    #     dx1, dx2, dy1, dy2 = next_box    #     cx1, cx2, cy1, cy2 = box    #     line = []  # (x1, x2, y1, y2)    #     if cx1 == dx2:  # top    #         if (dy2 - dy1) < (cy2 - cy1):  # destination is smaller    #             line = [dx2, dx2, dy1, dy2]    #         else:  # current is smaller    #             line = [cx1, cx1, cy1, cy2]    #     elif cy1 == dy2:  # left    #         if (dx2 - dx1) < (cx2 - cx1):  # destination is smaller    #             line = [dx1,  dx2, dy2, dy2]    #         else:  # current is smaller    #             line = [cx1, cx2, cy1, cy1]    #     elif cx2 == dx1:  # bottom    #         if (dy2 - dy1) < (cy2 - cy1):  # destination is smaller    #             line = [dx1, dx1, dy1, dy2]    #         else:  # current is smaller    #             line = [cx2, cx2, cy1, cy2]    #     elif cy2 == dy1:  # right    #         if (dx2 - dx1) < (cx2 - cx1): # destination is smaller    #             line = [dx1, dx2, dy1, dy1]    #         else:  # current is smaller    #             line = [cx1, cx2, cy2, cy2]    #    #             # print(line)    #     # calculate the line to L, R and mid    #     left_most = (line[0], line[2])    #     right_most = (line[1], line[3])    #     on_point = ()    #     if right_most[0] - left_most[0] == 0: # x2 - x1 , horizontal    #         if current_point[1] < left_most[1]: # y < y1    #             on_point = left_most    #         elif current_point[1] > right_most[1]:    #             on_point = right_most    #         else:    #             on_point = (right_most[0], current_point[1])    #     else:    #         if current_point[0] < left_most[0]: # x < x1    #             on_point = left_most    #         elif current_point[0] > right_most[0]:    #             on_point = right_most    #         else:    #             on_point = (current_point[0], right_most[1])    #     points[box] = on_point    #     path.append(on_point)    #     print(current_point, on_point)    #     dist = math.sqrt((current_point[0] - on_point[0])**2 + (current_point[1] - on_point[1])**2)  # calculates the distance    #     distance[box] = dist    #     print(dist)    #     current_point # x,y coord in current box    """    Searches for a path from source_point to destination_point through the mesh    Args:        source_point: starting point of the pathfinder        destination_point: the ultimate goal the pathfinder must reach        mesh: pathway constraints the path adheres to    Returns:        A path (list of points) from source_point to destination_point if exists        A list of boxes explored by the algorithm    """    if len(path) is 0:        print("No path")    return path, boxes.keys()