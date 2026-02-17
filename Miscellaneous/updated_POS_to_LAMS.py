import re
import itertools

# this code applies to C, H, Ru systems and assumes that those elements are ordered as such (C H Ru)

def calc_dist(coord, comp, coord_list, coords_hi):
    
    dist = []
    x1 = coord_list[coord][0]
    y1 = coord_list[coord][1]
    z1 = coord_list[coord][2]
    
    x2 = coord_list[comp][0]
    y2 = coord_list[comp][1]
    z2 = coord_list[comp][2]

    x_dist = abs(x1 - x2)
    y_dist = abs(y1 - y2)
    z_dist = abs(z1 - z2)
    
    x_evald, y_evald, z_evald = eval_prdc_bnds(coords_hi, x_dist, y_dist, z_dist)

    sqrt_arg = x_evald**2 + y_evald**2 + z_evald**2
    dist = sqrt_arg**0.5

    return dist

def eval_prdc_bnds(coords_hi, x, y, z):

    max_x_dist = float(coords_hi[0])/2
    if x >= max_x_dist:
        x_dist = float(coords_hi[0]) - x
    else:
        x_dist = x

    max_y_dist = float(coords_hi[1])/2
    if y >= max_y_dist:
        y_dist = float(coords_hi[1]) - y
    else:
        y_dist = y

    max_z_dist = float(coords_hi[2])/2
    if z >= max_z_dist:
        z_dist = float(coords_hi[2]) - z
    else:
        z_dist = z

    return x_dist, y_dist, z_dist 

