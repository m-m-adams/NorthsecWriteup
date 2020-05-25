

def generate_keys(init):
    mask = 0x0101010101010101
    init = init |mask
    value = init
    while value < init+n//8:
        value = (value | mask) +1
        yield value

n = 1<<25
i=0

a = generate_keys(0)
for key in a:
    print(hex(key))



