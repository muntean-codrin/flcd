import re


class Grammar:
    def __init__(self, file):
        self.starting_symbol = "program"
        self.file_name = file
        self.non_terminals = set()
        self.terminals = set()
        self.productions = set()
        self.productions_for_non_terminal = {}
        self.read_from_file()

    def read_from_file(self):
        file = open(self.file_name, "r")
        lines = file.readlines()
        for line in lines:
            self.process_line(line.strip())

    def process_line(self, line):
        if line:
            self.productions.add(line)
            left_side, right_side = line.split("::=")
            non_terminal = left_side.strip()
            production = right_side.strip()
            self.non_terminals.add(non_terminal)
            if non_terminal not in self.productions_for_non_terminal.keys():
                self.productions_for_non_terminal[non_terminal] = [production]
            else:
                self.productions_for_non_terminal[non_terminal].append(production)
            matches = re.findall(r"\"[^\"]*\"", production)
            for match in matches:
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


    def print_menu(self):
        print("1. Terminals")
        print("2. Non-terminals")
        print("3. Productions")
        print("4. Productions for non-terminal")
        print("5. Cfg check")

    def menu(self):
        while True:
            self.print_menu()
            option = input("Option: ")
            if option == "1":
                print_list(self.terminals)
            elif option == "2":
                print_list(self.non_terminals)
            elif option == "3":
                print_list(self.productions)
            elif option == "4":
                non_terminal = input("Non-terminal: ")
                print(self.productions_for_non_terminal[non_terminal])
            elif option == "5":
                if(self.is_cfg()):
                    print("Context free grammar")
                else:
                    print("Grammar is not context free")
            elif option == "q":
                break
                
def print_list(l):
    for element in l:
        print(element)


g = Grammar(input("File: "))
g.menu()