def find_bonds(POSCAR_file, coords_hi, counts):

    C_H_len = 1.74
    C_C_len = 2.04
    Ru_H_len = 2.00 # to check that H is not bonded to adsorbed C
    data = []

    with open(POSCAR_file, 'r') as f:
        lines = f.readlines()[7:]
        lines = str(lines)
        data = re.findall(r"[-+]?\d*\.\d+|\d+", lines)

    coord_list_old = []
    i = 0

    while i in range(len(data) - 2):
        x = float(data[i])
        y = float(data[i+1])
        z = float(data[i+2])
        coords = [x, y, z] 
        coord_list_old.append(coords)
        i+=3

    bond_count = 0
    bond_types = []
    bond_idxs = []

    c_c_dists = []
    c_h_dists = []
    h_ru_dists = [] # excluded from LAMMPS file dataset 

    # H-Ru distances (NOT INCLUDED IN COORDS OR BOND COUNT)
    filtered_coord_list = []
    H_count = int(counts[1])
    C_count = int(counts[0])
    H_removed = 0
    
    for coord in range(len(coord_list_old)):
        keep_coord = True # keep H atom if not bonded to Ru
        if coord in range(C_count, C_count + H_count):
            near_ru = False 
            for comp in range(C_count + H_count, len(coord_list_old)):
                dist = calc_dist(coord, comp, coord_list_old, coords_hi)
                h_ru_dists.append(dist)
                if dist <= Ru_H_len:
                    near_ru = True # H is close or bonded to Ru
                    break
            if near_ru:
                keep_coord = False
                for comp in range(C_count):
                    dist = calc_dist(coord, comp, coord_list_old, coords_hi)
                    c_h_dists.append(dist)
                    if dist <= C_H_len:
                        keep_coord = True # H is bonded to a C
            if not keep_coord:
                H_removed += 1
        if keep_coord:
            filtered_coord_list.append(coord_list_old[coord])
    
    H_count = H_count - H_removed
    coord_list = filtered_coord_list
    print(f"{H_removed} adsorbed H atoms removed")

    C_bond_counts = [0] * C_count
    C_atom_types = [] * C_count
    for coord in range(len(coord_list) - 1):

        # C_C_total distances
        get_bonds(bond_idxs, coord_list, coord, 0, C_count - 1, coord + 1, C_count, 
                 c_c_dists, C_C_len)

        # C_H_total distances
        get_bonds(bond_idxs, coord_list, coord, 0, C_count, C_count, C_count + H_count,
                 c_h_dists, C_H_len)

        if coord in range(C_count):
            for comp in range(C_count, C_count + H_count):
                dist = calc_dist(coord, comp, coord_list, coords_hi)
                c_h_dists.append(dist)
                if dist <= C_H_len: 
                    C_bond_counts[coord] += 1                    
    
    atom_type_list = [1, 2, 3, 4, 5]
    atom_counts = [0] * len(atom_type_list)
    # H bonds per C
    for i in range(C_count):
        # adsorbed carbon
        if C_bond_counts[i] <= 1:
            atom_type = 3
            atom_idx = atom_type - 1
            atom_counts[atom_idx] += 1
        # carbon with 2H
        if C_bond_counts[i] == 2:
            atom_type = 2
            atom_idx = atom_type - 1
            atom_counts[atom_idx] += 1
        # carbon with 3H
        if C_bond_counts[i] == 3:
            atom_type = 1
            atom_idx = atom_type - 1
            atom_counts[atom_idx] += 1

        C_idx = i + 1
        C_info = [C_idx, atom_type]
        C_atom_types.append(C_info)

    atom_types = []
    for atom in range(len(coord_list)):
        if atom in range(C_count):
            C_atom_type = C_atom_types[atom][1]
            atom_types.append(C_atom_type)
        if atom in range(C_count, C_count + H_count):
            atom_type = 4
            atom_idx = atom_type - 1
            atom_counts[atom_idx] += 1
            atom_types.append(atom_type)
        if atom in range(C_count + H_count, len(coord_list)):
            atom_type = 5
            atom_idx = atom_type - 1
            atom_counts[atom_idx] += 1
            atom_types.append(atom_type)
    
    bond_type_rules = {
        (1, 2): 1,
        (1, 3): 3,
        (1, 4): 5,
        (2, 2): 2,
        (2, 3): 4,
        (2, 4): 6,
        }

    bond_idx_info = []
    for bond in bond_idxs:
        atom_1_idx = bond[0] - 1
        atom_2_idx = bond[1] - 1
        atom_type_1 = atom_types[atom_1_idx]
        atom_type_2 = atom_types[atom_2_idx]

        sorted_types = tuple(sorted((atom_type_1, atom_type_2)))
        
        if sorted_types in bond_type_rules:
            bond_type = bond_type_rules[sorted_types]
            bond_info = [bond_type, atom_1_idx + 1, atom_2_idx + 1]  
            bond_idx_info.append(bond_info)

    bond_types = [1, 2, 3, 4, 5, 6]
    bond_count = [0] * len(bond_types)
    for bond in range(len(bond_idx_info)):
        bond_type = bond_idx_info[bond][0]
        bond_idx = bond_type - 1
        if bond_type in bond_types:
            bond_count[bond_idx] += 1

    return bond_count, bond_types, bond_idx_info, coord_list, atom_types, atom_counts

def get_bonds(bond_idxs, coord_list, coord, coord_start, coord_end, comp_start, comp_end, 
                 bond_dist_list, bond_len):
    if coord in range(coord_start, coord_end):
        for comp in range(comp_start, comp_end):
            dist = calc_dist(coord, comp, coord_list, coords_hi)
            bond_dist_list.append(dist)
            if dist <= bond_len:
                coord_idx_1 = coord + 1
                coord_idx_2 = comp + 1  
                bond_info = [coord_idx_1, coord_idx_2]
                bond_idxs.append(bond_info)

