section .text
    global _start           

_start:
    mov rax, 0x02000001     
    mov rdi, 0x1           
    syscall
