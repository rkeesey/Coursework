from sys import argv
# project0.py

# Starter code for project 0 in ICS 32 Programming with Software Libraries in Python

# Replace the following placeholders with your information.

# RUBY KEESEY
# RKEESEY@UCI.EDU
# 76645012

def square(height):
    caps = '+-+\n'
    connects = '+-+-+\n'
    cols ='| |\n'
    wtspc = ''

    output = ''
    if height > 0:
        output += caps
        output += cols
        if height > 1:
            for i in range (1, height):
                output += wtspc
                output += connects
                wtspc += '  '
                output += wtspc
                output += cols
        output += wtspc
        output += caps
    return output

def main():
    inpt = int(argv[1])
    output = square(inpt)
    print(output)

if __name__ == "__main__":
    main()