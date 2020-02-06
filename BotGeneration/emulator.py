
'''
  emulate single instruction
'''
def emulInstruction(ci, register_file, code_map):
  # opcodes = [("mov",2), ("add",2), ("sub",2), (INST_JMP,1), ("push",1), ("pushad",1), ("inc", 1), ("dec",1)]

  if ci.opcode == "mov":
    register_file[ci.paramname] = ci.paramimm
  if ci.opcode == "add":
    register_file[ci.paramname] += ci.paramimm
  if ci.opcode == "sub":
    register_file[ci.paramname] -= ci.paramimm
  if ci.opcode == "inc":
    register_file[ci.paramname] += 1
  if ci.opcode == "dec":
    register_file[ci.paramname] -= 1

  if ci.opcode == INST_JMP:
    print("TODO: JMP")
    pass

  if ci.opcode == "push":

    if type(ci.paramname) == int:
      value = ci.paramname
    else:
      value = register_file[ci.paramname]

    # assumption 4byte values -> x86-64
    esp = register_file["esp"]
    code_map[esp-1] == (ci.paramimm>>24) & 0xFF
    code_map[esp-2] == (ci.paramimm>>16) & 0xFF
    code_map[esp-3] == (ci.paramimm>>8) & 0xFF
    code_map[esp-4] == (ci.paramimm) & 0xFF
    esp -= 4

  if ci.opcode == "pushad":
    pass


  # todo: how many bytes were written to the memory?
  # == damage


'''
  print map
'''
def printMap(code_map):
  for i in range(32):
    print("{:04x} | ".format(i*32), end='')
    for j in range(32):
      print("{:02x} ".format(code_map[32*i+j]), end = '')
    print("")

 
'''
  emulate code and track execution
'''
def emulate(bot, codeasm):
  # map 0x400
  # eip 0x200, start in the middle
  # esp, give private stack region

  code_map = [0]*1024

  register_file = {
    "eax": 0, "ebx": 0, "ecx": 0, "edx": 0, "edi": 0,
    "esi": 0, "ebp": 0, "esp": 0x17080, "eip": 0x200 
  }
  eip = register_file["eip"]

  # copy code into file
  codelen = len(hex(codeasm)[2:])
  for i in range(int(codelen/2+0.5)):
    code_map[eip+i] = (codeasm>>(len(hex(codeasm)[2:])*4-(i*2+2)*4))&0xFF
    #print("write: {} <- {} {}".format(hex(eip+i), hex((codeasm>>(len(hex(codeasm)[2:])*4-(i*2+2)*4))&0xFF), code_map[eip+i]))

  printMap(code_map)
  # print(code_map[eip:eip+0x10])

  
  code = bot.getInstForEmulation()

  while True:
    ci = code[eip]

    # ignore labels
    if ci.opcode.startswith("label"):
      continue

    emulInstruction(ci, register_file, code_map)


  fitness = executed + write_damage
  return fitness
  '''