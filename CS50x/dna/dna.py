import csv
import sys


def main():

    # TODO: Check for command-line usage
    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")


    # TODO: Read database file into a variable
    # #list of dictionary

    people = []
    csvfile = sys.argv[1]
    with open(csvfile, "r")as datafile:
        reader = csv.DictReader(datafile)
        for row in reader:       #for every row(item)
            people.append(row)

        print(people)
        print(int(len(people)))
        print(people[0].keys())
        print(people[0].values())
        print(len(people[0].values()))
        print(list(people[0].values())[2])

    # TODO: Read DNA sequence file into a variable(string)
    textfile = sys.argv[2]
    with open(textfile)as sequencefile:
        sequence = sequencefile.read().rstrip()

        print(sequence)



    # TODO: Find longest match of each STR in DNA sequence
    # # 몇번 반복되는지 횟수를 기록하기 위한 데이터가 필요한데 dictionary나 list 만들기. tuple은 값 변화시킬 수 없기 때문에 안좋음

    strcounts = []
    for key in people[0].keys():               # for every key in individual item(dictionary)
        match = str(longest_match(sequence, key))     # check for longest match
        strcounts.append(match)                  # sort it into a list

    print(strcounts)
    print(strcounts[2])

    for i in range(len(people)):                                        # 사람수 만큼 loop
        match_count = 0
        for j in range(len(people[0].values()))[1:]:                    #large.csv의 경우 9까지
            if(strcounts[j] == list(people[i].values())[j]):            # strcount와 people 리스트의 각 row를 (person)을 비교함
                match_count = match_count +  1
        if match_count == len(people[0].values()) - 1:
            print(people[i]["name"])
            exit()

    else:
        print("No Match")





    # TODO: Check database for matching profiles #만든 data structure(dict)랑 datafile 비교해서 match 있으면 print match

    return


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
