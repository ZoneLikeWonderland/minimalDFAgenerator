import Reg2NFA
import NFA2DFA

s = """1*0?(1*0)?1*"""
s = """0?0?111+ | 0?1+0?11+ | 0?11+0?1+ 
            | 0?111+0? | 
            1+0?0?11+ | 
            1+0?1+0?1+
            |
            1+0?11+0? | 11+0?0?1+ | 11+0?1+0? | 111+0?0?  
                """.replace(" ", "").replace("\n", "")

# print(s)
nfa = Reg2NFA.cacl(s)
# print(nfa)
NFA2DFA.run(str(nfa))
