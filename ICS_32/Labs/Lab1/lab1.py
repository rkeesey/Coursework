from pathlib import Path
# lab1.py
# Starter code for lab 1 in ICS 32 Programming with Software Libraries in Python
# Replace the following placeholders with your information.
# Ruby Keesey
# rkeesey@uci.edu
# 76645012

# String Constants
TXT1 = "Welcome to PyNote!\n\n"
TXT2 = "Below are the notes stored in this file: "
TXT3 = "Please enter a new note (enter q to exit): "

def write_notes(file_path):
    while True:
        prompt = input(TXT3)
        if prompt != 'q':
            with open(file_path, 'a') as f:
                f.write(f'{prompt}\n\n')
        else:
            return False

def start_notes():

    file_name = "pynote.txt"
    written_to = Path.cwd()/file_name
    statements = ''
    if Path.exists(written_to) == True:
        with open(written_to, 'r') as f:
            existing = f.read()    

        statements = f'{TXT1}{TXT2}{written_to}\n\n{existing}'
        return statements, written_to
    else:
        return statements, written_to
def main():

    statements, file_path = start_notes()
    print(statements)

    write_notes(file_path)
    pass
if __name__ == "__main__":
    main()
