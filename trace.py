import copy
import ast
from utils import prettyPrint


def trace(code):
    # pass entire code or code as list
    if isinstance(code, str):
        code = code.splitlines()
    return traceHelper(code, variables = {}, functions = {})
### CITATION NOTE####
# I used ChatGPT/stackoverflow to figure out how eval and ast_literal eval work, 
# but the recursion logic itself is original
def traceHelper(code, variables, functions):
    input()
    # base case
    if code == []:
        return (variables, functions)
    # recursive case
    else:
        prettyPrint(variables)
        line = code[0]
        rest = code[1:]
        # handle functions
        if 'def' in line:
            funcName = line[line.find('def')+3:line.find('(')].strip()
            params = line[line.find('(')+1:line.find(')')].split(',')
            params = [param.strip() for param in params]
            funcBody = []
            for i in range(len(rest)):
                currentLine = rest[i]
                # must be part of the function
                if currentLine.startswith(' ') or currentLine.startswith('\t'):
                    currentLine = currentLine.strip()
                    funcBody.append(currentLine)
                else:
                    # end funcion here
                    break 
            functions[funcName] = {
                'params': params,
                'body': funcBody
            }
            # skip to rest of code to mitigate against inf recursion
            return traceHelper(rest[len(funcBody):], variables, functions)
        
        # handle variable assignment
        elif '=' in line:
            variableName = line[:line.find('=')].strip()
            variableValue = line[line.find('=')+1:].strip()

            # evaluate python expressions from a string (convert strings to floats)
            # https://stackoverflow.com/questions/15197673/using-pythons-eval-vs-ast-literal-eval 
            try:
                variables[variableName] = eval(variableValue, {}, variables)
            except:
                variables[variableName] = variableValue
        
        # handle function calls
        elif '(' in line and ')' in line:
            funcName = line[:line.find('(')].strip()
            argsList = line[line.find('(')+1:line.find(')')].split(',')
            args = [arg.strip() for arg in argsList]
            # if the function is defined
            if funcName in functions:
                # use deepcopy since `variables` is a dict
                scopedVariables = copy.deepcopy(variables)
                
                # extract function information
                paramsList = functions[funcName]['params']
                funcBody = functions[funcName]['body']
                
                # assign param to passed in arg value
                for i in range(len(paramsList)):
                    currentParam = paramsList[i]
                    currentArg = args[i]
                    try:
                        scopedVariables[currentParam] = ast.literal_eval(currentArg)
                    except:
                        scopedVariables[currentParam] = eval(currentArg, {}, variables)
            
            for funcLine in funcBody:
                if 'print' in funcLine:
                    printLine = funcLine[funcLine.find('print')+5:].strip()
                    # used chatgpt to figure out how eval works here
                    output = eval(printLine, {}, scopedVariables)
                    print(f'Output: {output}')
                # recursively trace the rest of the function
                else:
                    traceHelper([funcLine], scopedVariables, functions)

        return traceHelper(rest, variables, functions) 

if __name__ == '__main__':
    code = """
    x = 10
    y = 25

    def add(a, b):
        result = a + b
        print(result)

    add(x, y)
    """

    trace(code)