def write_LAMMPS(LAMMPS_name, atom_counts, bond_count, coord_atoms, 
                 coords_hi, bond_types, bond_idxs, coord_list,
                 angles, angle_types, angle_list, 
                 dihedrals, dihedral_types, dihedral_type_rules):

    file_name = LAMMPS_name
    atom_sum = len(coord_atoms)
    bond_sum = 0
    for bond in range(len(bond_count)):
        bond_sum += bond_count[bond]
    
    atom_symbols = ['CT3', 'CT2', 'Cmet', 'HA', 'Ru']

    with open (file_name, 'w') as f:
        
        f.write("# LAMMPS data file written from POSCAR data file\n\n")

        f.write(f"{atom_sum} atoms\n")
        f.write(f"{bond_sum} bonds\n")
        f.write(f"{len(angles)} angles\n")
        f.write(f"{len(dihedrals)} dihedrals\n")
        
        f.write(f"\n{len(atom_symbols)} atom types\n")
        f.write(f"{len(bond_types)} bond types\n")
        f.write(f"{len(angle_list)} angle types\n")
        f.write(f"{len(dihedral_type_rules)} dihedral types\n\n")

        f.write(f"0.0 {coords_hi[0]} xlo xhi\n")
        f.write(f"0.0 {coords_hi[1]} ylo yhi\n")
        f.write(f"0.0 {coords_hi[2]} zlo zhi\n\n")

        f.write("Masses\n\n")

        f.write("1 12.0107  # CT3\n2 12.0107  # CT2\n3 12.0107  # Cmet\n4 3.00794  # HA\n5 101.07  # Ru\n\n") #needs to be edited if elements are not C, H, and Ru

        f.write("Atoms  # molecular\n\n")
        for i in range(len(coord_atoms)):
            
            x = coord_list[i][0]
            y = coord_list[i][1]
            z = coord_list[i][2]
            
            atom_ID = i + 1
            molec_ID = 1

            atom_type = atom_types[i]

            f.write(f"{atom_ID} {molec_ID} {atom_type} {x} {y} {z}\n")

        f.write(f"\nBonds\n\n")

        for i in range(len(bond_idxs)):
                
            bond_type = bond_idxs[i][0]
            bond_num = i + 1
            atom_1 = bond_idxs[i][1]
            atom_2 = bond_idxs[i][2]

            f.write(f"{bond_num} {bond_type} {atom_1} {atom_2}\n")
        f.write("\n")

        f.write(f"Angles\n\n")
        for i in range(len(angles)):
            
            angle_num = i + 1
            angle_type = angle_types[i]
            i = angles[i][0]
            j = angles[i][1]
            k = angles[i][2]

            f.write(f"{angle_num} {angle_type} {i} {j} {k}\n")
        f.write("\n")    

        f.write(f"Dihedrals\n\n")
        for i in range(len(dihedrals)):
            
            dihedral_num = i + 1
            dihedral_type = dihedral_types[i]
            i = dihedrals[i][0]
            j = dihedrals[i][1]
            k = dihedrals[i][2]
            l = dihedrals[i][3]

            f.write(f"{dihedral_num} {dihedral_type} {i} {j} {k} {l}\n")

def get_angles(bond_idxs, atom_types, atom_counts):
    
    bond_dict = {}
    for bond in bond_idxs:
        b_type, a1, a2 = bond
        if a1 not in bond_dict:
            bond_dict[a1] = []
        if a2 not in bond_dict:
            bond_dict[a2] = []
        bond_dict[a1].append(a2)
        bond_dict[a2].append(a1)  # Include both directions for full connectivity

    angle_type_rules = {
        (1, 2, 2): 1, (2, 2, 2): 2, (1, 2, 3): 3,
        (1, 3, 2): 4, (3, 2, 2): 5, (2, 3, 2): 6,
        (4, 2, 1): 7, (4, 1, 2): 8, (4, 2, 2): 9,
        (4, 2, 3): 10, (4, 1, 3): 11, (4, 1, 4): 12,
        (4, 2, 4): 13,
    }

    seen_angles = set()
    angles = []
    angle_types = []
    atom_groupings = []

    for j in bond_dict:
        neighbors = bond_dict[j]
        for idx1 in range(len(neighbors)):
            for idx2 in range(idx1 + 1, len(neighbors)):
                i = neighbors[idx1]
                k = neighbors[idx2]

                i_type = atom_types[i - 1]
                j_type = atom_types[j - 1]
                k_type = atom_types[k - 1]

                # Check both (i, j, k) and (k, j, i)
                angle_tuple = (i, j, k)
                reverse_angle_tuple = (k, j, i)
                angle_types_key = (i_type, j_type, k_type)
                reverse_types_key = (k_type, j_type, i_type)

                if angle_tuple in seen_angles or reverse_angle_tuple in seen_angles:
                    continue

                if angle_types_key in angle_type_rules:
                    angle_type = angle_type_rules[angle_types_key]
                elif reverse_types_key in angle_type_rules:
                    angle_type = angle_type_rules[reverse_types_key]
                    angle_tuple = reverse_angle_tuple  # Store canonical form
                else:
                    continue

                seen_angles.add(angle_tuple)
                seen_angles.add(reverse_angle_tuple)

                angles.append(angle_tuple)
                angle_types.append(angle_type)
                atom_groupings.append([atom_types[angle_tuple[0] - 1],
                                       atom_types[angle_tuple[1] - 1],
                                       atom_types[angle_tuple[2] - 1]])

    return angles, angle_types, angle_type_rules

