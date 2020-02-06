import random

INST_JMP = "jmp"

# define registers and possible opcodes
registers = ["eax", "ebx", "ecx", "edx", "esi", "edi", "esp", "ebp"]
opcodes = [("mov",2), ("add",2), ("sub",2), (INST_JMP,1), 
           ("push",1), ("pushad",1), ("inc", 1), ("dec",1), 
           ("cmp", 2), ("je", 1), ("jne", 1)]


def createRandomInst(bot):
    opr = random.randint(0, len(opcodes)-1)
    opcode = opcodes[opr]
    reg = registers[random.randint(0, len(registers)-1)]

    # special case for jumps
    if opcode[0][0] == "j":
        if (random.random() < 0.6) and bot.len() >= 1:
            reg = random.randint(0, bot.len()-1)        # jump inside code

    if opcode[1] == 2:
        imm = random.randint(0,2**10)   # 2**10 = 1024
    else:
        imm = None

    # return instruction to bot
    return Instruction(opcode[0], reg, imm)


'''
  Instruction types: opcode register [immediate]
  Sample: 
    mov eax, 0x1234
    mov ebx, 0x4321
    jump eax
    jump 1           # jump to 1st instruction
    push eax
'''
class Instruction:
  def __init__(self, opcode, paramname, paramimm=None):
    self.opcode = opcode
    self.paramname = paramname  
    self.paramimm = paramimm

    if paramimm == None:
      self.paramcount = 1
    else:
      self.paramcount = 2

  def instToText(self):
    output = ""
    
    if self.paramcount == 1:
      if self.opcode[0] == "j" and type(self.paramname) == int:
        output += "{} label{}".format(self.opcode, self.paramname)  
      else:
        output += "{} {}".format(self.opcode, self.paramname)
    else:
      output += "{} {}, {}".format(self.opcode, self.paramname, hex(self.paramimm))
       
    return output

  def printInst(self):
    print(self.instToText())



'''
  stores list of instructions which
  is a Bot
'''
class Bot:
  def __init__(self):
    self.instructions = []
    self.damage = 0
    self.execution = 0

  def len(self):
    return len(self.instructions)

  def addInst(self, inst):
    self.instructions.append(inst)

  def getInsts(self):
    return self.instructions

  def setInsts(self, insts):
    self.instructions = insts

  def botToText(self):
    output = ""

    # scan bot for "jump label"
    labels = []
    for inst in self.instructions:
      if inst.opcode == INST_JMP and type(inst.paramname) == int:
        labels.append(inst.paramname)

    for i,inst in enumerate(self.instructions):
      if i in labels: # append labels
        output += "label{}:\n".format(i)

      output += inst.instToText() + "\n"

    return output

  def printBot(self):
    print(self.botToText())

  def getInstForEmulation(self):
    insts = []

    # scan bot for "jump label"
    labels = []
    for inst in self.instructions:
      if inst.opcode == INST_JMP and type(inst.paramname) == int:
        labels.append(inst.paramname)

    for i,inst in enumerate(self.instructions):
      if i in labels: # append labels
        insts.append(Instruction("label{}:\n".format(i),"eax"))
      insts.append(inst)

    return insts

  def addExDam(self, execution, damage):
    self.damage = damage
    self.execution = execution

  def getExDam(self):
    return (self.execution, self.damage)

  def getScore(self):
    return (self.execution + self.damage*2)
