#!/usr/bin/env python

from collections import namedtuple
from sys import argv
import math
import os

elem_data = namedtuple('elem_data', ['type', 'count'])

def XDAT_data(file_name, start, end, nth):
    
    with open(file_name, 'r') as f:
        data = f.readlines()
    lattice_params = []
    elems = []
    clean_data = []
    for i, line in enumerate(data):
        line_data = line.strip()
        line_data = line.split()
        if i in range(2, 5):
            lattice_params.append(line_data)
        elif i in range(5, 7):
            elems.append(line_data)
        else:
            clean_data.append(line_data)

    elem_list= []
    elem_tot = 0
    for i in range(len(elems[0])):
        elem = elem_data(elems[0][i], int(elems[1][i]))
        elem_list.append(elem)
        elem_tot += int(elems[1][i])

    xdat_coords = []
    for i, line in enumerate(clean_data):
        frame_coords = []
        if line[0] == 'Direct':
            frame = int(line[2])
            line_num = i
            if frame in range(start, end, nth):
                for coord in range(line_num + 1, line_num + elem_tot + 1):
                    frame_coords.append(clean_data[coord])
                xdat_coords.append(frame_coords) 
    
    return xdat_coords, elem_tot, elem_list, lattice_params

def rmv_xs_h(xdat_coords, elem_tot, elem_list, lattice_params):

    lat_x = float(lattice_params[0][0]) 
    lat_y = float(lattice_params[1][1]) 
    lat_z = float(lattice_params[2][2]) 
    
    max_x = lat_x * 0.5
    max_y = lat_y * 0.5
    max_z = lat_z * 0.5

    H_count = 0
    H_frame_idx = 0
    for elem in elem_list:
        if elem.type == 'H':
            H_count = elem.count
            break
        H_frame_idx += elem.count
    
    H_frame_idx = H_frame_idx - 1 # for 0 indexing

    C_count = 0
    for elem in elem_list:
        if elem.type == 'C':
            C_count = elem.count
            break
    
    H_C_bond = 1.50 # Angstroms
    for n, frame in enumerate(xdat_coords):
        frame_H = []
        frame_count = 0
        for i, coord in enumerate(frame):
            H_dists = []
            x_1 = float(coord[0]) * lat_x
            y_1 = float(coord[1]) * lat_y
            z_1 = float(coord[2]) * lat_z
            for j, comp in enumerate(frame):
                if i >= H_frame_idx and i <= H_frame_idx + H_count:
                    if j < C_count: # assuming C is the first element

                        x_2 = float(comp[0]) * lat_x
                        y_2 = float(comp[1]) * lat_y
                        z_2 = float(comp[2]) * lat_z

                        dist = calc_dist(max_x, max_y, max_z, x_1, y_1, z_1, x_2, y_2, z_2)
                        H_dists.append(dist)
            if len(H_dists) != 0 and all(val > H_C_bond for val in H_dists):
                print('H removed from frame ', n)
                print(y_1)
        
                        


    new_coords = 0
    return new_coords

def calc_dist(max_x, max_y, max_z, x_1, y_1, z_1, x_2, y_2, z_2):

    x_dist = abs(float(x_1) - float(x_2))
    x_real = eval_dist(max_x, x_dist)

    y_dist = abs(float(y_1) - float(y_2))
    y_real = eval_dist(max_y, y_dist)

    z_dist = abs(float(z_1) - float(z_2))
    z_real = eval_dist(max_z, z_dist)
    
    dist = (x_real **2 + y_real ** 2 + z_real ** 2) ** 0.5
    
    return dist
    

def eval_dist(max_dist, calc_dist):
    if calc_dist > max_dist:
        real_dist = calc_dist - max_dist
    else:
        real_dist = calc_dist

    return real_dist
    

if __name__=='__main__':
    
    #file_name = argv[1]
    #start = int(argv[2])
    #end = int(argv[3])
    #nth = int(argv[4])
    start = 1
    end = 10
    nth = 2
    file_name = "XDATCAR_sample.txt"

    xdat_coords, elem_tot, elem_list, lattice_params = XDAT_data(file_name, start, end, nth)
    new_coords = rmv_xs_h(xdat_coords, elem_tot, elem_list, lattice_params)