import re
from SymbolTable import SymbolTable

keyword_symbol_patterns = [
    r'def',
    r'->',
    r'numar',
    r';',
    r'printeaza',
    r'citeste',
    r'daca',
    r'altfel daca',
    r'altfel',
    r'si',
    r'sau',
    r':\(',
    r':\)',
    r'\[',
    r'\]',
    r'\+',
    r'-',
    r'\*',
    r'/',
    r'<',
    r'<=',
    r'=',
    r'>=',
    r'==',
    r'\n'
]

variable_constant_patterns = [
    r'[a-zA-Z_][a-zA-Z_0-9]*',  # Match variable names
    r'"[^"]*"',  # Match string constants
    r'\d+'  # Match number constants
    r'.*'
]



token_patterns = keyword_symbol_patterns + variable_constant_patterns


class Scanner:
    def __init__(self, symbol_table, input_file):
        self.symbol_table = symbol_table
        self.sourceCodeFile = input_file
        tokenFile = open("token.in", "r")
        self.tokenFileContent = [line.strip() for line in tokenFile.readlines()]
        self.PIF = []
   
    
    def scan(self):
        token_regex = '|'.join(token_patterns)
        fin = open(self.sourceCodeFile, "r")
        i = 1
        isError = 0
        for line in fin:
            #print("Line " + str(i) + ":")
            i = i + 1
            tokens = re.findall(token_regex, line)

            # Print matched tokens
            lastToken = ''
            for token in tokens:
                if(token == "\n"):
                    continue
                if(token in self.tokenFileContent):
                    self.PIF.append((token, -1))
                elif(token.isidentifier() and lastToken == "def"):
                    self.PIF.append(('id', token))
                    self.symbol_table.add(token, 0)
                elif(token.isidentifier()):
                    try:
                        self.symbol_table.get(token)
                    except:
                        print("Error at line {}, token {}".format(i, token))
                        isError = 1
                elif (token.isdigit() or token[0] == '"'):
                    self.PIF.append(('const', token))
                    self.symbol_table.add(token, token)
                else:
                   print("Error at line {}, token {}".format(i, token))
                   isError = 1
                lastToken = token
        return isError
            
                
                
                
if __name__ == "__main__":

    symbol_table = SymbolTable(6)
    scanner = Scanner(symbol_table, "p1.txt")
    isError = scanner.scan()
    
    if(isError == 0):
        print("lexically correct")
    else:
        print("lexically incorrect")
    

    with open("PIF.out", "w") as f:
        f.write("{}".format(scanner.PIF))

    with open("ST.out", "w") as f:
        f.write("{}".format(symbol_table))
    
