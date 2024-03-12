def calculate(number1, number2, operation):
    if operation == "x":
        return number1 * number2
    if operation == "+":
        return number1 + number2
    if operation == "-":
        return number1 - number2
    if operation == "/":
        return number1/number2

def calculate_line(rest):
    return calculate(int(rest[1]), int(rest[2]), rest[0])

# def process_line( lines, i):
#     instruction, *rest = lines[i].strip().split()
#     match instruction:
#         case "calc":
#             return "done"
#             # return calculate_line(rest)
#         case "goto":
#             if len(rest) > 1:
#                 return int(calculate_line(rest[1:]))
#             else:
#                 return int(rest[0])

#
def read_file():
    with open("step_4.txt", "r") as file:
        lines = [""] + file.readlines()

        i = 1
        lines_seen = set()

        while i < len(lines) - 1: 
            line = lines[i].strip()
            if line in lines_seen:
                print('Line', i, line)
                return i 

            lines_seen.add(line)

            instruction, *rest = line.split()

            match instruction:
                # case "calc":
                #     return int(calculate_line(rest))
                case "goto":
                    if len(rest) > 1:
                        # print("going to", rest[1:])
                        i = int(calculate_line(rest[1:])) 
                    else:
                        i = int(rest[0]) 
                case "remove":
                    j = int(rest[0])
                    lines.pop(j)
                    if i < j:
                        i += 1
                case "replace":
                     lines[int(rest[0])] = lines[int(rest[1])]
                     i += 1

        assert False

if __name__ == "__main__":
    step_4_answer = read_file()
    # print(step_4_answer)
    # Line 4478 goto 7760
    
    # number1 = int(input("First number: "))
    # number2 = int(input("Second number: "))
    # operation = input("Operation: ")
    # print(calculate(number1, number2, operation))