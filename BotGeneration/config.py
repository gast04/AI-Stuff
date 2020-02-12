
# define registers and possible opcodes
registers = ["eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp"]
opcodes = [("mov",2), ("add",2), ("sub",2), ("jmp",1), 
           ("push",1), ("pushad",1), ("inc", 1), ("dec",1), 
           ("cmp", 2), ("je", 1), ("jne", 1)]


damage_mult = 1     # weight damage more than execution
