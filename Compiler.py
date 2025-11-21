# global variables
data_added = False
data_finished = False
COUNTER = 4000
register_count = 0
asm_file = None

functions = {
}

addresses = {
}

datas = {}


registers = {
    "0": "$zero"
}

operators = {'+', '-', '*', '/', '%', '<', '>'}

register_arr = [0] * 32


# Sets up zero register and in array intializes value
# Sets up newline data
def setUp():
    register_arr[0] = 0
    datas[r'\n'] = "newline"


def tokenize(code):
    tokens = code.split()
    return tokens


def createVariable(tokens):
    global COUNTER, register_count
    varName = tokens[1]
    value = tokens[3]
    currRegister = "$t" + str(register_count)
    registers[varName] = currRegister
    register_count += 1
    addresses[currRegister] = COUNTER
    # increase counter of address by 4 bits (int)
    COUNTER += 4
    return currRegister, value


# Handles operations
def compileOperations(operator, operand1, operand2, overflowReg):
    if (operator == "%"):
        asm_file.write("div " + operand1 + ", " + operand2 + "\n")
        asm_file.write("mfhi " + overflowReg + "\n")

    elif (operator == "+" and operand2.isdigit()):
        asm_file.write("addi " + operand1 + ", " + operand1 + ", " + operand2 + "\n" )




def compile(tokens):
    global data_added, data_finished
    tempRegOffset = 0

    # const / .data
    if tokens[0] == "const" and tokens[1] == "char*":
        if (data_added == False):
            asm_file.write(".data\nnewline: .asciiz \"\\n\"\n")
            data_added = True
        varName = tokens[2]
        varString = tokens[4]
        datas[varName] = varName
        asm_file.write(varName + ": .asciiz " + varString + "\n")
        return

    # to ignore non translating lines
    if (tokens[0] == "#include" or tokens[0] == "{" or tokens[0] == "}"):
        return

    # to print out the globl main text stuff
    if (data_finished == False):
        asm_file.write(".text\n.globl main\n")
        data_finished = True


    # turning labels into mips labels
    if tokens[0].endswith(":"):
        label = tokens[0]
        asm_file.write(label + "\n")
        return

    # turning methods into labels
    if tokens[0] == "int" and tokens[2] != "=":
        methodName = tokens[1]
        asm_file.write(methodName + ":\n")
        return

    # INT assignment to li and also store in registers and memory dictionary
    if tokens[0] == "int" and tokens[2] == "=":
        currRegister, value = createVariable(tokens)
        asm_file.write("li " + currRegister + ", " + value + "\n")
        return

    # Operation handling without conditional statement
    if len(tokens) > 2 and tokens[0].isalpha() and tokens[1] == "=":
            # deals with first operand
            if (tokens[2].isalpha()):
                operand1 = registers.get(tokens[2])

            # operator
            operator = tokens[3]

            # deals with second operand
            if (tokens[4].isdecimal()):
                operand2 = tokens[4]
            elif (tokens[4].isalpha()):
                operand2 = registers.get(tokens[4])

            # Overflow reg for necessary operations
            overflowReg = "$t" + str(register_count + tempRegOffset)

            compileOperations(operator, operand1, operand2, overflowReg)
            return

    # handle if statements
    if tokens[0] == "if":
        finalReg = ""
        operand1 = ""
        operand2 = ""

        if (tokens[2][0] in operators):
            # deals with first operand
            if (tokens[1].isalpha()):
                operand1 = registers.get(tokens[1])

            # operator
            operator = tokens[2]

            # deals with second operand
            if (tokens[3].isdecimal()):
                operand2 = "$t" + str(register_count + tempRegOffset)
                asm_file.write("li " + operand2 + ", " + tokens[3] + "\n")
                tempRegOffset += 1
            elif (tokens[3].isalpha()):
                operand2 = registers.get(tokens[3])

            # Overflow reg for necessary operations
            overflowReg = "$t" + str(register_count + tempRegOffset)

            compileOperations(operator, operand1, operand2, overflowReg)
            finalReg = overflowReg

        if (len(tokens) >= 6 and tokens[2] == ">"):
            asm_file.write("bgt " + operand1 + ", " + operand2 + ", " + tokens[5] + "\n")

        if (len(tokens) >= 8 and tokens[4] == "==" and tokens[5] == "0"):
            asm_file.write("beq " + finalReg + ", "+ registers.get("0") + ", " + tokens[7] + "\n")
        return

    # Handles goto to jump
    if tokens[0] == "goto":
        jumpLabel = tokens[1]
        asm_file.write("j " + jumpLabel + "\n")
        return

    # Handles printf and return to syscall
    if tokens[0].startswith("printf") or tokens[0].startswith("return"):
        arg = ""
        parts = tokens[0].split("printf", 1)
        # determines type for li $v0
        numTellsType = "0"

        if tokens[0] == "return":
            numTellsType = "10"
        elif "%d" in parts[1] :
            numTellsType = "1"
            if (tokens[1].isdecimal()):
                arg = "$t" + str(register_count + tempRegOffset)
            elif (tokens[1].isalpha()):
                arg = registers.get(tokens[1])
        else:
            numTellsType = "4"

        asm_file.write("li $v0, " + numTellsType + "\n" )

        if tokens[0] == "return":
            asm_file.write("")
        else:
            parts[1] = parts[1].replace('"', "")
            if parts[1] in datas:
                arg = datas[parts[1]]
                asm_file.write("la $a0, " + arg + "\n")
            else:
                asm_file.write("move $a0, " + arg + "\n")


        asm_file.write("syscall\n")
        return

    asm_file.write("XXXXXXNOTIMPLEMENTEDYETXXXXXXX\n")


def main():
    global data_added, COUNTER, register_count, asm_file

    setUp()

    c_filePath = "/Users/nandana/PycharmProjects/Compiler/src/fizzbuzz_simple.c"
    asm_filePath = "/Users/nandana/PycharmProjects/Compiler/src/fizzbuzz.asm"

    asm_file = open(asm_filePath, "w")

    with open(c_filePath, "r") as c_file:
        code = c_file.read()

        for line in code.splitlines():
            tokens = tokenize(line)
            # empty lines
            if not tokens:
                continue
            # cleanup
            for i in range(len(tokens)):
                tokens[i] = tokens[i].replace("(", "").replace(")", "").replace(";", "")
            compile(tokens)

    asm_file.close()


if __name__ == "__main__":
    main()


