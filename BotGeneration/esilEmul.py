import r2pipe

'''
  emulate Bot using ESIL
'''
def emulBot(r2p):

  damage = 0
  executed = 0

  code_map = r2p.cmdj("pxj 1024 @ 0")

  while True:

    # execution outside of allowed area
    regs = r2p.cmdj("drj")
    if regs["eip"] >= 1024:
      return executed, damage

    # Invalid Instruction check
    curi = r2p.cmdj("pdj 1 @ eip")[0]
    if curi['type'] == 'invalid':
      return executed, damage

    # check for outside write only push can write outside for the moment
    if 'push' in curi['type'] and (regs["esp"] > 1024 or regs['esp'] < 4):
      return executed, damage

    # emulate single instruction
    r2p.cmd("ds")
    executed += 1
    code_map_new = r2p.cmdj("pxj 1024 @ 0")

    # write damage by comparing code maps
    for c1, c2 in zip(code_map, code_map_new):
      if c1 != c2:
        damage += 1

    # set hard limit to avoid loops
    if executed >= 500:
      return executed, damage

    code_map = code_map_new.copy()


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
def emulate(codeasm):
  # map 0x400
  # eip 0x200, start in the middle

  # init r2pipe
  r2p = r2pipe.open("malloc://1024")
  r2p.cmd("e asm.arch=x86")
  r2p.cmd("e asm.bits=32")
  r2p.cmd("aei")
  r2p.cmd("aeim")
  r2p.cmd("wx {}@0x200".format(hex(codeasm)[2:]))
  r2p.cmd("aer PC=0x200")

  # emulate by single stepping
  executed, write_damage = emulBot(r2p)

  return executed, write_damage  # fitness, damage and execution time
