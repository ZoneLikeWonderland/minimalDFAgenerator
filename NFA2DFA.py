def run(inputstr):
    alphabet = set()

    inputstr = inputstr.strip().split("\n")
    NFAstate = {i for i in inputstr[0].split(" ")}
    NFApath = {}
    start = inputstr[1].split(" ")[0]
    accepting = set(inputstr[1].split(" ")[1:])
    for i in inputstr[2:]:
        j = i.split(" ")
        if j[0] not in NFApath:
            NFApath[j[0]] = {}
        for k in j[2:]:
            if k != 'e':
                alphabet.add(k)
            if k not in NFApath[j[0]]:
                NFApath[j[0]][k] = set()
            NFApath[j[0]][k].add(j[1])
    print("alphabet", alphabet)
    print("NFApath", NFApath)
    # print(NFAstate)

    def e_expand(stateset: set):
        queue = sorted(stateset)
        newstateset = {i for i in stateset}
        expanded = set()
        while len(queue) > 0:
            state = queue[0]
            queue = queue[1:]
            if state in NFApath and 'e' in NFApath[state] and state not in expanded:
                expanded .add(state)
                queue.extend(list(NFApath[state]['e']))
                newstateset |= NFApath[state]['e']
        return newstateset

    def move(stateset: set, c: str):
        nextStateSet = set()
        for j in stateset:
            if j in NFApath and c in NFApath[j]:
                nextStateSet |= NFApath[j][i]
        return nextStateSet

    DFApath = {}
    start = e_expand({start})
    mark = [str(sorted(start))]
    acceptingState = set()
    queue = [start]

    while len(queue) > 0:
        nowStateSet = queue[0]
        queue = queue[1:]
        # print(nowStateSet)
        if len(nowStateSet & accepting) > 0:
            acceptingState.add(str(sorted(nowStateSet)))
        for i in alphabet:
            nextStateSet = move(nowStateSet, i)
            if len(nextStateSet) > 0:
                nextStateSet = e_expand(nextStateSet)
                if str(sorted(nextStateSet)) not in mark:
                    queue.append(nextStateSet)
                    mark.append(str(sorted(nextStateSet)))
                if str(sorted(nowStateSet)) not in DFApath:
                    DFApath[str(sorted(nowStateSet))] = {}
                DFApath[str(sorted(nowStateSet))][i] = str(
                    sorted(nextStateSet))

    # print(mark)
    print("DFApath", DFApath)

    DFAstate2id = {j: i for i,
                   j in zip(range(len(mark)), mark)}
    print("DFAstate2id", DFAstate2id)

    DFApathSimple = {
        DFAstate2id[i]: {
            k: DFAstate2id[l] for k, l in j.items()
        } for i, j in DFApath.items()
    }
    # print(acceptingState)
    # print(DFAstate2id[str(sorted(acceptingState))])
    print()
    print("DFApathSimple", DFApathSimple)

    # Minimize

    def inwhich(state: int, P: list):
        for i in range(len(P)):
            if state in P[i]:
                return i
        return None

    P = [{DFAstate2id[i] for i in acceptingState}]
    unaccepting = {i for i in range(len(DFAstate2id))}-P[0]
    if len(unaccepting) > 0:
        P.append(unaccepting)

    # print(start)
    print(P)
    j = -1
    while j < len(P)-1:
        # print(P)
        j += 1
        statesetSimple = P[j]
        # print("now", statesetSimple)
        for c in alphabet:
            wait = {}
            for state in statesetSimple:
                if state not in DFApathSimple or c not in DFApathSimple[state]:
                    pos = -1
                else:
                    pos = inwhich(DFApathSimple[state][c], P)
                if pos not in wait:
                    wait[pos] = []
                wait[pos].append(state)
            # print(c, wait)
            if len(wait) > 1:
                P.remove(statesetSimple)
                for i in wait:
                    P.append(set(wait[i]))
                j = -1
                break
    print(P)

    redirect = [0 for i in range(len(DFAstate2id))]
    for i in P:
        p = i.pop()
        for j in i | {p}:
            redirect[j] = p
    print(redirect)
    print(redirect[DFAstate2id[str(sorted(start))]])

    nodeTemplate = "\\node[state{ac}][{relapos}]({id}){{{text}}};"
    edgeTemplate = "({begin})edge{edgeset} node{{{char}}}({end})"

    prenode = set()
    node = set()
    edge = set()
    last = -1

    for i in mark:
        if redirect[DFAstate2id[i]] in prenode:
            continue
        node.add((nodeTemplate.format(
            ac=(",accepting" if i in acceptingState else "") +
            (",initial" if redirect[DFAstate2id[i]] ==
             redirect[DFAstate2id[str(sorted(start))]] else""),
            id=redirect[DFAstate2id[i]],
            text=redirect[DFAstate2id[i]],
            relapos=""if last == -1 else
            "right=of {}".format(last)
        ), redirect[DFAstate2id[i]]))
        last = redirect[DFAstate2id[i]]
        prenode.add(
            redirect[DFAstate2id[i]]
        )
    turn = set()
    for i in DFApathSimple:
        for j in DFApathSimple[i]:
            if redirect[i] != redirect[DFApathSimple[i][j]]:
                turn.add((redirect[DFApathSimple[i][j]], redirect[i]))
    for i in DFApathSimple:
        for j in DFApathSimple[i]:
            edge.add(edgeTemplate.format(
                begin=redirect[i],
                char=j,
                end=redirect[DFApathSimple[i][j]],
                edgeset="[loop below]" if redirect[i] == redirect[DFApathSimple[i][j]] else
                "[bend left=10]"if(
                    redirect[i], redirect[DFApathSimple[i][j]])in turn else ""
            ))

    print("\n".join([i[0] for i in sorted(node, key=lambda x: x[1])]))
    print("\path[->]")
    print("\n".join(edge))
