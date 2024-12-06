import copy
import ast
from utils import countWhiteSpace

"""
[CITATION NOTE]
To make this makeshift interpreter work, I needed to be able to evaluate expressions, 
so I got help from ChatGPT with learning how eval and ast.literal_eval work.
The recursive algorithmic structure is original, but any line(s) that calls either of those methods
were inspired or copied from GPT.
"""

def executeFunction(funcName, args, scopedVariables, functions, codeSteps):
    # get necessary function info
    paramsList = functions[funcName]['params']
    funcBody = functions[funcName]['body']
    # keeps track of relative indents within a function using a helper function
    whiteSpaceCounts = [countWhiteSpace(line) for line in funcBody]
    minWhiteSpace = min(whiteSpaceCounts)
    funcBody = [line[minWhiteSpace:] for line in funcBody]
    # assign every param to respective arg value
    for i in range(len(paramsList)):
        currentParam = paramsList[i]
        currentArg = args[i]
        try:
            scopedVariables[currentParam] = ast.literal_eval(currentArg)
        except:
            scopedVariables[currentParam] = eval(currentArg, {}, scopedVariables)
    # execute the function line by line
    # use a while loop so we can skip around code blocks within the function
    currentLine = 0
    while currentLine < len(funcBody):
        funcLine = funcBody[currentLine]
        currentLine += 1
        # these conditionals are similar to the ones in trace helper
        if funcLine.startswith('if'):
            ifCondition = funcLine[funcLine.find('if')+len('if'):funcLine.find(':')].strip()
            # don't need to worry about rest since currentLine keeps track     
            ifBody, _ = getIndentBody(funcBody[currentLine:]) 
            # execute if body
            executeIf(ifCondition, ifBody, scopedVariables, functions, codeSteps)
            # shift currentLine so we don't reevaluate any lines
            currentLine += len(ifBody)
        elif funcLine.startswith('print'):   
            # execute print 
            executePrint(funcLine, scopedVariables, codeSteps)
        elif 'while' in funcLine:
            whileCondition = funcLine[funcLine.find('while')+len('while'):funcLine.find(':')].strip()
            # don't need to worry about rest since currentLine keeps track     
            whileLoop, _ = getIndentBody(funcBody[currentLine:]) 

            # execute if body
            executeWhile(whileCondition, whileLoop, scopedVariables, functions, codeSteps)
            # shift currentLine so we don't reevaluate any lines
            currentLine += len(whileLoop)
        else:
            # keep going
            traceHelper([funcLine], scopedVariables, functions, codeSteps)

def executePrint(line, variables, codeSteps):
    printExpr = line[line.find('print')+len('print'):].strip()
    output = eval(printExpr, {}, variables)
    codeSteps.append(f"Printed: {output}")

def executeIf(condition, body, variables, functions, codeSteps):
    # evaluate the condition
    boolValue = eval(condition, {}, variables)
    # only need to process if block if boolValue is True
    # otherwise, nothing happens 
    if boolValue:
        codeSteps.append(f'If condition is True')
        codeSteps.append(f'Entering if block...')
        for ifLine in body:
            if 'print' in ifLine:
                executePrint(ifLine, variables, codeSteps)
            else:
                traceHelper([ifLine], variables, functions, codeSteps)
    else:
        codeSteps.append(f'If condition is False')

def executeWhile(condition, body, variables, functions, codeSteps):
    # evaluate the condition
    boolValue = eval(condition, {}, variables)
    # run while loop while it evaluates to true
    while boolValue:
        # track while condition
        codeSteps.append(f'While condition [{condition}] is {boolValue}')
        for whileLine in body:
            traceHelper([whileLine], variables, functions, codeSteps)
        # processed the while loop, recheck if the condition is still true
        boolValue = eval(condition, {}, variables)
        # helpful to track condition after it is rechecked

def getIndentBody(lines):
    body = []
    currentLine = 0
    
    # Collect indented lines
    while currentLine < len(lines) and (lines[currentLine].startswith(' ') or lines[currentLine].startswith('\t')):
        body.append(lines[currentLine].strip())
        currentLine += 1
    
    # Remaining lines are those after the block
    restLines = lines[currentLine:]
    
    return body, restLines

