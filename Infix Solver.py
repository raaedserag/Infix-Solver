from pythonds.basic.stack import Stack
from pythonds.trees.binaryTree import BinaryTree

# Define sequential search ===> Return true or false
def search_this(lista, item):
    if item in lista:  # Search for the item in the list
        return True  # if found return true
    return False  # else, return false


# Define operators list ===> Return a list of operators
def operators_list():
    return ['*', '+', '-', '/', '^']


# Define the allowed chars ===> Return a list of sorted chars
def chars_list():
    sorted_c = ['(', ')', '*', '+', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '^']
    return sorted_c


# Define is operator? ===> Return true/false
def isoperator(c):
    if search_this(operators_list(), c):  # check if the item 'c' is found in the operators list or not
        return True
    return False


# Remove every white space
def remove_all_spaces(statement):
    for i in range(0, len(statement)):
        statement = statement.replace(' ', '')  # check every char in the statement and if = ' ', replace it with ''
    return statement


# Define Check_chars ===> return 'true' or the type of error
def check_statement(statement):
    o_brace = 0  # This variable holds number of open braces '('
    c_brace = 0  # This variable holds number of closed braces ')'

    for i in range(0, len(statement)):
        token = statement[ i]
        # This assignment of statement[i] to token helps to improve the run time and for simplicity
        #######################################################################################
        # FIRST CHECK: Check if the token isn't a valid char
        if not search_this(chars_list(), token):
            return 'Error: ' + token + ' Isn\'t a valid char for a mathematical operation'
        #######################################################################################
        # SECOND CHECK(WILL BE CONTINUED AFTER LAST 'FOR' LOOP): Check if the user has inputted the braces correctly
        if token == '(':
            o_brace += 1  # If the token is an open bracket, increase it's count by 1
        elif token == ')':
            c_brace += 1  # If the token is a closed bracket, increase it's count by 1
            ###############
            # And since the user must enter the open braces before the closed, so c_brace MUSTN'T be greater than o_brace
            if c_brace > o_brace:  # If this happens, show the error
                return 'Error: Missing ('
                ###############
        #########################################################################################
        # The next condition must be put, since all coming checks depend on the current and the next token
        if i < len(statement) - 1:
            n_token = statement[i + 1]
            # This assignment of statement[i+1] to n_token helps to improve the run time and for simplicity

            ######################################################################################################
            # THIRD CHECK: Check if the user has entered duplicated operators, but negative values are considered
            if isoperator(token) and isoperator(n_token) and n_token != '-':
                return 'Error: Duplicated operators ' + token + n_token
            #######################################################################################################
            # FOURTH CHECK: Check if the user has inputted an empty brackets
            if token == '(' and n_token == ')':
                return 'Error: Empty parenthesis ()'
            ########################################################################################################

    ###########################################################
    # SECOND CHECK CONTINUED: Check if o_brace != c_brace
    if o_brace != c_brace:
        if o_brace > c_brace:
            return 'Error: Missing )'
    ############################################################

    return 'True'  # If the statement has no of the above errors, return 'true'


def check_if_valid_operand(tested_operand):
    try:
        float(tested_operand)  # Check if the operand is a valid number
    except ValueError:  # If not, return false
        return False
    return True


