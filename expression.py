class Expression:

    def printLogicTable(self, conditions=None):
        if conditions is None:
            conditions = {}
        if self._table is None:
            self._generateTable()
        string = ""
        print(self._expression)
        for lines in range(len(self._table)):
            printLine = True
            for condition in conditions:
                if condition in self._expression:
                    value = self._table[lines][self._expression.index(condition)] == "V"
                    if value != conditions[condition]:
                        printLine = False
                        break
            if printLine:
                for char_index, letter in enumerate(self._table[lines]):
                    if char_index == self._result_index:
                        string += f'\033[92m{letter}\033[0m'
                    else:
                        string += letter
                # string += str(table[lines])
                string += "\n"
        print(string)
        # print(self._parenthesis_map)
        # print(self._used_characters)
        # print(self._priorities)

    def _getNextIndex(self, actual_index, element):
        # a regra para achar o próximo index para fazer a operação é simples, o atomo ao lado, caso não tenha
        # sido utilizado ou o resultado da maior prioridade e que seja menor que a prioridade atual sem descer
        # um nivel de parenteses o index é calculado para cada lado
        next_right = -1
        for index_near in range(actual_index, len(self._priorities)):
            if self._parenthesis_map[index_near] < self._parenthesis_map[actual_index]:
                break
            next_priority = self._priorities[index_near]
            if element > next_priority > 0 and self._used_characters[index_near] == 0:
                next_right = index_near
                break

        next_left = -1
        for index_near in range(actual_index, -1, -1):
            if self._parenthesis_map[index_near] < self._parenthesis_map[actual_index]:
                break
            next_priority = self._priorities[index_near]
            if element > next_priority > 0 and self._used_characters[index_near] == 0:
                next_left = index_near
                break

        # print(f"elemento: {element} left {self._priorities[next_left]} right {self._priorities[next_right]}")
        return next_left, next_right

    def _generateTable(self):
        symbols = "~^+|>="
        # expression = "(p^q)>r+(~p=(q+~r))"
        # expression = "~((~r+y^(~y+r))^~((p^q)+(~p^~q)))"
        # expression = "(r=q)>(p|(~r>(p+~q)))"
        # expression = "a^b+(c^~d>(e+f)^g+(h=i^(j+k)))"

        # primeiro passo é separar as letras e organizar por ordem alfabetica
        atoms = [letter for letter in self._expression if letter.isalpha()]
        atoms = list(dict.fromkeys(atoms))
        atoms.sort()

        # cada letra só pode ser usada uma vez por operação, essa lista faz o controle
        self._used_characters = [0 if letter not in "()" else 0 for letter in self._expression]

        # calcula o nivel maximo de parenteses (maior prioridade) e cria um mapa para ajudar
        # a localizar qual o proximo termo
        self._parenthesis_map = list()
        max_parenthesis = 0
        level = 0
        for character in self._expression:
            if character == "(":
                level += 1
            if character == ")":
                level -= 1
            self._parenthesis_map.append(level)
            if level > max_parenthesis:
                max_parenthesis = level

        # calcula as prioridades das operações, começando do maior nivel de parenteses até o menor
        # print(f"parenthesis nivel: {maxParenthesis}")
        self._priorities = [0 for _ in range(len(self._expression))]
        self._table = [[" " for _ in range(len(self._expression))] for _ in range(2 ** len(atoms))]
        priority = 2
        for parenthesis_level in range(max_parenthesis + 1, -1, -1):
            for symbol in symbols:
                for index, character in enumerate(self._expression):
                    if character.isalpha() or character.isdecimal():
                        self._priorities[index] = 1
                    # primeiro atribui a prioridade aos simbolos do nivel atual de parenteses,
                    # da esquerda para a direita
                    if character == symbol and self._parenthesis_map[index] == parenthesis_level:
                        self._priorities[index] = priority
                        priority += 1

        # print([str(p) for p in priorities])
        # inicializa todas as colunas com os atomos lógicos
        for column in range(len(self._expression)):
            for line in range(2 ** len(atoms)):
                character: str = self._expression[column]
                if character.isalpha():
                    order = 2 ** (len(atoms) - atoms.index(character) - 1)
                    if int(line / order) % 2 == 0:
                        self._table[line][column] = "V"
                    else:
                        self._table[line][column] = "F"
                if character.isdecimal():
                    self._table[line][column] = character

        # começando da prioridade 2, ele vai indo para cada simbolo e realiza a sua operação
        for element in range(2, priority):
            index = self._priorities.index(element)
            symbol = self._expression[index]
            if symbol == "~":
                if self._expression[index + 1] != "(":
                    self._used_characters[index + 1] += 1
                    for line in range(2 ** len(atoms)):
                        if self._table[line][index + 1] == "F":
                            self._table[line][index] = "V"
                        else:
                            self._table[line][index] = "F"
                else:
                    index_next = -1
                    big = 0
                    for i in range(index, len(self._priorities)):
                        nextPriority = self._priorities[i]
                        if self._parenthesis_map[i] < self._parenthesis_map[index]:
                            break
                        if element > nextPriority > big:
                            index_next = i
                            big = nextPriority

                    self._used_characters[index_next] += 1
                    for line in range(2 ** len(atoms)):
                        if self._table[line][index_next] == "F":
                            self._table[line][index] = "V"
                        else:
                            self._table[line][index] = "F"

            if symbol == "^":
                nextLeft, nextRight = self._getNextIndex(index, element)

                self._used_characters[nextLeft] += 1
                self._used_characters[nextRight] += 1
                for line in range(2 ** len(atoms)):
                    if self._table[line][nextLeft] == "V" and self._table[line][nextRight] == "V":
                        self._table[line][index] = "V"
                    else:
                        self._table[line][index] = "F"

            if symbol == "+":
                nextLeft, nextRight = self._getNextIndex(index, element)

                self._used_characters[nextLeft] += 1
                self._used_characters[nextRight] += 1
                for line in range(2 ** len(atoms)):
                    if self._table[line][nextLeft] == "V" or self._table[line][nextRight] == "V":
                        self._table[line][index] = "V"
                    else:
                        self._table[line][index] = "F"

            if symbol == "|":
                nextLeft, nextRight = self._getNextIndex(index, element)

                self._used_characters[nextLeft] += 1
                self._used_characters[nextRight] += 1
                for line in range(2 ** len(atoms)):
                    if (self._table[line][nextLeft] == "V" or self._table[line][nextRight] == "V") and \
                            not self._table[line][nextLeft] == self._table[line][nextRight]:
                        self._table[line][index] = "V"
                    else:
                        self._table[line][index] = "F"

            if symbol == ">":
                nextLeft, nextRight = self._getNextIndex(index, element)

                self._used_characters[nextLeft] += 1
                self._used_characters[nextRight] += 1
                for line in range(2 ** len(atoms)):
                    if not (self._table[line][nextLeft] == "V" and self._table[line][nextRight] == "F"):
                        self._table[line][index] = "V"
                    else:
                        self._table[line][index] = "F"

            if symbol == "=":
                nextLeft, nextRight = self._getNextIndex(index, element)

                self._used_characters[nextLeft] += 1
                self._used_characters[nextRight] += 1
                for line in range(2 ** len(atoms)):
                    if self._table[line][nextLeft] == self._table[line][nextRight]:
                        self._table[line][index] = "V"
                    else:
                        self._table[line][index] = "F"

        # print([str(i) for i in range(len(expression))])
        # print([letter for letter in expression])
        # print([str(i) for i in usedCharacters])
        # print(expression)
        self._result_index = self._priorities.index(max(self._priorities))
        for line in range(len(self._table)):
            for index, character in enumerate(self._table[line]):
                if index == self._result_index:
                    self._result_column.append(character)
        # printTable(table, result)
        # print([p for p in priorities if p != 0])
        # print([str(l) for l in parenthesisMap])

    def __init__(self, expression: str):
        self._expression = expression
        self._result_index = -1
        self._table = None
        self._used_characters = list()
        self._parenthesis_map = list()
        self._priorities = list()
        self._result_column = list()
        self._generateTable()

    @staticmethod
    def printSymbols():
        print("~ : Negação")
        print("^ : Conjunção")
        print("+ : Disjunção")
        print("| : Disjunção Exclusiva")
        print("> : Condicional")
        print("= : Bicondicional")

    @staticmethod
    def isEquivalent(p: "Expression", q: "Expression"):
        if len(p._result_column) != len(q._result_column):
            return False
        for index, value in enumerate(p._result_column):
            if value != q._result_column[index]:
                return False

        return True
