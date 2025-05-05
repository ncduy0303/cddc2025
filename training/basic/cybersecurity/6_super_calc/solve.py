from pwn import remote, context

context.log_level = 'debug'  # Enable DEBUG mode

def solve_expr(expr):
    # Remove spaces and '='
    expr = expr.replace('=', '').strip()
    # Evaluate the arithmetic expression safely
    try:
        return str(eval(expr))
    except Exception:
        raise

r = remote('52.76.13.43', 8084)
line = r.recvline().decode().strip()
# print(line) # 'What is'

while True:
    try:
        expr = r.recvuntil(b'=').decode().strip()
        # print(expr, end=' ') # 'i.e 1 + 6 = '
        answer = solve_expr(expr)
        # print(answer)
        r.sendline(answer.encode())
    except Exception:
        # Flag found
        # print(r.recvall().decode())
        break