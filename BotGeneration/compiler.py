import subprocess as sp

'''
  compile bot using rasm2
  rasm2 -a x86 -b 32 -f bot.x86-32.asm
'''
def compileBot(bot):

  bot_code = bot.botToText()

  codefile = open("bots/bot.x86-32.asm", "w+")
  codefile.write(bot_code)
  codefile.close()

  compile_cmd = ["rasm2", "-a", "x86", "-b", "32", "-f", "bots/bot.x86-32.asm"]
  proc = sp.Popen(compile_cmd, stdout=sp.PIPE)
  # TODO: check if compilation failed

  # return compiled binary
  return int(proc.stdout.read().strip(),16)