# Define splitting infix equation ===> Returns a list of valid operands and operators \ return 'SYNTAX ERROR' if there is a non-valid operand
def split_equation(entered_eqn):
    splitter_equation = []  # This variable holds the splitter equation of operators and operands

    brackets_num = 0  # This variable holds count of all open and closed brackets (To do the last check)

    operator_num = 0  # This variable holds count of operators ( To do the last check)
    length = len(entered_eqn)  # This variable holds length of the equation
    digits = ''  # This variable holds every complete operand to append in the splitter_list
    for i in range(0, length):
        token = entered_eqn[i]
        # This assignment of entered_eqn[i] to token helps to improve the run time and for simplicity

        # The next condition must be put, since all coming checks depend on the current and the next token
        if i < length - 1:
            n_token = entered_eqn[i + 1]  # This assignment of entered_eqn[i+1] to n_token helps to improve the run time and for simplicity

        # First: if char is an open bracket
        if token == '(' or token== ')':  # If the token is a bracket

            if digits != '':  # If the digits has a valid operand in, append it to the list
                if check_if_valid_operand(digits):  # Append it only if it's valid
                    splitter_equation.append(digits)
                    digits = ''  # Remove the operand from the variable 'digits' after appending it
                else:
                    return 'SYNTAX ERROR'  # Or return the error message

            splitter_equation.append(token)  # Append the bracket
            brackets_num += 1  # Increase the count of brackets by 1

        # Second: if char is an operator
        elif isoperator(token):
            # First, Append the current operand
            if digits != '':  # If the digits has a valid operand in, append it to the list
                if check_if_valid_operand(digits):  # Append it only if it's valid
                    splitter_equation.append(digits)
                    digits = ''  # Remove the operand from the variable 'digits' after appending it
                else:
                    return 'SYNTAX ERROR'

            ''' If the operator is '-' & it's not the last char & the next char isn't operator & (it's the first char
            || the previous token is an open bracket || the previous bracket is an operator ==> the operator is just
            a negative mark to the next operand'''
            if i != length - 1 and token == '-' and (not isoperator(n_token)) and n_token != '(' and (
                        i == 0 or entered_eqn[i - 1] == '(' or isoperator(entered_eqn[i - 1])):
                digits = digits + token  # Append the negative mark before the operand

            # Else: this is a normal operator    
            else:
                splitter_equation.append(token)  # Append it to the splitter list
                operator_num += 1  # Increase the count of the operators

        # Third: if the token is a number
        else:
            digits = digits + token  # Append it to the operand digits variable

            # Continue for or end for

    if digits != '':  # If the digits has a valid operand in, append it to the list
        if check_if_valid_operand(digits):  # Append it only if it's valid
            splitter_equation.append(digits)
        else:
            return 'SYNTAX ERROR'
    # Finished every tokens

    # Calculate operands Count
    operand_num = len(splitter_equation) - operator_num - brackets_num  # Calculate operands count

    # Operands count must be = operators count + 1
    if operand_num != operator_num + 1:
        return 'SYNTAX ERROR'

    # Return the true syntax list of expression splitter 
    return splitter_equation


# Define converting to postfix
def infixToPostfix(infixexpr):
    prec = {}
    prec["^"] = 4
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr

    for token in tokenList:
        if token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        elif not isoperator(token):
            postfixList.append(token)
        else:
            while (not opStack.isEmpty()) and \
                    (prec[opStack.peek()] >= prec[token]):
                postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return postfixList


# Define build parse tree from full parenthesis expression
def buildParseTree(fpexp):
    fplist = fpexp.split()
    pStack = Stack()
    eTree = BinaryTree('')
    pStack.push(eTree)
    currentTree = eTree
    for i in fplist:
        if i == '(':
            currentTree.insertLeft('')
            pStack.push(currentTree)
            currentTree = currentTree.getLeftChild()
        elif i not in ['^', '+', '-', '*', '/', ')']:
            parent = pStack.pop()
            currentTree.setRootVal(float(i))
            currentTree = parent
        elif i in ['^', '+', '-', '*', '/']:
            currentTree.setRootVal(i)
            currentTree.insertRight('')
            pStack.push(currentTree)
            currentTree = currentTree.getRightChild()
        elif i == ')':
            currentTree = pStack.pop()
        else:
            raise ValueError
    return eTree


