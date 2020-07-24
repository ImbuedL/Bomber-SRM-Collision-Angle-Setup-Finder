"""
 
EDIT THE INFORMATION AT THE BOTTOM
 
- CODE CURRENTLY ASSUMES MAX OF 15 ESS TURNS ALLOWED (can easily edit this by changing Max_ESS_Count hardcoded in find_ranked_collision_solutions() function)
- SIDEHOPS ARE NOT FULLY IMPLEMENTED YET
 
"""
 
 
def sortFirst(val):
    return val[0]  
 
 
def col(normal_vector_angle, movement_angle):
   
   
    """
   
   This function takes the normal_vector_angle of a wall and the movement_angle
   that you collided into it with and returns the collision angle that you get
   by moving into it with this movement angle
   
   """
 
   
    angle_diff = abs(normal_vector_angle - movement_angle)
   
    if angle_diff > 0x8000:
               
        collision_angle = abs(0x10000 - angle_diff )
        print(hex(collision_angle))
               
    elif angle_diff <= 0x8000 and angle_diff >= 0:
                   
        collision_angle = angle_diff
        print(hex(collision_angle))
                   
    else:
        print("UHHHHHHHH??????")
       
    return
 
 
def find_goal_collision_angles_40_bit(value_string):
   
    # if seahorse, then value_string = '0x24', for example
   
    """
   
   This function gives us the goal collision angles for a given item that needs
   the 0x40 bit to be 0
   
   """
   
    if len(value_string) != 4 or value_string[0] != '0':
        print('invalid input into find_goal_collision_angles() function')
   
    seahorse_list = []
    for i in range(256):
        string = hex(i)
        if len(string) == 3:
            new_string = '0x0' + string[2]
        elif len(string) == 4:
            new_string = string
        else:
            print("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!???????????????????????????")
       
        collision_value = value_string + new_string[2:4]
       
        if len(collision_value) != 6:
            print(collision_value)
       
        # If the 0x40 bit is 0, then add the value:
        if collision_value[4] != '4' and collision_value[4] != '5' and collision_value[4] != '6' and collision_value[4] != '7' and collision_value[4] != 'c' and collision_value[4] != 'd' and collision_value[4] != 'e' and collision_value[4] != 'f':
            seahorse_list.append(int(collision_value, 16))
            #seahorse_list.append(collision_value)
    if len(seahorse_list) != 128:
        print("??????????????")
   
    return seahorse_list
 
 
def find_goal_collision_angles_20_bit(value_string):
   
    # if seahorse, then value_string = '0x24', for example
   
    """
   
   This function gives us the goal collision angles for a given item that needs
   the 0x20 bit to be 0
   
   """
   
    if len(value_string) != 4 or value_string[0] != '0':
        print('invalid input into find_goal_collision_angles() function')
   
    seahorse_list = []
    for i in range(256):
        string = hex(i)
        if len(string) == 3:
            new_string = '0x0' + string[2]
        elif len(string) == 4:
            new_string = string
        else:
            print("ERROR!!!!!!!!!!!!!!!!!!!!!!!!!!!???????????????????????????")
       
        collision_value = value_string + new_string[2:4]
       
        if len(collision_value) != 6:
            print(collision_value)
       
        # If the 0x20 bit is 0, then add the value:
        if collision_value[4] != '2' and collision_value[4] != '3' and collision_value[4] != '6' and collision_value[4] != '7' and collision_value[4] != 'a' and collision_value[4] != 'b' and collision_value[4] != 'e' and collision_value[4] != 'f':
            seahorse_list.append(int(collision_value, 16))
            #seahorse_list.append(collision_value)
    if len(seahorse_list) != 128:
        print("??????????????")
   
    return seahorse_list
 
 
def find_valid_goal_angles(goal_collision_angle_list, normal_vector_angle_list):
   
    """
   
   a normal vector angle is the angle you get by targeting a given wall
   
   
   This function takes a list of normal vector angles and a list of goal collision
   angles and returns a list of all in the form (goal_angle, normal_angle, goal_collision_angle)
   where goal_angle is an angle that can be used to collide into a wall with a normal vector angle
   of normal_angle to get a collision angle of goal_collision_angle
   
   """
   
    valid_goal_angle_list = []
   
    for normal_vector_angle in normal_vector_angle_list:
        for i in range(65536):
           
            angle_diff = abs(normal_vector_angle - i)
           
            if angle_diff > 0x8000:
           
                collision_angle = abs(0x10000 - angle_diff )
           
            elif angle_diff <= 0x8000 and angle_diff >= 0:
               
                collision_angle = angle_diff
               
            else:
                print("UHHHHHHHH??????")
           
            if collision_angle in goal_collision_angle_list:
               
                valid_goal_angle_list.append((i, normal_vector_angle, collision_angle))
               
   
    return valid_goal_angle_list
 
###############################################################################
 
