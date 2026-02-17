# project1.py
#
# ICS 32 Fall 2025
# Project #1: File System Explorer
# 
# NAME: Ruby Keesey
# EMAIL: rkeesey@uci.edu
# STUDENT ID: 76645012
#
# High-level Design:
# 

from pathlib import Path

# These string constants are provided to avoid typo errors for the man command.
# Each constant holds one line of text. 
# These can be concatenated to create the correct man directions.
# Note: uncomment and move the constants into your function for creating the directions.

# GENERIC1 = "The File System Explorer supports this command in the following format/s:\n"
# GENERIC2 = "[COMMAND]\n"
# GENERIC3 = "[COMMAND] [INPUT]\n"
# GENERIC4 = "[COMMAND] [-OPTIONS] [INPUT]\n"
# GENERIC5 = "[COMMAND] [-OPTIONS] [INPUT] [OPTION_INPUT]\n"
# GENERIC6 = "The [INPUT] corresponds to the [COMMAND].\n"
# GENERIC7 = "The [OPTIONAL_INPUT] corresponds to [-OPTIONS].\n"
# LS_DIR = "ls is a command that lists the contents of a directory. [INPUT] is the path.\n"
# LS_DIR2 = "ls options include -r, -f, -s, -e, -g and -l.\n"
# LS_DIR3 = "-r = recursive, -f file only, -s match specific file name, -e match specific extension.\n"
# LS_DIR4 = "-g and -l prints only files with size greater (g) or less (l) than [OPTION_INPUT].\n"
# CAT_DIR = "cat is a command that prints the contents of a file. [INPUT] is the file path.\n"
# CAT_DIR2 = "cat options include -f and -d.\n"
# CAT_DIR3 = "-f = prints the first line only, -d duplicates the file into filename.dup.\n"
# MAN_DIR = "man is a command that prints the directions for the command. [INPUT] is the command.\n"
# Q_DIR = "q is a command that quits the file system explorer.\n"

MAN = '''The File System Explorer supports this command in the following format/s:
[COMMAND] [INPUT]
man is a command that prints the directions for the command. [INPUT] is the command.\n'''
Q = '''The File System Explorer supports this command in the following format/s:
[COMMAND]
q is a command that quits the file system explorer.\n'''
CAT = '''The File System Explorer supports this command in the following format/s:
[COMMAND] [INPUT]
[COMMAND] [-OPTIONS] [INPUT]
The [INPUT] corresponds to the [COMMAND].
cat is a command that prints the contents of a file. [INPUT] is the file path.
cat options include -f and -d.
-f = prints the first line only, -d duplicates the file into filename.dup.\n'''
LS = '''The File System Explorer supports this command in the following format/s:
[COMMAND] [INPUT]
[COMMAND] [-OPTIONS] [INPUT]
[COMMAND] [-OPTIONS] [INPUT] [OPTION_INPUT]
The [INPUT] corresponds to the [COMMAND].
The [OPTIONAL_INPUT] corresponds to [-OPTIONS].
ls is a command that lists the contents of a directory. [INPUT] is the path.
ls options include -r, -f, -s, -e, -g and -l.
-r = recursive, -f file only, -s match specific file name, -e match specific extension.
-g and -l prints only files with size greater (g) or less (l) than [OPTION_INPUT].\n'''

def man(input):

    txt =''
    if input == 'man':
        txt = MAN
    elif input == 'q':
        txt = Q
    elif input == 'cat':
        txt = CAT
    elif input == 'ls':
        txt = LS
    else:
        txt = 'ERROR: Invalid Command.\n'
    return txt

def ls_r(i): # recursive function to get subdirectory contents
    files = []
    for j in i.iterdir():
        if j.is_file() or j.is_symlink():
            files.append(str(j))
        elif j.is_dir():
            files.extend(ls_r(j)) # calls ls_r function again
        else: 
            files.append(str(j))
    return files

def dir_manager(ls_file, rec_spec, options, opt_inpt):
    for elem in ls_file:
        file = Path(elem).name
        specific = ls_s_e(file, options, opt_inpt)
        if specific == True:
            rec_spec += f'{elem}\n'
    return rec_spec

