import cs50

height = cs50.get_int("height: ")

while height < 1 or height > 8:
    height = cs50.get_int("height: ")


for i in range(height): #높이
    print(" " * (height-i-1), end="")
    print("#" * (i+1) , end="")
    print("  " , end="")
    print("#" * (i+1))

# for loop가 i = 0에서 시작하다보니 처음에 아무것도 없는 newline만들고 시작함.