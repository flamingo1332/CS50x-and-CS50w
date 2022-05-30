import cs50

n = cs50.get_int("Number: ")

digits = []
count = 0


for i in range(16):
    digit = int((n / 10**(15-i)) % 10)
    digits.append(digit)

#digit[0] ~ digit[15]


for i in range(0, 16, 2):
    if digits[i] > 4:
        count = count + 1

# for i in
# if digit[0]>4 or digit[2]>4 or digit[4]>4 or digit[6]>4 or digit[8]>4 or digit[10]>4 or digit[12]>4 or digit[14]>4:
#     count

a = digits[14]*2 + digits[12]*2 + digits[10]*2 + digits[8]*2 + digits[6]*2 + digits[4]*2 + digits[2]*2 + digits[0]*2 - count*9
b = digits[15] + digits[13] + digits[11] + digits[9] + digits[7] + digits[5] + digits[3] + digits[1] + a


#16digit
if 999999999999999< n <10000000000000000:
    if b % 10 == 0:
        if digits[0]*10 + digits[1] == 51 or digits[0]*10 + digits[1] == 52 or digits[0]*10 + digits[1] == 53 or digits[0]*10 + digits[1] == 54 or digits[0]*10 + digits[1] == 55:
            print("MASTERCARD")
        elif digits[0] == 4:
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")

#15digit
elif 99999999999999< n <1000000000000000:
    if(b % 10 == 0):
        if digits[1]*10 + digits[2] == 34 or digits[1]*10 + digits[2] == 37:
            print("AMEX")
        else:
            print("INVALID")
    else:
        print("INVALID")


#13digit
elif 999999999999< n <10000000000000:
    if b % 10 == 0 and digits[3] == 4:
        print("VISA")
    else:
        print("INVALID")


#else
else:
    print("INVALID")