def right_sidehop_angles(angle, camera_angle):
   
    angle_list = []
   
    cardinal_list = [(camera_angle - 0xC000)%(0x10000), (camera_angle - 0x8000)%(0x10000), (camera_angle - 0x4000)%(0x10000), camera_angle]
   
    cardinal_list.sort()
   
    ################# Find Nearest Cardinal (the one movement snaps to)
   
    initial_sidehop_angle = (angle - 0x4000)%(0x10000)
   
    diff_list = []
    for cardinal_angle in cardinal_list:
        diff_list.append(abs((initial_sidehop_angle - cardinal_angle)%(0x10000)))
       
    min_diff = min(diff_list)
   
    if min_diff != 0x2000:
        for cardinal_angle in cardinal_list:
            if abs((initial_sidehop_angle - cardinal_angle)%(0x10000)) == min_diff:
                nearest_cardinal = cardinal_angle
    elif min_diff == 0x2000:
        closest_list = []
        for cardinal_angle in cardinal_list:
            if abs((initial_sidehop_angle - cardinal_angle)%(0x10000)) == min_diff:
                closest_list.append(cardinal_angle)
       
       
        # subtract 1 to break the tie (we want the lower one)
        new_diff_list = []
        for cardinal_angle in closest_list:
            new_diff_list.append(abs((initial_sidehop_angle - 1 - cardinal_angle)%(0x10000)))
           
        new_min_diff = min(new_diff_list)
       
        for cardinal_angle in closest_list:
            if abs((initial_sidehop_angle - 1 - cardinal_angle)%(0x10000)) == new_min_diff:
                nearest_cardinal = cardinal_angle
       
    ###########################################################################
   
    nearest_cardinal_index = cardinal_list.index(nearest_cardinal)
   
    # TAP SIDEHOP
    # 1 frame window
    angle_list.append((initial_sidehop_angle + 5*0x12C)%(0x10000))
   
   
   
    # 1 Frame Hold Sidehop
    if abs((initial_sidehop_angle - nearest_cardinal)%(0x10000)) <= 0x12C:
       
        # 1 frame window
        angle_list.append((nearest_cardinal + 4*0x12C)%(0x10000))
       
    elif abs((initial_sidehop_angle - nearest_cardinal)%(0x10000)) > 0x12C:
       
        if nearest_cardinal_index != 3:
       
            if initial_sidehop_angle > nearest_cardinal:
               
                # 1 frame window
                angle_list.append((initial_sidehop_angle - 0x12C + 4*0x012C)%(0x10000))
   
            elif initial_sidehop_angle < nearest_cardinal:
               
                # 1 frame window
                angle_list.append((initial_sidehop_angle + 0x12C + 4*0x012C)%(0x10000))
               
        elif nearest_cardinal_index == 3:
           
            if initial_sidehop_angle > nearest_cardinal or initial_sidehop_angle < cardinal_list[0]:
               
                # 1 frame window
                angle_list.append((initial_sidehop_angle - 0x12C + 4*0x012C)%(0x10000))
           
            elif initial_sidehop_angle < nearest_cardinal and initial_sidehop_angle > cardinal_list[2]:
               
                # 1 frame window
                angle_list.append((initial_sidehop_angle + 0x12C + 4*0x012C)%(0x10000))
               
               
               
               
   
    # 2 Frame Hold Sidehop
    if abs((initial_sidehop_angle - nearest_cardinal)%(0x10000)) <= 0x12C:
       
        # 1 frame window
        angle_list.append((nearest_cardinal + 3*0x12C)%(0x10000))
       
    elif abs((initial_sidehop_angle - nearest_cardinal)%(0x10000)) > 0x12C:
       
        if nearest_cardinal_index != 3:
           
       
            if initial_sidehop_angle > nearest_cardinal:
               
                if abs(((initial_sidehop_angle - 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) <= 0x12C:
                   
                    # 1 frame window
                    angle_list.append((nearest_cardinal + 3*0x12C)%(0x10000))
               
                elif abs(((initial_sidehop_angle - 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) > 0x12C:
               
                    # 1 frame window
                    angle_list.append((initial_sidehop_angle - 2*0x12C + 3*0x012C)%(0x10000))
   
            elif initial_sidehop_angle < nearest_cardinal:
               
                if abs(((initial_sidehop_angle + 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) <= 0x12C:
                   
                    # 1 frame window
                    angle_list.append((nearest_cardinal + 3*0x12C)%(0x10000))
               
                elif abs(((initial_sidehop_angle + 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) > 0x12C:
               
                    # 1 frame window
                    angle_list.append((initial_sidehop_angle + 2*0x12C + 3*0x012C)%(0x10000))
               
               
        elif nearest_cardinal_index == 3:
           
            if initial_sidehop_angle > nearest_cardinal or initial_sidehop_angle < cardinal_list[0]:
               
                if abs(((initial_sidehop_angle - 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) <= 0x12C:
                   
                    # 1 frame window
                    angle_list.append((nearest_cardinal + 3*0x12C)%(0x10000))
               
                elif abs(((initial_sidehop_angle - 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) > 0x12C:
               
                    # 1 frame window
                    angle_list.append((initial_sidehop_angle - 2*0x12C + 3*0x012C)%(0x10000))
               
           
            elif initial_sidehop_angle < nearest_cardinal and initial_sidehop_angle > cardinal_list[2]:
               
                if abs(((initial_sidehop_angle + 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) <= 0x12C:
                   
                    # 1 frame window
                    angle_list.append((nearest_cardinal + 3*0x12C)%(0x10000))
               
                elif abs(((initial_sidehop_angle + 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) > 0x12C:
               
                    # 1 frame window
                    angle_list.append((initial_sidehop_angle + 2*0x12C + 3*0x012C)%(0x10000))
     
    """
 
   TODO
 
   """            
               
    # 3 frame hold sidehop
   
    # 4 frame hold sidehop
   
    # 5 frame hold sidehop (true hold sidehop)
               
   
    return angle_list
 
 
###############################################################################
   
def left_sidehop_angles(angle, camera_angle):
   
    angle_list = []
   
    cardinal_list = [(camera_angle - 0xC000)%(0x10000), (camera_angle - 0x8000)%(0x10000), (camera_angle - 0x4000)%(0x10000), camera_angle]
   
    cardinal_list.sort()
   
    ################# Find Nearest Cardinal (the one movement snaps to)
   
    initial_sidehop_angle = (angle - 0x4000)%(0x10000)
   
    diff_list = []
    for cardinal_angle in cardinal_list:
        diff_list.append(abs((initial_sidehop_angle - cardinal_angle)%(0x10000)))
       
    min_diff = min(diff_list)
   
    if min_diff != 0x2000:
        for cardinal_angle in cardinal_list:
            if abs((initial_sidehop_angle - cardinal_angle)%(0x10000)) == min_diff:
                nearest_cardinal = cardinal_angle
    elif min_diff == 0x2000:
        closest_list = []
        for cardinal_angle in cardinal_list:
            if abs((initial_sidehop_angle - cardinal_angle)%(0x10000)) == min_diff:
                closest_list.append(cardinal_angle)
       
       
        # subtract 1 to break the tie (we want the lower one)
        new_diff_list = []
        for cardinal_angle in closest_list:
            new_diff_list.append(abs((initial_sidehop_angle - 1 - cardinal_angle)%(0x10000)))
           
        new_min_diff = min(new_diff_list)
       
        for cardinal_angle in closest_list:
            if abs((initial_sidehop_angle - 1 - cardinal_angle)%(0x10000)) == new_min_diff:
                nearest_cardinal = cardinal_angle
       
    ###########################################################################
   
    nearest_cardinal_index = cardinal_list.index(nearest_cardinal)
   
    # TAP SIDEHOP
    # 1 frame window
    angle_list.append((initial_sidehop_angle - 5*0x12C)%(0x10000))
   
   
   
    # 1 Frame Hold Sidehop
    if abs((initial_sidehop_angle - nearest_cardinal)%(0x10000)) <= 0x12C:
       
        # 1 frame window
        angle_list.append((nearest_cardinal - 4*0x12C)%(0x10000))
       
    elif abs((initial_sidehop_angle - nearest_cardinal)%(0x10000)) > 0x12C:
       
        if nearest_cardinal_index != 3:
       
            if initial_sidehop_angle > nearest_cardinal:
               
                # 1 frame window
                angle_list.append((initial_sidehop_angle - 0x12C - 4*0x012C)%(0x10000))
   
            elif initial_sidehop_angle < nearest_cardinal:
               
                # 1 frame window
                angle_list.append((initial_sidehop_angle + 0x12C - 4*0x012C)%(0x10000))
               
        elif nearest_cardinal_index == 3:
           
            if initial_sidehop_angle > nearest_cardinal or initial_sidehop_angle < cardinal_list[0]:
               
                # 1 frame window
                angle_list.append((initial_sidehop_angle - 0x12C - 4*0x012C)%(0x10000))
           
            elif initial_sidehop_angle < nearest_cardinal and initial_sidehop_angle > cardinal_list[2]:
               
                # 1 frame window
                angle_list.append((initial_sidehop_angle + 0x12C - 4*0x012C)%(0x10000))
               
               
               
               
   
    # 2 Frame Hold Sidehop
    if abs((initial_sidehop_angle - nearest_cardinal)%(0x10000)) <= 0x12C:
       
        # 1 frame window
        angle_list.append((nearest_cardinal - 3*0x12C)%(0x10000))
       
    elif abs((initial_sidehop_angle - nearest_cardinal)%(0x10000)) > 0x12C:
       
        if nearest_cardinal_index != 3:
           
       
            if initial_sidehop_angle > nearest_cardinal:
               
                if abs(((initial_sidehop_angle - 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) <= 0x12C:
                   
                    # 1 frame window
                    angle_list.append((nearest_cardinal - 3*0x12C)%(0x10000))
               
                elif abs(((initial_sidehop_angle - 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) > 0x12C:
               
                    # 1 frame window
                    angle_list.append((initial_sidehop_angle - 2*0x12C - 3*0x012C)%(0x10000))
   
            elif initial_sidehop_angle < nearest_cardinal:
               
                if abs(((initial_sidehop_angle + 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) <= 0x12C:
                   
                    # 1 frame window
                    angle_list.append((nearest_cardinal - 3*0x12C)%(0x10000))
               
                elif abs(((initial_sidehop_angle + 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) > 0x12C:
               
                    # 1 frame window
                    angle_list.append((initial_sidehop_angle + 2*0x12C - 3*0x012C)%(0x10000))
               
               
        elif nearest_cardinal_index == 3:
           
            if initial_sidehop_angle > nearest_cardinal or initial_sidehop_angle < cardinal_list[0]:
               
                if abs(((initial_sidehop_angle - 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) <= 0x12C:
                   
                    # 1 frame window
                    angle_list.append((nearest_cardinal - 3*0x12C)%(0x10000))
               
                elif abs(((initial_sidehop_angle - 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) > 0x12C:
               
                    # 1 frame window
                    angle_list.append((initial_sidehop_angle - 2*0x12C - 3*0x012C)%(0x10000))
               
           
            elif initial_sidehop_angle < nearest_cardinal and initial_sidehop_angle > cardinal_list[2]:
               
                if abs(((initial_sidehop_angle + 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) <= 0x12C:
                   
                    # 1 frame window
                    angle_list.append((nearest_cardinal - 3*0x12C)%(0x10000))
               
                elif abs(((initial_sidehop_angle + 0x12C)%(0x10000) - nearest_cardinal)%(0x10000)) > 0x12C:
               
                    # 1 frame window
                    angle_list.append((initial_sidehop_angle + 2*0x12C - 3*0x012C)%(0x10000))
     
    """
 
   TODO
 
   """            
               
    # 3 frame hold sidehop
   
    # 4 frame hold sidehop
   
    # 5 frame hold sidehop (true hold sidehop)
               
   
    return angle_list
 
 
 
 
###############################################################################
 
def find_ranked_collision_solutions(initial_angle_list, camera_angle, goal_angle_list, filename):
   
    """
   
   The idea is to have goal_angle_list = find_valid_goal_angles(find_goal_collision_angles('0x24'), oceanside_room4_normal_vector_angle_list)
   if doing seahorse (item 0x24)
   
   It is assumed that initial_angle_list = [initial_angle, short_chest_angle] (would be extremely easy to change this but I see no point atm)
   
   """
   
    Max_ESS_Count = 15
   
    cardinal_list = [(camera_angle - 0xC000)%(0x10000), (camera_angle - 0x8000)%(0x10000), (camera_angle - 0x4000)%(0x10000), camera_angle]
 
   
    walk_angle_list = []
   
    # add all directions from walking to the initial angle list
    for cardinal_angle in cardinal_list:
        for i in range(5):
            walk_angle_list.append((cardinal_angle + (i+1)*0xBB8)%(0x10000) )
            walk_angle_list.append((cardinal_angle - (i+1)*0xBB8)%(0x10000) )
           
   
    #initial_angle_list_list = [initial_angle_list, cardinal_list, walk_angle_list]        
   
   
    # add all 4 cardinal directions and all walk angles to the initial angle list
    #initial_angle_list = initial_angle_list + cardinal_list + walk_angle_list        
   
    # for angles in initial_angle_list (namely initial angle and short chest cs angle and wall angles)
    solution_list = []
    cup_solution_list = []
    sidehop_solution_list = []
   
   
    # for angles in cardinal_list
    solution_list_cardinal = []
    cup_solution_list_cardinal = []
    sidehop_solution_list_cardinal = []
   
    # for angles in walk_angle_list
    solution_list_walk = []
    cup_solution_list_walk = []
    sidehop_solution_list_walk = []
   
   
    with open(filename, "a") as file:
       
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
   
        for initial_angle in initial_angle_list:
           
            print(hex(initial_angle))
           
            if initial_angle > 65535 or initial_angle < 0 or isinstance(initial_angle, int) == False:
                print('Error: The initial angle is not a valid input')
           
            #for i in range(8192):
            for i in range(Max_ESS_Count):
                for entry in goal_angle_list:
                   
                    angle = entry[0]
                    normal_vector_angle = entry[1]
                    collision_angle = entry[2]
                   
                    if (initial_angle + i*1800)%65536 == angle:
                        solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', ''))
                       
                    if (initial_angle - i*1800)%65536 == angle:
                        solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', ''))
 
                    if (initial_angle + 0x12C + i*1800)%65536 == angle:
                        cup_solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '1 c-up (target) Left and', ''))
                   
                    if (initial_angle + 0x12C - i*1800)%65536 == angle:
                        cup_solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '1 c-up (target) Left and', ''))
 
                    if (initial_angle - 0x12C + i*1800)%65536 == angle:
                        cup_solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '1 c-up (target) Right and', ''))
                   
                    if (initial_angle - 0x12C - i*1800)%65536 == angle:
                        cup_solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '1 c-up (target) Right and', ''))
                       
                    if (initial_angle + 0x3C0 + i*1800)%65536 == angle:
                        cup_solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '1 c-up (no target) Left and', ''))
                   
                    if (initial_angle + 0x3C0 - i*1800)%65536 == angle:
                        cup_solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '1 c-up (no target) Left and', ''))
 
                    if (initial_angle - 0x3C0 + i*1800)%65536 == angle:
                        cup_solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '1 c-up (no target) Right and', ''))
                   
                    if (initial_angle - 0x3C0 - i*1800)%65536 == angle:
                        cup_solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '1 c-up (no target) Right and', ''))
 
                    ##### Here I am hard coding in the walls from bomber's hideout to allow which walls you can sidehop into
                   
                    for right_sidehop_angle in right_sidehop_angles((initial_angle - i*1800)%(0x10000), camera_angle):
                       
                        if 0x0000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x4000:
                       
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                               
                        elif 0x4000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x8000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                       
                        elif 0x8000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0xC000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
       
                        elif 0xC000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x10000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                       
                        ###
                       
                        if 0x0000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x4000:
                       
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                               
                        elif 0x4000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x8000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                       
                        elif 0x8000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0xC000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
       
                        elif 0xC000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x10000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                       
                ###### Now Left Sidehops
                   
                    for left_sidehop_angle in left_sidehop_angles((initial_angle - i*1800)%(0x10000), camera_angle):
                       
                        if 0x0000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x4000:
                       
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x4000 or normal_vector_angle == 0x8000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                               
                        elif 0x4000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x8000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                       
                        elif 0x8000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0xC000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
       
                        elif 0xC000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x10000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                   
                        ###
                       
                    for left_sidehop_angle in left_sidehop_angles((initial_angle + i*1800)%(0x10000), camera_angle):
                       
                        if 0x0000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x4000:
                       
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x4000 or normal_vector_angle == 0x8000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                               
                        elif 0x4000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x8000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                       
                        elif 0x8000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0xC000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
       
                        elif 0xC000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x10000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
       
        ##### Now sort and then write to file
       
       
        solution_list.sort(key=sortFirst)
        cup_solution_list.sort(key=sortFirst)
        sidehop_solution_list.sort(key=sortFirst)
       
        file.write("------------------------------------------------------------------------------------------------------------------------ SETUPS USING: initial_angle OR short_chest_angle OR wall angle\n")
        file.write("----- SETUPS WITHOUT c-up OR sidehops\n")
       
        for entry in solution_list:
           
            # if (entry[1] in walk_list) == True:
           
            #file.write("%d = %s is a working initial angle with %d %s ESS turns for goal angle %d = %s\n" %(entry[1], hex(entry[1]), entry[0], entry[3], entry[2], hex(entry[2])))
            file.write("%s is a working initial angle with %s %d %s ESS turns %s for a goal angle of %s which can collide into a wall with normal vector angle %s to get collision angle %s\n" %(hex(entry[1]), entry[6], entry[0], entry[3], entry[7], hex(entry[2]), hex(entry[4]), hex(entry[5])))
       
        file.write("------------------------------------------------------------------------------------------\n")
        file.write("----- SETUPS WITH c-up\n")
       
        for entry in cup_solution_list:
           
            # if (entry[1] in walk_list) == True:
           
            #file.write("%d = %s is a working initial angle with %d %s ESS turns for goal angle %d = %s\n" %(entry[1], hex(entry[1]), entry[0], entry[3], entry[2], hex(entry[2])))
            file.write("%s is a working initial angle with %s %d %s ESS turns %s for a goal angle of %s which can collide into a wall with normal vector angle %s to get collision angle %s\n" %(hex(entry[1]), entry[6], entry[0], entry[3], entry[7], hex(entry[2]), hex(entry[4]), hex(entry[5])))
       
        file.write("------------------------------------------------------------------------------------------\n")
        file.write("----- SETUPS WITH sidehops\n")
       
        for entry in sidehop_solution_list:
           
            # if (entry[1] in walk_list) == True:
           
            #file.write("%d = %s is a working initial angle with %d %s ESS turns for goal angle %d = %s\n" %(entry[1], hex(entry[1]), entry[0], entry[3], entry[2], hex(entry[2])))
            file.write("%s is a working initial angle with %s %d %s ESS turns %s for a goal angle of %s which can collide into a wall with normal vector angle %s to get collision angle %s\n" %(hex(entry[1]), entry[6], entry[0], entry[3], entry[7], hex(entry[2]), hex(entry[4]), hex(entry[5])))
       
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
       
       
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
   
        for initial_angle in cardinal_list:
           
            print(hex(initial_angle))
           
            if initial_angle > 65535 or initial_angle < 0 or isinstance(initial_angle, int) == False:
                print('Error: The initial angle is not a valid input')
           
            #for i in range(8192):
            for i in range(Max_ESS_Count):
                for entry in goal_angle_list:
                   
                    angle = entry[0]
                    normal_vector_angle = entry[1]
                    collision_angle = entry[2]
                   
                    if (initial_angle + i*1800)%65536 == angle:
                        solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', ''))
                       
                    if (initial_angle - i*1800)%65536 == angle:
                        solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', ''))
 
                    if (initial_angle + 0x12C + i*1800)%65536 == angle:
                        cup_solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '1 c-up (target) Left and', ''))
                   
                    if (initial_angle + 0x12C - i*1800)%65536 == angle:
                        cup_solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '1 c-up (target) Left and', ''))
 
                    if (initial_angle - 0x12C + i*1800)%65536 == angle:
                        cup_solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '1 c-up (target) Right and', ''))
                   
                    if (initial_angle - 0x12C - i*1800)%65536 == angle:
                        cup_solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '1 c-up (target) Right and', ''))
                       
                    if (initial_angle + 0x3C0 + i*1800)%65536 == angle:
                        cup_solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '1 c-up (no target) Left and', ''))
                   
                    if (initial_angle + 0x3C0 - i*1800)%65536 == angle:
                        cup_solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '1 c-up (no target) Left and', ''))
 
                    if (initial_angle - 0x3C0 + i*1800)%65536 == angle:
                        cup_solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '1 c-up (no target) Right and', ''))
                   
                    if (initial_angle - 0x3C0 - i*1800)%65536 == angle:
                        cup_solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '1 c-up (no target) Right and', ''))
 
                    ##### Here I am hard coding in the walls from bomber's hideout to allow which walls you can sidehop into
                   
                    for right_sidehop_angle in right_sidehop_angles((initial_angle - i*1800)%(0x10000), camera_angle):
                       
                        if 0x0000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x4000:
                       
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                               
                        elif 0x4000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x8000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                       
                        elif 0x8000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0xC000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
       
                        elif 0xC000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x10000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                       
                        ###
                       
                        if 0x0000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x4000:
                       
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                               
                        elif 0x4000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x8000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                       
                        elif 0x8000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0xC000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
       
                        elif 0xC000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x10000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                       
                ###### Now Left Sidehops
                   
                    for left_sidehop_angle in left_sidehop_angles((initial_angle - i*1800)%(0x10000), camera_angle):
                       
                        if 0x0000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x4000:
                       
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x4000 or normal_vector_angle == 0x8000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                               
                        elif 0x4000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x8000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                       
                        elif 0x8000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0xC000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
       
                        elif 0xC000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x10000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                   
                        ###
                       
                    for left_sidehop_angle in left_sidehop_angles((initial_angle + i*1800)%(0x10000), camera_angle):
                       
                        if 0x0000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x4000:
                       
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x4000 or normal_vector_angle == 0x8000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                               
                        elif 0x4000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x8000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                       
                        elif 0x8000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0xC000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
       
                        elif 0xC000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x10000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list_cardinal.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
       
        ##### Now sort and then write to file
       
       
        solution_list_cardinal.sort(key=sortFirst)
        cup_solution_list_cardinal.sort(key=sortFirst)
        sidehop_solution_list_cardinal.sort(key=sortFirst)
       
        file.write("------------------------------------------------------------------------------------------\n")
        file.write("------------------------------------------------------------------------------------------------------------------------ SETUPS USING: cardinal directions (based on camera_angle)\n")
        file.write("----- SETUPS WITHOUT c-up OR sidehops\n")
       
        for entry in solution_list_cardinal:
           
            # if (entry[1] in walk_list) == True:
           
            #file.write("%d = %s is a working initial angle with %d %s ESS turns for goal angle %d = %s\n" %(entry[1], hex(entry[1]), entry[0], entry[3], entry[2], hex(entry[2])))
            file.write("%s is a working initial angle with %s %d %s ESS turns %s for a goal angle of %s which can collide into a wall with normal vector angle %s to get collision angle %s\n" %(hex(entry[1]), entry[6], entry[0], entry[3], entry[7], hex(entry[2]), hex(entry[4]), hex(entry[5])))
       
        file.write("------------------------------------------------------------------------------------------\n")
        file.write("----- SETUPS WITH c-up\n")
       
        for entry in cup_solution_list_cardinal:
           
            # if (entry[1] in walk_list) == True:
           
            #file.write("%d = %s is a working initial angle with %d %s ESS turns for goal angle %d = %s\n" %(entry[1], hex(entry[1]), entry[0], entry[3], entry[2], hex(entry[2])))
            file.write("%s is a working initial angle with %s %d %s ESS turns %s for a goal angle of %s which can collide into a wall with normal vector angle %s to get collision angle %s\n" %(hex(entry[1]), entry[6], entry[0], entry[3], entry[7], hex(entry[2]), hex(entry[4]), hex(entry[5])))
       
        file.write("------------------------------------------------------------------------------------------\n")
        file.write("----- SETUPS WITH sidehops\n")
       
        for entry in sidehop_solution_list_cardinal:
           
            # if (entry[1] in walk_list) == True:
           
            #file.write("%d = %s is a working initial angle with %d %s ESS turns for goal angle %d = %s\n" %(entry[1], hex(entry[1]), entry[0], entry[3], entry[2], hex(entry[2])))
            file.write("%s is a working initial angle with %s %d %s ESS turns %s for a goal angle of %s which can collide into a wall with normal vector angle %s to get collision angle %s\n" %(hex(entry[1]), entry[6], entry[0], entry[3], entry[7], hex(entry[2]), hex(entry[4]), hex(entry[5])))
       
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
       
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
   
        for initial_angle in walk_angle_list:
           
            print(hex(initial_angle))
           
            if initial_angle > 65535 or initial_angle < 0 or isinstance(initial_angle, int) == False:
                print('Error: The initial angle is not a valid input')
           
            #for i in range(8192):
            for i in range(Max_ESS_Count):
                for entry in goal_angle_list:
                   
                    angle = entry[0]
                    normal_vector_angle = entry[1]
                    collision_angle = entry[2]
                   
                    if (initial_angle + i*1800)%65536 == angle:
                        solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', ''))
                       
                    if (initial_angle - i*1800)%65536 == angle:
                        solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', ''))
 
                    if (initial_angle + 0x12C + i*1800)%65536 == angle:
                        cup_solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '1 c-up (target) Left and', ''))
                   
                    if (initial_angle + 0x12C - i*1800)%65536 == angle:
                        cup_solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '1 c-up (target) Left and', ''))
 
                    if (initial_angle - 0x12C + i*1800)%65536 == angle:
                        cup_solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '1 c-up (target) Right and', ''))
                   
                    if (initial_angle - 0x12C - i*1800)%65536 == angle:
                        cup_solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '1 c-up (target) Right and', ''))
                       
                    if (initial_angle + 0x3C0 + i*1800)%65536 == angle:
                        cup_solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '1 c-up (no target) Left and', ''))
                   
                    if (initial_angle + 0x3C0 - i*1800)%65536 == angle:
                        cup_solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '1 c-up (no target) Left and', ''))
 
                    if (initial_angle - 0x3C0 + i*1800)%65536 == angle:
                        cup_solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '1 c-up (no target) Right and', ''))
                   
                    if (initial_angle - 0x3C0 - i*1800)%65536 == angle:
                        cup_solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '1 c-up (no target) Right and', ''))
 
                    ##### Here I am hard coding in the walls from bomber's hideout to allow which walls you can sidehop into
                   
                    for right_sidehop_angle in right_sidehop_angles((initial_angle - i*1800)%(0x10000), camera_angle):
                       
                        if 0x0000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x4000:
                       
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                               
                        elif 0x4000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x8000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                       
                        elif 0x8000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0xC000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
       
                        elif 0xC000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x10000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                       
                        ###
                       
                        if 0x0000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x4000:
                       
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                               
                        elif 0x4000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x8000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                       
                        elif 0x8000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0xC000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
       
                        elif 0xC000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x10000:
                   
                            if right_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Right Sidehop'))
                       
                ###### Now Left Sidehops
                   
                    for left_sidehop_angle in left_sidehop_angles((initial_angle - i*1800)%(0x10000), camera_angle):
                       
                        if 0x0000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x4000:
                       
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x4000 or normal_vector_angle == 0x8000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                               
                        elif 0x4000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x8000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                       
                        elif 0x8000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0xC000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
       
                        elif 0xC000 <= (initial_angle - i*1800)%(0x10000) and (initial_angle - i*1800)%(0x10000) < 0x10000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Right', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                   
                        ###
                       
                    for left_sidehop_angle in left_sidehop_angles((initial_angle + i*1800)%(0x10000), camera_angle):
                       
                        if 0x0000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x4000:
                       
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x4000 or normal_vector_angle == 0x8000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                               
                        elif 0x4000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x8000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x8000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
                       
                        elif 0x8000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0xC000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0xC000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
       
                        elif 0xC000 <= (initial_angle + i*1800)%(0x10000) and (initial_angle + i*1800)%(0x10000) < 0x10000:
                   
                            if left_sidehop_angle == angle and (normal_vector_angle == 0x0000 or normal_vector_angle == 0x4000):
                               
                                sidehop_solution_list_walk.append((i, initial_angle, angle, 'Left', normal_vector_angle, collision_angle, '', 'and a Left Sidehop'))
       
        ##### Now sort and then write to file
       
       
        solution_list_walk.sort(key=sortFirst)
        cup_solution_list_walk.sort(key=sortFirst)
        sidehop_solution_list_walk.sort(key=sortFirst)
       
        file.write("------------------------------------------------------------------------------------------\n")
        file.write("------------------------------------------------------------------------------------------------------------------------ SETUPS USING: walk angles (based on camera_angle)\n")
        file.write("----- SETUPS WITHOUT c-up OR sidehops\n")
       
        for entry in solution_list_walk:
           
            # if (entry[1] in walk_list) == True:
           
            #file.write("%d = %s is a working initial angle with %d %s ESS turns for goal angle %d = %s\n" %(entry[1], hex(entry[1]), entry[0], entry[3], entry[2], hex(entry[2])))
            file.write("%s is a working initial angle with %s %d %s ESS turns %s for a goal angle of %s which can collide into a wall with normal vector angle %s to get collision angle %s\n" %(hex(entry[1]), entry[6], entry[0], entry[3], entry[7], hex(entry[2]), hex(entry[4]), hex(entry[5])))
       
        file.write("------------------------------------------------------------------------------------------\n")
        file.write("----- SETUPS WITH c-up\n")
       
        for entry in cup_solution_list_walk:
           
            # if (entry[1] in walk_list) == True:
           
            #file.write("%d = %s is a working initial angle with %d %s ESS turns for goal angle %d = %s\n" %(entry[1], hex(entry[1]), entry[0], entry[3], entry[2], hex(entry[2])))
            file.write("%s is a working initial angle with %s %d %s ESS turns %s for a goal angle of %s which can collide into a wall with normal vector angle %s to get collision angle %s\n" %(hex(entry[1]), entry[6], entry[0], entry[3], entry[7], hex(entry[2]), hex(entry[4]), hex(entry[5])))
       
        file.write("------------------------------------------------------------------------------------------\n")
        file.write("----- SETUPS WITH sidehops\n")
       
        for entry in sidehop_solution_list_walk:
           
            # if (entry[1] in walk_list) == True:
           
            #file.write("%d = %s is a working initial angle with %d %s ESS turns for goal angle %d = %s\n" %(entry[1], hex(entry[1]), entry[0], entry[3], entry[2], hex(entry[2])))
            file.write("%s is a working initial angle with %s %d %s ESS turns %s for a goal angle of %s which can collide into a wall with normal vector angle %s to get collision angle %s\n" %(hex(entry[1]), entry[6], entry[0], entry[3], entry[7], hex(entry[2]), hex(entry[4]), hex(entry[5])))
       
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
        #######################################################################
       
       
       
       
        print("Done.")
 
 
 