# Define convert to Fully parenthesis
def convert_to_full(statement):
    temp_list = ''  # This variable will hold every small full parenthesis equation
    opstack = Stack()  # This variable will hold the full parenthesis equation
    postfix_exp = infixToPostfix(statement)  # Convert infix expression to post fix(list)

    for i in postfix_exp:
        final_list = []

        if i in "/*+-^":  # If the token is an operator
            final_list.append('(')  # Start with ( ====> exp=[(]
            o2 = opstack.pop()  # Get second operand
            o1 = opstack.pop()  # Get first operand
            final_list.append(o1)  # Concat with first operand ===> exp=[(,op1]
            final_list.append(i)  # Concat with operator ===> exp=[(,op1,operator]
            final_list.append(o2)  # Concat with second operand ===> exp=[(,op1,operator,op2]
            final_list.append(')')  # Concat with ) ===> exp=[(,op1,operator,op2,)]
            temp_list = " ".join(
                final_list)  # Convert it to string with spaces ==>( op1 operator op2 )
            opstack.push(temp_list)  # Push it in the stack to do the next operations

        else:  # If the token is an operand ===> push it in the stack
            opstack.push(i)

    # After all tokens had finished, return the full parenthesis equation with one space between elements
    return temp_list


# Define Evaluation of Parse Tree =====> Returns the tree Value / MATHEMATICAL ERROR
def evaluate(parseTree):  # Modified

    ##############################################################################
    # If the current node is an operand(leaf) ===> return it's Value only and stop
    if not isoperator(parseTree.getRootVal()):
        return parseTree.getRootVal()
    ##############################################################################
    # If it's not a leaf(it's a node) ====> GET THE left and right BRANCH VALUE
    left_operand = evaluate(parseTree.getLeftChild())  # Recursive function to do the same with every parse tree
    right_operand = evaluate(parseTree.getRightChild())  # Do math fn return a value or return a string with ERROR

    # Check if the 2-branches has returned a value(float) or any of them has returned error(string)
    if type(left_operand) == float and type(right_operand) == float:
        return do_math(left_operand, right_operand, parseTree.getRootVal())  # If them returned value ===> return value

    # If any of the b ranches has an error ===> Indicate that error and return it
    else:
        if type(left_operand) == str:  # If the error is in the left side ===> return it
            return left_operand
        else:  # If the error is in the right side ===> return it
            return right_operand


# Define do Math ===> do operations and return the result or the value error
def do_math(op1, op2, operator):
    if operator == '+':
        return op1 + op2

    elif operator == '-':
        return op1 - op2

    elif operator == '*':
        return op1 * op2

    elif operator == '/':
        if op2 == 0:
            return 'ERROR: You can\'t divide by 0'
        return op1 / op2

    else:
        if op1 == 0:
            return 'ERROR: You can\'t Power of the base of 0'
        return op1 ** op2


# format printing ===> print as integer or as float
def printing(result):
    if type(result) == complex:
        print('Error: Imaginary Number')
    elif result.is_integer():
        print('= ', int(result))

    else:
        print('= ', float(result))


# Take the first input from the user and remove the spaces from it before storing it

user_input = remove_all_spaces(input('Please enter infix expression or enter \'end\' to terminate:\n')).lower()
while user_input != 'end':  # If the user hasn't inputted 'end' ===> continue the program
    check = check_statement(user_input)  # Check the statement and store the result in'check'
    if check != 'True':  # If there is an error===> print it and take the next input
        print(check)
    else:  # If it's a true statement ====> continue the program
        splitted = split_equation(user_input)  # Split every operand and operator and bracket in the statement to a list
        if splitted == 'SYNTAX ERROR':  # If there is an invalid operand, the split function will return error
            print(splitted)  # Print the error and take the next input
        else:  # If the splitter equation is correct ==> continue the program
            # Convert the splitter eqn to full parenthesis, then build the parse tree and evaluate it
            result = evaluate(buildParseTree(convert_to_full(splitted)))
            if type(result) != str:  # If the result is a Float ====> then the operation has done
                printing(result)  # Format printing of the result (integer/float)
            else:
                print(result)  # If the evaluate function has returned error ===> print it

    # Take the next input
    user_input = remove_all_spaces(input('Please enter infix expression or enter \'end\' to terminate:\n')).lower()
