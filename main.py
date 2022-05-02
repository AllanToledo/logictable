from expression import Expression

if __name__ == "__main__":
    P = Expression("p>q+r=s^~p>r")
    P.printLogicTable()
    P.printLogicTable({"r": True})
    # Q = LogicTable("(p^q)+(p^r")
    # Q.printTable()
    # print(LogicTable.isEquivalent(P, Q))
    # A = LogicTable("((p>q)>r)=~(p>(q>r))")
    # A.printTable()