def ls_s_e(ls_elem, option, word):
    p = Path(ls_elem)
    if option == '-s' or option == '-frs':
        match = p.stem
        return word in match
        
    elif option == '-e' or option == '-fre':
        match = p.suffix.lstrip('.')
        return word == match

        

def ls(input, options='', opt_inpt=0):
    p = Path(input)
    if not p.exists():
        return f"ERROR: Invalid Path. \n"

    ls_file = []
    ls_dir = []
    ls_sub = []

    for i in p.iterdir():
        if i.is_file() or i.is_symlink():
            ls_file.append(str(i))
        elif i.is_dir():
            ls_dir.append(str(i))
            if options == '-r' or options == '-fr' or options == '-frs' or options == '-fre':
                recurs = ls_r(i)
                for j in recurs:
                    ls_sub.append(str(j))
        else: 
            ls_file.append(str(i))
    
    ls_file.sort()
    ls_sub.sort()

    f_only = ''
    rec_spec = ''
    if options == '-f' or options == '-fr':
        for file in ls_file:
            f_only += f'{file}\n'
        if options == '-fr':
            for sub in ls_sub:
                f_only += f'{sub}\n'
        return f_only
    
    elif options == '-frs':
        lst1 = dir_manager(ls_file, rec_spec, options, opt_inpt)
        lst2 = dir_manager(ls_sub, lst1, options, opt_inpt)
        return lst2
            
    
    elif options == '-fre':
        lst1 = dir_manager(ls_file, rec_spec, options, opt_inpt)
        lst2 = dir_manager(ls_sub, lst1, options, opt_inpt)
        return lst2
    
    elif options == '-s':
        lst1 = dir_manager(ls_file, rec_spec, options, opt_inpt)
        return lst1
    
    elif options == '-e':
        lst1 = dir_manager(ls_file, rec_spec, options, opt_inpt)
        return lst1

    ls_dir.sort()
    ls_ordered = ''
    for file in ls_file:
        ls_ordered += f'{file}\n'
        

    for dir in ls_dir:
        ls_ordered += f'{dir}\n'

    rec = ''
    if options == '-r':
        for file in ls_file:
            rec += f'{file}\n'
        for dir in ls_dir:
            rec += f'{dir}\n'
        for sub in ls_sub:
            rec += f'{sub}\n'
        return rec

    return ls_ordered

def cat(inpt, options=''):
    p = Path(inpt)
    if not p.exists():
        return f"ERROR: Invalid Path. \n"

    with open(inpt, 'r') as f:
        file_r = f.readlines()
    if options == '-f':
        return f'{file_r[0]}\n'
    elif options == '-d':
        file_w = f'{inpt}.dup'
        with open(file_w, 'w') as f:
            for line in file_r:
                f.write(str(line))
    else:
        full = ''
        for line in file_r:
            full += f'{line}'
        full += '\n'
        return full

def parse_command(user_input):

    separated = user_input.split()
    command = separated[0]

    value = ''
    if command == 'man':
        input = separated[1]
        if len(separated) != 2:
            return "ERROR: Invalid Format.\n" 
        value = man(input)
    elif command == 'ls': 
        if len(separated) == 4:
            options = separated[1]
            input = separated[2]
            opt_inpt = separated[3]
            value = ls(input, options, opt_inpt)
        elif len(separated) == 3:
            options = separated[1]
            input = separated[2]
            value = ls(input, options)
            if value == '':
                return "ERROR: Invalid Format.\n"
        
        elif len(separated) == 2:
            input = separated[1]
            value = ls(input)
        else:
            return "ERROR: Invalid Format.\n"
    elif command == 'cat':
        if len(separated) > 2:
            input = separated[2]
            options = separated[1]
            value = cat(input, options)
        elif len(separated) == 2:
            input = separated[1]
            value = cat(input)
        else:
            return "ERROR: Invalid Format.\n"
    elif command == 'q':
        if len(separated) != 1:
            return "ERROR: Invalid Format.\n"
        return 'quit'
    else: 
        return "ERROR: Invalid Command.\n"
    return value

def main() -> None:
    while True:
        user_input = input()
        value = parse_command(user_input)
        if (value == "quit"):
            exit()
        else:
            print(value, end="")

if __name__ == '__main__':
    main()