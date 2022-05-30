import cs50

# ask user for text
text = cs50.get_string("Text: ")

letter_count = 0.00
word_count = 1.00
sentence_count = 0.00

for i in range(len(text)):
    if text[i].isalpha():
        letter_count += 1

    elif text[i].isspace():
        word_count += 1

    elif text[i] == "!" or text[i] == "." or text[i] == "?":
        sentence_count += 1


l = (letter_count / word_count) * 100
s = (sentence_count / word_count) * 100

index = round(0.0588 * l - 0.296 * s - 15.8)

# 21 words 3 sentences 80letters 22.4 -4.23 -15.8

# print(str(word_count))
# print(str(sentence_count))
# print(str(letter_count))
# print(str(index))
# print(str(l))
# print(str(s))


if index < 1:
    print("Before Grade 1")

elif index >= 16:
    print("Grade 16+")

else:
    print("Grade " + str(index))