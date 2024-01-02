import copy
import re

def list_to_string(l):
    list_as_string = ""
    for e in l:
        list_as_string += e + " "
    return list_as_string


class Grammar:
    def __init__(self, file):
        self.starting_symbol = "program"
        self.file_name = file
        self.non_terminals = set()
        self.terminals = set()
        self.productions = []
        self.productions_for_non_terminal = {}
        self.read_from_file()

    def read_from_file(self):
        file = open(self.file_name, "r")
        lines = file.readlines()
        for line in lines:
            self.process_line(line.strip())
        for i in range(len(self.productions)):
            self.productions[i] = self.productions[i].replace('\"', "")


    def process_line(self, line):
        if line:
            self.productions.append(line.strip())
            left_side, right_side = line.split("::=")
            non_terminal = left_side.strip()
            production = right_side.strip()
            production_list = production.split(" | ")
            self.non_terminals.add(non_terminal)
            if non_terminal not in self.productions_for_non_terminal.keys():
                self.productions_for_non_terminal[non_terminal] = production_list
            else:
                self.productions_for_non_terminal[non_terminal] += production_list
            matches = re.findall(r"\"[^\"]*\"", production)
            for match in matches:
                match = match[1:-1]
                self.terminals.add(match)

    def is_cfg(self):
        if self.starting_symbol not in self.non_terminals:
            return False
        for nonterminal in self.non_terminals:
            for nonterminal2 in self.non_terminals:
                if nonterminal == nonterminal2:
                    continue
                if self.productions_match(nonterminal, nonterminal2):
                    return False
        else:
            return True

    def productions_match(self, nonterminal1: str, nonterminal2: str) -> bool:
        productions1 = self.productions_for_non_terminal[nonterminal1]
        productions2 = self.productions_for_non_terminal[nonterminal2]

        if len(productions1) != len(productions2):
            return False
        for production in productions1:
            if production not in productions2:
                return False
        return True