def find_walk_angles(camera_angle):
   
    cardinal_list = [(camera_angle - 0xC000)%(0x10000), (camera_angle - 0x8000)%(0x10000), (camera_angle - 0x4000)%(0x10000), camera_angle]
 
    for cardinal_angle in cardinal_list:
        for i in range(5):
            print('Walking angle ' + hex((cardinal_angle + (i+1)*0xBB8)%(0x10000)) + ' is obtained by walking in cardinal direction ' + hex(cardinal_angle) + ' and walking to Link`s Left for %d frames.' %(i+1))
            print('Walking angle ' + hex((cardinal_angle - (i+1)*0xBB8)%(0x10000)) + ' is obtained by walking in cardinal direction ' + hex(cardinal_angle) + ' and walking to Link`s Right for %d frames.' %(i+1))
    return
 
def find_walk_angle(camera_angle, walk_angle):
   
    """
   
   EXAMPLE:
       
       find_walk_angle(0x3ddf, 0x1ab7)
   
   """
   
    cardinal_list = [(camera_angle - 0xC000)%(0x10000), (camera_angle - 0x8000)%(0x10000), (camera_angle - 0x4000)%(0x10000), camera_angle]
   
    for cardinal_angle in cardinal_list:
        for i in range(5):
           
            if (cardinal_angle + (i+1)*0xBB8)%(0x10000) == walk_angle:
                print('Walking angle ' + hex((cardinal_angle + (i+1)*0xBB8)%(0x10000)) + ' is obtained by walking in cardinal direction ' + hex(cardinal_angle) + ' and walking to Link`s Left for %d frames.' %(i+1))
            elif (cardinal_angle - (i+1)*0xBB8)%(0x10000) == walk_angle:
                print('Walking angle ' + hex((cardinal_angle - (i+1)*0xBB8)%(0x10000)) + ' is obtained by walking in cardinal direction ' + hex(cardinal_angle) + ' and walking to Link`s Right for %d frames.' %(i+1))
    return
 
