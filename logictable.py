from expression import Expression
import sys

if __name__ == "__main__":
    P = Expression(sys.argv[1])
    values = sys.argv[2].split(",") if(len(sys.argv) > 2) else list()
    conditions = {}
    for value in values:
        param = value.split("=")
        conditions[param[0]] = param[1] == "True"
    P.printLogicTable(conditions)