def get_dihedrals(bond_list, atom_types):
    bond_dict = {}
    for _, a1, a2 in bond_list:
        bond_dict.setdefault(a1, []).append(a2)
        bond_dict.setdefault(a2, []).append(a1)
   
    dihedral_type_rules = {
        (2, 2, 2, 2):1, (1, 2, 2, 2):2, (1, 2, 2, 1):3, (1, 2, 2, 3):4,
        (1, 2, 3, 2):5, (1, 3, 2, 2):6, (3, 2, 2, 2):7, (2, 3, 2, 2):8,
        (4, 1, 2, 2):9, (4, 2, 2, 1):10, (4, 2, 2, 2):11, (4, 2, 2, 3):12,
        (4, 2, 3, 2):13, (4, 1, 2, 3):14, (4, 1, 3, 4):15, (4, 1, 2, 4):16,
        (4, 2, 2, 4):17
    }
    
    dihedrals = []
    dihedral_types = []
    seen = set()

    for j in bond_dict:
        for k in bond_dict[j]:
            if j < k:  # avoid double counting
                neighbors_j = [i for i in bond_dict[j] if i != k]
                neighbors_k = [l for l in bond_dict[k] if l != j]
                for i in neighbors_j:
                    for l in neighbors_k:
                        dihedral = (i, j, k, l)
                        reverse_dihedral = (l, k, j, i)
                        if dihedral in seen or reverse_dihedral in seen:
                            continue
                        seen.add(dihedral)
                        seen.add(reverse_dihedral)

                        types = (atom_types[i - 1], atom_types[j - 1],
                                 atom_types[k - 1], atom_types[l - 1])
                        if types in dihedral_type_rules:
                            dtype = dihedral_type_rules[types]
                            dihedrals.append(dihedral)
                            dihedral_types.append(dtype)

    return dihedrals, dihedral_types, dihedral_type_rules

def extract_header(POSCAR_file):

    with open(POSCAR_file, 'r') as f:
        lines = f.readlines()[2:7]
        lines = str(lines)
        data = re.findall(r"[-+]?\d*\.\d+|\d+", lines)
        xhi = data[0]
        yhi = data[4]
        zhi = data[8]
        coords_hi = [xhi, yhi, zhi]
        element_counts = data[9:]

    return coords_hi, element_counts

if __name__=="__main__":
    
    POSCAR_file = input("Enter a POSCAR name: ")

    # Extract number following "POSCAR", if any
    match = re.match(r"POSCAR(\d*)$", POSCAR_file.strip())

    if match:
        number = match.group(1)  # This will be '' if there's no number
        if number:
            LAMMPS_file = f"LAMMPS_traj_{number}.txt"
        else:
            LAMMPS_file = "LAMMPS_traj.txt"
    else:
        raise ValueError("Input file name must start with 'POSCAR'")

    print("LAMMPS output file name:", LAMMPS_file)

    coords_hi, element_counts = extract_header(POSCAR_file)

    bond_count, bond_types, bond_idxs, coord_list, atom_types, atom_counts = find_bonds(POSCAR_file, coords_hi, element_counts)

    angle, angle_types, angle_list = get_angles(bond_idxs, atom_types, atom_counts)

    dihedrals, dihedral_types, dihedral_type_rules = get_dihedrals(bond_idxs, atom_types)
    
    write_LAMMPS(LAMMPS_file, atom_counts, bond_count, atom_types, 
                 coords_hi, bond_types, bond_idxs, coord_list, 
                 angle, angle_types, angle_list, 
                 dihedrals, dihedral_types, dihedral_type_rules)
    
    print(f"{POSCAR_file} converted to {LAMMPS_file}")