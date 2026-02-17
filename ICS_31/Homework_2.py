# Keesey, Ruby, rkeesey

# Problem 1
def sum5(inpt):
    sum = 0
    count = 5
    while count <= inpt:
        sum += count
        count += 5
    print(sum)

# Problem 2
def cap(inpt_strng):
    caps = ['A', 'E', 'I', 'O', 'U', 'Y']
    undrcs = ['a', 'e', 'i', 'o', 'u', 'y']
    mod_strng = []
    for let in inpt_strng:
        if let in undrcs:
            idx_2 = undrcs.index(let)
            mod_strng.append(caps[idx_2])
        else:
            mod_strng.append(let)
    print(''.join(mod_strng))    

# Problem 3
def MeanRemove(num_lst):
    lst_sum = sum(num_lst)
    lst_len = len(num_lst)
    lst_avg = lst_sum/lst_len

    mod_lst = []
    for i in range(lst_len):
        mod_num = num_lst[i] - lst_avg
        mod_lst.append(int(mod_num))

    print(mod_lst)

# Problem 5
def LongestEdge(ver1, ver2, ver3):
    x1, y1, z1 = ver1
    x2, y2, z2 = ver2
    x3, y3, z3 = ver3

    edge_1 = ((x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2) ** 0.5
    edge_2 = ((x1 - x3)**2 + (y1 - y3)**2 + (z1 - z3)**2) ** 0.5
    edge_3 = ((x2 - x3)**2 + (y2 - y3)**2 + (z2 - z3)**2) ** 0.5

    print(max(edge_1, edge_2, edge_3))

# Problem 6
def CheeseHunt(coord_1, coord_2):

    found = 0
    start_x = 2
    start_y = 2
    
    while True:
        start_dist_x = abs(coord_1 - start_x)
        start_dist_y = abs(coord_2 - start_y)
        new_x = start_x
        new_y = start_y
        print(f"({start_x}, {start_y})", end=' ')
        usr_inpt = input("Please move: ")
        if usr_inpt == 'left':
            new_x = start_x - 1
            new_dist_y = start_dist_y
        if usr_inpt == 'right':
            new_x = start_x + 1
            new_dist_y = start_dist_y
        new_dist_x = abs(coord_1 - new_x)
        if usr_inpt == 'up':
            new_y = start_y - 1
            new_dist_x = start_dist_x
        if usr_inpt == 'down':
            new_y = start_y + 1
            new_dist_x = start_dist_x
        
        new_dist_x = abs(coord_1 - new_x)
        new_dist_y = abs(coord_2 - new_y)

        if new_dist_x == 0 and new_dist_y == 0:
            print(f"Congratulations! You found the cheese at ({coord_1},{coord_2}).")
            break
        elif new_dist_x > start_dist_x or new_dist_y > start_dist_y:
            print("Farther from cheese")
        elif new_dist_x < start_dist_x or new_dist_y < start_dist_y:
            print("Closer to cheese")
        
        start_x = new_x
        start_y =new_y
        


if __name__=='__main__':
    sum5(19)
    sum5(21)

    cap('ashley')
    cap('coronavirus')

    MeanRemove([1, 2, 3])

    LongestEdge((4, 5.5, 8), (9, 14, 0), (3, 1.5, 17))
    
    CheeseHunt(1, 2)


