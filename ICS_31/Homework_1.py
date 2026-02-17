# Keesey, Ruby, 76645012
import random

# Problem 1
a = 3
b = 5
summed = a + b
squared = summed**2
print(squared) # output: 64

# Problem 2
q = 17 // 4
print("q: ", q) # output: 4
r = 17 % 4
print("r: ", r) # output: 1

# Problem 3
# x^2 + 2xy + y^2x^2 + 2xy + y^2
x = 2 # dummy integer
y = 8 # dummy integer

eq_py_exp = x**2 + 2*x*y + y**2*x**2 + 2*x*y + y**2
print("equivalent python expression: ", eq_py_exp) # output: 388 when x = 2 and x = 8

# Problem 4
expression = 3 + 2.5 * 4
print(type(expression)) #output: <class 'float'>

# Problem 5
x = -3
y = 2
result = x**2 + 3*x + 2*y**2
print(result) # output: 8

# Problem 6
base = float(input("Enter the base: "))
height = float(input("Enter the height "))
area = 0.5 * base * height # area of a triangle
print("The area is ", area)

# Problem 7
temp_F = float(input("Enter the temperature in fahrenheit: "))
temp_C = (temp_F - 32) * 5/9 
print("The temperature in celsius is", temp_C)

# Problem 8
names_input = input("Enter the name list: ")
list = names_input.split()
for i in range(len(list)):
    name = list[i].strip(',')
    print("Hello", name)

# Problem 9
first = input("Enter the first name: ")
last = input("Enter the last name: ")
print(f"{first}    {first}    {first}    {first}    {last} {last}")

# Problem 10
list_1 = input("Enter the first sequence: ")
list_1 = list_1.split(',')
list_2 = input("Enter the second sequence: ")
list_2 = list_2.split(',')

common_nums = []
for i in range(len(list_1)):
    for j in range(len(list_2)):
        num_1 = int(list_1[i])
        num_2 = int(list_2[j])
        if num_1 == num_2:
            common_nums.append(num_1)
print("Common numbers:", common_nums)

# Problem 11
usr_inpt = int(input("Enter a number: "))
abs_sqrt = (abs(usr_inpt))**0.5
print("Result: ", abs_sqrt)

# Problem 12
secret = random.randint(1, 100)
print(f"Secret number is {secret}")
loop_num = 0
while loop_num != 1:
    usr_inpt = int(input("Enter a number: "))
    if usr_inpt > secret:
        print(f"The number is smaller than {usr_inpt}")
    if usr_inpt < secret:
        print(f"The number is larger than {usr_inpt}")
    if usr_inpt == secret:
        print(f"Congratulations! The number is {secret}")
        loop_num = 1

# Problem 13
# a.
prime_sum = 2 + 3 + 5 + 7 + 11 # output: 28
# b.
sqr_cube_sum = 13**2 * 18**3 # output: 985608
# c.
radius = 9.5
sph_vol = 4/3 * 3.14 * radius**3 # output: 3589.543333333333

# Problem 14
nums = '3 4 9 1 0 1 1 6 8 1 6 1 7 3 5 1 4 9 1 9'
# a.
third_num = nums[4] # output: 9
# b.
svnth_num = nums[32] # output: 4
# c.
sum_nums =  int(nums[18]) + int(nums[-1]) # output: 10
# d.
diff_nums = int(nums[12]) - int(nums[22]) # output: 0

# Problem 15
s = 'Python Programming'
# a. 
if s[4] == 'o':
    char_a = True
else:
    char_a = False
# output: True
# b.
if len(s) == 18:
    char_b = True
else:
    char_b = True
# output: True
# c.
count = 0
for i in s:
    if i == 'm':
        count += 1

if count == 3:
    char_c = True
else:
    char_c = False
# output: False
# d.
if s[-1] == 'g':
    char_d = True
else:
    char_d = False
#output: True

# Problem 16
# a.
flt_num = 3.0
int_num = 2
prod = flt_num * int_num
if type(prod) is int:
    char_a = True
else:
    char_a = False
# output: False
# b.
A = [4, 3, 2, 7]
B = [6, 10, 9, 3, 8]
combined = A + B
if len(combined) == 9:
    char_b = True
else:
    char_b = False
# output: True
# c.
rmndr = 140 % 3
if rmndr <= 3:
    char_c = True
else:
    char_c = False
# output: True
# d.
divis = 27 % 5 
multip = 219 % 73
if divis == 0 and multip == 0:
    char_d = True
else: 
    char_d = False
# output: False
# e.
string = 'Hello World'
if len(string) >= 10:
    char_e = True
else:
    char_e = False
# output: True

# Problem 17
s = 'abcdefghijklmnopqrstuvwxyz'
# a. 
string_a = s[15] + s[24] + s[19] + s[7] + s[14] + s[13]
# b.
string_b = s[8] + s[2] +  s[18]
# c.
string_c = s[3] + s[6] + s[-3] + s[19]
# d.
string_d = s[15] + s[17] + s[14] + s[6] + s[17]+ s[0] + s[12]