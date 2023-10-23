class HashTable:
    def __init__(self, size):
        self._size = size
        self._table = [[] for _ in range(size)]

    def hash(self, key):
        sum_char = sum(ord(c) for c in key)
        return sum_char % self._size

    def add(self, key, value):
        index = self.hash(key)
        slot = self._table[index]

        for i in range(len(slot)):
            if slot[i][0] == key:
                slot.pop(i)
                slot.append((key, value))
                return

        slot.append((key, value))

    def get(self, key):
        index = self.hash(key)
        slot = self._table[index]

        for pair in slot:
            if pair[0] == key:
                return pair[1]

        return None

    def remove(self, key):
        index = self.hash(key)
        slot = self._table[index]

        for i in range(len(slot)):
            if slot[i][0] == key:
                slot.pop(i)
                return

    def get_size(self):
        return self._size

    def __str__(self):
        result = f"Hash table size {self._size}:\n"
        for i in range(self._size):
            result += f"{i}: "
            slot = self._table[i]
            result += " ".join([f"[{pair[0]}={pair[1]}]" for pair in slot])
            result += "\n"
        return result


class SymbolTable:
    def __init__(self, size):
        self._table = HashTable(size)

    @property
    def size(self):
        return self._table.get_size()

    def get(self, identifier):
        variable_data = self._table.get(identifier)
        if variable_data is not None:
            return variable_data
        raise Exception("Variable not defined.")

    def add(self, identifier, value):
        self._table.add(identifier, value)

    def remove(self, identifier):
        self._table.remove(identifier)

    def __str__(self):
        return str(self._table)


if __name__ == "__main__":
    symbol_table = SymbolTable(6)

    symbol_table.add("a", 2)
    symbol_table.add("b", 3)
    symbol_table.add("str1", "test")
    symbol_table.add("g", 2)
    print(symbol_table)

    symbol_table.add("b", 15)
    symbol_table.remove("a")
    print(symbol_table)