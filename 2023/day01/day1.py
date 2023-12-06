input_file = 'input0'
input_file = 'input1'
input_file = 'input'

numbers = []
with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')

        if l == '':
            continue

        first = None
        last =  None
        for c in l:
            if c.isdigit():
                if first is None:
                    first = c
                last = c

        if first is None:
            break
        numbers.append(int(first + last))

print(numbers)

print("#### Part 1 ####")
print("Answer is:", str(sum(numbers)))

#### PART 2 ####
print("============ Part 2 start ================")

numbers = []
digits_spell = {
        'one': '1',
        'two': '2',
        'three': '3',
        'four': '4',
        'five': '5',
        'six': '6',
        'seven': '7',
        'eight': '8',
        'nine': '9'
        }

with open(input_file, 'r') as fh:
    for l in fh:
        l = l.strip('\n')

        if l == '':
            continue

        first = None
        last =  None

        # O(n^2)
        for i in range(len(l)):
            subl = l[i:]

            # if we have a digit at the start of the substring
            if subl[0].isdigit():
                # process it

                # if it's our first digit (char or text) store it
                if first is None:
                    first = subl[0]

                # save it as a last digiet
                last = subl[0]

                # go to next substring
                continue 

            # does the string start with textual digit
            for k, v in digits_spell.items():
                if subl.startswith(k):
                    # if it's our first digit (char or text) store it
                    if first is None:
                        first = v

                    # save it as a last digiet
                    last = v

                    # once we've found one, break this loop
                    break


        numbers.append(int(first + last))

print(numbers)

print("#### Part 2 ####")
print("Answer is:", str(sum(numbers)))
