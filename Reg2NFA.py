from copy import deepcopy

operators = {'|', '*', '+', '?', '(', ')'}

class NFA(object):
    nodeCount = 0

    def newNode(selfd):
        NFA.nodeCount += 1
        return NFA.nodeCount

    def __init__(self, c: str = None):
        self.NFApath = []
        if c == None:
            self.front = self.newNode()
            self.back = self.front
        else:
            self.front = self.newNode()
            self.back = self.newNode()
            self.NFApath.append((self.front, self.back, c))

    def concat(self, right):
        self.NFApath.extend(right.NFApath)
        self.NFApath.append((self.back, right.front, 'e'))
        self.back = right.back

    def star(self):
        newFront = self.newNode()
        newBack = self.newNode()
        self.NFApath.append((self.back, self.front, 'e'))
        self.NFApath.append((newFront, self.front, 'e'))
        self.NFApath.append((self.back, newBack, 'e'))
        self.NFApath.append((newFront, newBack, 'e'))
        self.front, self.back = newFront, newBack

    def oR(self, right):
        self.NFApath.extend(right.NFApath)
        newFront = self.newNode()
        newBack = self.newNode()
        self.NFApath.append((newFront, self.front, 'e'))
        self.NFApath.append((self.back, newBack, 'e'))
        self.NFApath.append((newFront, right.front, 'e'))
        self.NFApath.append((right.back, newBack, 'e'))
        self.front, self.back = newFront, newBack

    def __str__(self):
        s = " ".join([str(i+1) for i in range(NFA.nodeCount)])
        t = str(self.front)+" "+str(self.back)
        # for i in sorted(a.NFApath):
        #     print("{} {} {}".format(*i))
        u = ["{} {} {}".format(*i) for i in sorted(self.NFApath)]
        return "\n".join([s, t, "\n".join(u)])


def cacl(s):
    print("line", s)
    operand1 = NFA()
    operand2 = NFA()
    i = 0
    while i < len(s):
        # print(s[i])
        if s[i] not in operators:
            operand1.concat(operand2)
            operand2 = NFA(s[i])
            i += 1
        else:
            if s[i] == '(':
                p = i
                level = 0
                while True:
                    if s[p] == '(':
                        level += 1
                    elif s[p] == ')':
                        level -= 1
                    if level == 0:
                        break
                    p += 1
                operand1.concat(operand2)
                operand2 = cacl(s[i+1:p])
                i = p+1
            elif s[i] == '+':
                tmp = deepcopy(operand2)
                operand2.star()
                operand2.concat(tmp)
                i += 1
            elif s[i] == '*':
                operand2.star()
                i += 1
            elif s[i] == '?':
                operand2.oR(NFA())
                i += 1
            elif s[i] == '|':
                operand1.concat(operand2)
                p = s.find('|', i+1)
                q = s.find('(', i+1)
                r = s.find(')', i+1)
                o = s.find('#', i+1)
                p = min([
                    (lambda x: 10**10)(i) if i == -1 else i
                    for i in [p, q, r, o]
                ])
                operand2 = cacl(s[i+1:p])
                for i in operand1.NFApath:
                    print(i)
                print("before or")
                operand1.oR(operand2)
                for i in operand1.NFApath:
                    print(i)
                print("after or")
                operand2 = NFA()
                i = p
    operand1.concat(operand2)
    return operand1


# print(cacl(s))
