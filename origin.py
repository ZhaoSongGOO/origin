import sys
import subprocess

count = 0


def iota():
    global count
    count = count + 1
    return count


def reset():
    global count
    count = 0


I_PUSH = iota()
I_POP = iota()
I_ADD = iota()
I_MINUS = iota()
I_MULTI = iota()
I_DUP = iota()
OP_COUNT = iota()
reset()


def PUSH(a):
    return (I_PUSH, a)


def POP():
    return (I_POP, None)


def ADD():
    return (I_ADD, None)


def MINUS():
    return (I_MINUS, None)


def MULTI():
    return (I_MULTI, None)


def DUP():
    return (I_DUP, None)


def get_op_from_str(str):
    if str == "+":
        return ADD()
    elif str == "-":
        return MINUS()
    elif str == "dup":
        return DUP()
    elif str == ".":
        return POP()
    elif str == "*":
        return MULTI()
    else:
        return PUSH(int(str))


def read_tokens_from_line(line, row):
    tokens = []
    i = 0
    length = len(line)
    while i < length:
        if line[i].isspace():
            i = i + 1
            continue
        col = i + 1
        str = ""
        while not line[i].isspace():
            str = str + line[i]
            i = i + 1
        tokens.append([row, col, get_op_from_str(str)])
    return tokens


def lexer(source_file):
    # (row, col, str)
    tokens = []
    row = 1
    with open(source_file, "r") as f:
        line = f.readline()
        while line:
            line_tokens = read_tokens_from_line(line, row)
            row = row + 1
            line = f.readline()
            tokens.extend(line_tokens)
    return tokens


def compile_darwin(asm, tokens):
    asm.write("section .text\n")
    asm.write("    global _start\n")
    asm.write("dump:\n")
    asm.write("    push    rbp\n")
    asm.write("    mov     rbp, rsp\n")
    asm.write("    sub     rsp, 64\n")
    asm.write("    mov     QWORD [rbp-56], rdi\n")
    asm.write("    mov     QWORD [rbp-8], 1\n")
    asm.write("    mov     eax, 32\n")
    asm.write("    sub     rax, QWORD [rbp-8]\n")
    asm.write("    mov     BYTE [rbp-48+rax], 10\n")
    asm.write(".L2:\n")
    asm.write("    mov     rcx, QWORD [rbp-56]\n")
    asm.write("    movabs  rdx, -3689348814741910323\n")
    asm.write("    mov     rax, rcx\n")
    asm.write("    mul     rdx\n")
    asm.write("    shr     rdx, 3\n")
    asm.write("    mov     rax, rdx\n")
    asm.write("    sal     rax, 2\n")
    asm.write("    add     rax, rdx\n")
    asm.write("    add     rax, rax\n")
    asm.write("    sub     rcx, rax\n")
    asm.write("    mov     rdx, rcx\n")
    asm.write("    mov     eax, edx\n")
    asm.write("    lea     edx, [rax+48]\n")
    asm.write("    mov     eax, 31\n")
    asm.write("    sub     rax, QWORD [rbp-8]\n")
    asm.write("    mov     BYTE [rbp-48+rax], dl\n")
    asm.write("    add     QWORD [rbp-8], 1\n")
    asm.write("    mov     rax, QWORD [rbp-56]\n")
    asm.write("    movabs  rdx, -3689348814741910323\n")
    asm.write("    mul     rdx\n")
    asm.write("    mov     rax, rdx\n")
    asm.write("    shr     rax, 3\n")
    asm.write("    mov     QWORD [rbp-56], rax\n")
    asm.write("    cmp     QWORD [rbp-56], 0\n")
    asm.write("    jne     .L2\n")
    asm.write("    mov     eax, 32\n")
    asm.write("    sub     rax, QWORD [rbp-8]\n")
    asm.write("    lea     rdx, [rbp-48]\n")
    asm.write("    lea     rcx, [rdx+rax]\n")
    asm.write("    mov     rax, QWORD [rbp-8]\n")
    asm.write("    mov     rdx, rax\n")
    asm.write("    mov     rsi, rcx\n")
    asm.write("    mov     edi, 1\n")
    asm.write("    mov rax, 0x02000004\n")
    asm.write("    syscall\n")
    asm.write("    nop\n")
    asm.write("    leave\n")
    asm.write("    ret\n")
    asm.write("_start:\n")
    for token in tokens:
        op, v = token[2]
        if op == I_PUSH:
            asm.write(f"    push {v}\n")
        elif op == I_POP:
            asm.write(f"    pop rax\n")
        elif op == I_ADD:
            asm.write(f"    pop rax\n")
            asm.write(f"    pop rbx\n")
            asm.write(f"    add rax, rbx\n")
            asm.write(f"    push rax\n")
        elif op == I_MINUS:
            asm.write(f"    pop rax\n")
            asm.write(f"    pop rbx\n")
            asm.write(f"    sub rax, rbx\n")
            asm.write(f"    push rax\n")
        elif op == I_DUP:
            asm.write(f"    mov rdi, [rsp]\n")
            asm.write(f"    call dump\n")
    asm.write("    mov rdi, 0\n")
    asm.write("    mov rax, 0x02000001\n")
    asm.write("    syscall\n")
    asm.close()
    subprocess.check_call(["./build_macos.sh"], shell=True)


def compile(tokens):
    with open("origin.s", "w") as f:
        if sys.platform == "darwin":
            compile_darwin(f, tokens)
        else:
            raise NotImplementedError


if __name__ == "__main__":
    tokens = lexer(sys.argv[1])
    compile(tokens)