###############################################################################
   
bomber_normal_vector_angle_list = [0x0000, 0x4000, 0x8000, 0xC000]
 
#initial_angle = 0x3880
#camera_angle = 0x388F
#short_chest_angle = 0x2DCD
 
#initial_angle = 0x3DD1
#camera_angle = 0x3DDF
#short_chest_angle = 0x331E
 
 
initial_angle = 0x4258
camera_angle = 0x4250
short_chest = 0x4D14
 
 
 
#initial_angle = 0x38F8
#camera_angle = 0x38FE
#short_chest_angle = 0x2E3D
 
initial_angle_list = [initial_angle, short_chest_angle, 0x0000, 0x4000, 0x8000, 0xC000]
 
name_of_file = "kyle 0x63"
complete_name = name_of_file + ".txt"  
 
 
##### UNCOMMENT THIS IF YOU WANT TO DO A BUNCH OF ITEMS AT ONCE
"""
### Observatory 1 (plus or minus a few items)
 
list_40_bit = ['0x17', '0x07', '0x08', '0x52', '0x0C', '0x33', '0x39', '0x4C', '0x57', '0x2E', '0x4E', '0x25', '0x5A', '0x29', '0x2A', '0x2B', '0x2C']
list_20_bit = ['0x63', '0x73', '0x6C']
 
 
### Observatory 2
 
#list_40_bit = ['0x52', '0x54', '0x2E']
#list_20_bit = ['0x24', '0x07', '0x63', '0x4B']
 
###############################################################################
 
data_file_name = "data.txt"
 
with open(data_file_name, "a") as file:
   file.write("Initial Angle: " + hex(initial_angle) + "\n")
   file.write("Camera Angle: " + hex(camera_angle) + "\n")
   file.write("Short Chest Cutscene Angle: " + hex(short_chest_angle) + "\n")
   file.write("\n")
   
   ### Add walk angles
   
   cardinal_list = [(camera_angle - 0xC000)%(0x10000), (camera_angle - 0x8000)%(0x10000), (camera_angle - 0x4000)%(0x10000), camera_angle]
 
   for cardinal_angle in cardinal_list:
       for i in range(5):
           file.write('Walking angle ' + hex((cardinal_angle + (i+1)*0xBB8)%(0x10000)) + ' is obtained by walking in cardinal direction ' + hex(cardinal_angle) + ' and walking to Link`s Left for %d frames.' %(i+1) + '\n')
           file.write('Walking angle ' + hex((cardinal_angle - (i+1)*0xBB8)%(0x10000)) + ' is obtained by walking in cardinal direction ' + hex(cardinal_angle) + ' and walking to Link`s Right for %d frames.' %(i+1) + '\n')
 
 
 
###############################################################################
 
for item in list_40_bit:
   
   print("Item Value: " + item)
   
   goal_angle_list = find_valid_goal_angles(find_goal_collision_angles_40_bit(item), bomber_normal_vector_angle_list)
   
   complete_name = item + ".txt"  
   
   find_ranked_collision_solutions(initial_angle_list, camera_angle, goal_angle_list, complete_name)
 
for item in list_20_bit:
   
   print("Item Value: " + item)
   
   goal_angle_list = find_valid_goal_angles(find_goal_collision_angles_20_bit(item), bomber_normal_vector_angle_list)
 
   complete_name = item + ".txt"  
   
   find_ranked_collision_solutions(initial_angle_list, camera_angle, goal_angle_list, complete_name)
"""
 
 
 
##### USE THIS IF YOU WANT TO DO ONE ITEM AT A TIME
 
#goal_angle_list = find_valid_goal_angles(find_goal_collision_angles_40_bit('0x17'), bomber_normal_vector_angle_list)
goal_angle_list = find_valid_goal_angles(find_goal_collision_angles_20_bit('0x63'), bomber_normal_vector_angle_list)
 
 
find_ranked_collision_solutions(initial_angle_list, camera_angle, goal_angle_list, complete_name)