class Parser:
    def __init__(self, grammer, program_file):
        self.diction = {}
        self.firsts = {}
        self.follows = {}
        self.grammar = grammer
        
        self.rules = ["program ::= stmtlist", "stmtlist ::= stmt stmtlist | #", "stmt ::= int"]
        self.non_terminals = ['program', 'stmtlist', 'stmt']
        self.terminals = ['int']
        self.program = "int int int"

        #self.rules = ["program ::= stmtlist", "stmtlist ::= stmt stmtlist | #", "stmt ::= simplstmt", "simplstmt ::= assignstmt", "assignstmt ::= identifier = expression ;", "identifier ::= letter identifier | #", "expression ::= digit", "letter ::= A | B | C | D", "digit ::= 0 | 1 | 2 | 3"]
        #self.non_terminals = ['program', 'stmtlist', 'stmt', 'simplstmt', 'assignstmt', 'identifier', 'expression', 'letter', 'digit']
        #self.terminals = ['A', 'B', 'C', 'D', '0', '1', '2', '3', '=', ';']
        #self.program = "A = 2 ; B = 3 ;"

        self.rules = list(grammer.productions)
        self.non_terminals = list(grammer.non_terminals)
        self.terminals = list(grammer.terminals)
        with open(program_file, 'r') as file:
            file_contents = file.read()
        self.program = file_contents.replace('\n', ' ')

        self.start_symbol = None
        self.tableTerminals = None
        self.parsing_table = None
        self.grammar_is_LL = None
        
        self.computeAllFirsts()
        self.start_symbol = list(self.diction.keys())[0]
        self.computeAllFollows()

    def first(self, rule):
        if len(rule) != 0 and (rule is not None):
            if rule[0] in self.terminals:
                return rule[0]
            elif rule[0] == '#':
                return '#'

        if len(rule) != 0:
            if rule[0] in list(self.diction.keys()):
                first_list = []
                rhs_rules = self.diction[rule[0]]
                for itr in rhs_rules:
                    indivRes = self.first(itr)
                    if type(indivRes) is list:
                        for i in indivRes:
                            first_list.append(i)
                    else:
                        first_list.append(indivRes)

                if '#' not in first_list:
                    return first_list
                else:
                    first_list.remove('#')
                    if len(rule) > 1:
                        ansNew = self.first(rule[1:])
                        if ansNew is not None:
                            if type(ansNew) is list:
                                return first_list + ansNew
                            else:
                                return first_list + [ansNew]
                        else:
                            return first_list
                    first_list.append('#')
                    return first_list

    def follow(self, nt):
        solset = set()
        if nt == self.start_symbol:
            solset.add('$')

        for curNT in self.diction:
            rhs = self.diction[curNT]
            for subrule in rhs:
                if nt in subrule:
                    while nt in subrule:
                        index_nt = subrule.index(nt)
                        subrule = subrule[index_nt + 1:]
                        if len(subrule) != 0:
                            res = self.first(subrule)
                            if '#' in res:
                                res.remove('#')
                                ansNew = self.follow(curNT)
                                if ansNew is not None:
                                    if type(ansNew) is list:
                                        res = res + ansNew
                                    else:
                                        res = res + [ansNew]
                                else:
                                    res = res
                        else:
                            if nt != curNT:
                                res = self.follow(curNT)

                        if res is not None:
                            if type(res) is list:
                                for g in res:
                                    solset.add(g)
                            else:
                                solset.add(res)
        return list(solset)

    def computeAllFirsts(self):
        for rule in self.rules:
            k = rule.split("::=")
            k[0] = k[0].strip()
            k[1] = k[1].strip()
            rhs = k[1]
            multirhs = rhs.split('|')
            for i in range(len(multirhs)):
                multirhs[i] = multirhs[i].strip()
                multirhs[i] = multirhs[i].split()
            self.diction[k[0]] = multirhs

        for y in list(self.diction.keys()):
            t = set()
            for sub in self.diction.get(y):
                res = self.first(sub)
                if res is not None:
                    if type(res) is list:
                        for u in res:
                            t.add(u)
                    else:
                        t.add(res)

            self.firsts[y] = t

    def computeAllFollows(self):
        for NT in self.diction:
            solset = set()
            sol = self.follow(NT)
            if sol is not None:
                for g in sol:
                    solset.add(g)
            self.follows[NT] = solset

    def createParseTable(self):
        ntlist = list(self.diction.keys())
        self.tableTerminals = copy.deepcopy(self.terminals)
        self.tableTerminals.append('$')

        self.parsing_table = []
        for x in self.diction:
            row = []
            for y in self.tableTerminals:
                row.append('')
            self.parsing_table.append(row)

        self.grammar_is_LL = True

        for lhs in self.diction:
            rhs = self.diction[lhs]
            for y in rhs:
                res = self.first(y)
                if '#' in res:
                    if type(res) == str:
                        firstFollow = []
                        fol_op = self.follows[lhs]
                        if fol_op is str:
                            firstFollow.append(fol_op)
                        else:
                            for u in fol_op:
                                firstFollow.append(u)
                        res = firstFollow
                    else:
                        res.remove('#')
                        res = list(res) + list(self.follows[lhs])
                ttemp = []
                if type(res) is str:
                    ttemp.append(res)
                    res = copy.deepcopy(ttemp)
                for c in res:
                    xnt = ntlist.index(lhs)
                    yt = self.tableTerminals.index(c)
                    if self.parsing_table[xnt][yt] == '':
                        self.parsing_table[xnt][yt] = self.parsing_table[xnt][yt] \
                                       + f"{lhs}::={' '.join(y)}"
                    else:
                        if f"{lhs}::={y}" in self.parsing_table[xnt][yt]:
                            continue
                        else:
                            self.grammar_is_LL = False
                            self.parsing_table[xnt][yt] = self.parsing_table[xnt][yt] \
                                           + f",{lhs}::={' '.join(y)}"


    def validateStringUsingStackBuffer(self):
        with open("out.txt", 'w') as file:
            print(f"\nParse the program: {self.program}\n")
            file.write(f"\nParse the program: {self.program}\n")
            if not self.grammar_is_LL:
                return f"\nInput String = \"{self.program}\"\nGrammar is not LL(1)"

            stack = [self.start_symbol, '$']
            buffer = ['$']

            input_string = self.program.split()
            input_string.reverse()
            buffer += input_string

            program_so_far = []

            while True:
                if stack == ['$'] and buffer == ['$']:
                    file.write("Stack: {}\nBuffer: {}\n{} ".format(' '.join(buffer), ' '.join(stack), "End of parsing!"))
                    return "\nValid String!"
                elif stack == ['$']:
                    return "\nUnmached String!"
                elif stack[0] not in self.terminals:
                    x = list(self.diction.keys()).index(stack[0])
                    if(buffer[-1] not in self.tableTerminals):
                        return f"\n{buffer[-1]} is not a terminal."
                    y = self.tableTerminals.index(buffer[-1])
                    if self.parsing_table[x][y] != '':
                        entry = self.parsing_table[x][y]
                        file.write("Stack: {}\nBuffer: {}\n\n".format(' '.join(stack),' '.join(buffer)))
                        lhs_rhs = entry.split("::=")
                        lhs_rhs[1] = lhs_rhs[1].replace('#', '').strip()
                        entryrhs = lhs_rhs[1].split()
                        stack = entryrhs + stack[1:]
                    else:
                        return f"\nInvalid String! No rule at Table[{stack[0]}][{buffer[-1]}]."
                else:
                    if stack[0] == buffer[-1]:
                        file.write("Stack: {}\nBuffer: {}\n{}\n\n".format(' '.join(stack), ' '.join(buffer), f"Removing match: \'{stack[0]}\'"))
                        buffer = buffer[:-1]
                        program_so_far.append(buffer[-1])
                        stack = stack[1:]
                    else:
                        return f"\nInvalid String! Unmatched sequence: \'{list_to_string(program_so_far[-4:])}\'"

    def runParser(self):
        self.createParseTable()

        if self.program is not None:
            print(self.validateStringUsingStackBuffer())
        else:
            print("\nNo input String detected")



class Program:
    def run(self):
        self.grammar = Grammar("grammar.txt")
        self.parser = Parser(self.grammar, "program.txt")
        self.menu()

    def print_menu(self):
        print("\n\n1. Terminals")
        print("2. Non-terminals")
        print("3. Productions")
        print("4. Productions for non-terminal")
        print("5. Cfg check")
        print("6. Parse program")
        print()

    def menu(self):
        while True:
            self.print_menu()
            option = input("Option: ")
            if option == "1":
                print_list(self.grammar.terminals)
            elif option == "2":
                print_list(self.grammar.non_terminals)
            elif option == "3":
                print_list(self.grammar.productions)
            elif option == "4":
                non_terminal = input("Non-terminal: ")
                print(self.grammar.productions_for_non_terminal[non_terminal])
            elif option == "5":
                if (self.grammar.is_cfg()):
                    print("Context free grammar")
                else:
                    print("Grammar is not context free")
            elif option == "6":
                self.parser.runParser()
            elif option == "q":
                break


p = Program()
p.run()
