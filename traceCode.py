import copy
import ast
from utils import prettyPrint

def trace(code):
    # pass entire code or code as list
    if isinstance(code, str):
        code = code.splitlines()
    return traceHelper(code, variables = {}, functions = {})

def traceHelper(code, variables, functions):
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
            variableValue = line[line.find('=')+len('='):].strip()

            # evaluate python expressions from a string (convert strings to floats)
            # https://stackoverflow.com/questions/15197673/using-pythons-eval-vs-ast-literal-eval 
            try:
                variables[variableName] = eval(variableValue, {}, variables)
            except:
                variables[variableName] = variableValue
        
        # handle function calls
        elif '(' in line and ')' in line:
            funcName = line[:line.find('(')].strip()
            argsList = line[line.find('(')+len('('):line.find(')')].split(',')
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
            
                for i in range(len(funcBody)):
                    funcLine = funcBody[i]
                    if 'if' in funcLine:
                        ifBody = []
                        ifExpr = funcLine[funcLine.find('if')+len('if'):-1].strip()
                        for i in range(i+1, len(funcBody)):
                            currentLine = funcBody[i]
                            print(currentLine)
                            # must be part of the function
                            if currentLine.startswith(' ') or currentLine.startswith('\t'):
                                currentLine = currentLine.strip()
                                ifBody.append(currentLine)
                            else:
                                # end funcion here
                                break 
                        print(f'[{ifBody}]')
                        boolValue = eval(ifExpr, {}, scopedVariables)
                    elif 'print' in funcLine:
                        printExpr = funcLine[funcLine.find('print')+len('print'):].strip()
                        # used chatgpt to figure out how eval works here
                        output = eval(printExpr, {}, scopedVariables)
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
        if result < 30:
            print('lower')
        print(f'result is {result}')

    add(x, y)
    """

    trace(code)