def getFuncBody(rest):
    funcBody = []
    baseIndent = None
    lineIndex = 0
    while lineIndex < len(rest):
        currentLine = rest[lineIndex]
        # get current line indent level
        currentIndent = countWhiteSpace(currentLine)
        # set the base indent, ignore whitespace lines
        if baseIndent is None and currentLine.strip() != '':
            baseIndent = currentIndent
        # must be part of the function
        if currentIndent >= baseIndent and currentLine.strip() != '':
            funcBody.append(currentLine)
            lineIndex += 1
        else:
            # end function body here
            break 
    # remove processed lines from rest
    restLines = rest[lineIndex:]
    return funcBody, restLines

def getFuncInfoFromDefinition(line):
    # extract the function name and parameters
    funcName = line[line.find('def')+3:line.find('(')].strip()
    params = line[line.find('(')+1:line.find(')')].split(',')
    params = [item.strip() for item in params]
    return funcName, params 

def getFuncInfoFromCall(line):
    # extract the called function name and passed in arguments
    funcName = line[:line.find('(')]
    args = line[line.find('(')+1:line.find(')')].split(',')
    return funcName, args

def trace(code):
    if isinstance(code, str):
        code = code.splitlines()
    
    variables = {}
    functions = {}
    codeSteps=[]

    traceHelper(code, variables, functions, codeSteps)
    # only want to keep track of execution steps
    return codeSteps

def traceHelper(code, variables, functions, codeSteps):
    # base case
    if code == []:
        return (variables, functions, codeSteps)
    # recursive case
    else:
        line = code[0]
        rest = code[1:]
        # completely skip lines with only whitespace
        if len(line.strip()) == 0:
            return traceHelper(rest, variables, functions, codeSteps)
        codeSteps.append(f'Executing line: {line.strip()}')
        # handle function definitions 
        if 'def' in line:
            # collect function name, parameters, and body of the function
            funcName, params = getFuncInfoFromDefinition(line)
            funcBody, rest = getFuncBody(rest)
           
            functions[funcName] = {
                'params': params,
                'body': funcBody,
            }
            # skip to rest of code
            return traceHelper(rest, variables, functions, codeSteps)
        # handle variable assignment
        elif '=' in line:
            # collect variable name and its value
            variableName = line[:line.find('=')].strip()
            variableValue = line[line.find('=')+len('='):].strip()
            # evaluate python expressions from a string (convert strings to floats)
            # https://stackoverflow.com/questions/15197673/using-pythons-eval-vs-ast-literal-eval 
            try:
                variables[variableName] = eval(variableValue, {}, variables)
                codeSteps.append(f"Assigned: {variableName} = {variables[variableName]}")  # Debug assignment
            except:
                variables[variableName] = variableValue
            # skip to rest of code
            return traceHelper(rest, variables, functions, codeSteps)
        # handle print statements outside function
        elif 'print' in line:
            executePrint(line, variables, codeSteps)
            # skip to rest of code
            return traceHelper(rest, variables, functions, codeSteps)
        # handle function calls
        elif '(' in line and ')' in line:
            # extract the function name and the arguments
            funcName, args = getFuncInfoFromCall(line)
            # check that the function is registered
            if funcName in functions:
                
                # create a local scope for variables passed in
                scopedVariables = copy.deepcopy(variables)
                executeFunction(funcName, args, scopedVariables, functions, codeSteps)
        # handle if blocks
        elif 'if' in line:
            # extract if condition
            ifCondition = line[line.find('if')+len('if'):line.find(':')].strip()     
            # extract if body
            ifBody, rest = getIndentBody(rest)
            # execute the if block
            executeIf(ifCondition, ifBody, variables, functions, codeSteps)
            # skip to rest of code
            return traceHelper(rest, variables, functions, codeSteps)
        # handle while loop
        elif 'while' in line:
            # extract while loop condition
            whileCondition = line[line.find('while')+len('while'):line.find(':')].strip()
            # extract while loop body
            whileBody, rest = getIndentBody(rest)
            # execute the while loop
            executeWhile(whileCondition, whileBody, variables, functions, codeSteps)
            # skip to rest of code
            return traceHelper(rest, variables, functions, codeSteps)
        
        return traceHelper(rest, variables, functions, codeSteps) 
    
    