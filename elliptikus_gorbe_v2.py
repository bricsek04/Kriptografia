import random

def rajta_van_e(P, a, b, q):
    if P is None: return True
    x, y = P
    bal = (y ** 2) % q
    jobb = (x ** 3 + a*x + b) % q
    return bal == jobb

def additiv_inverz(P, q):
    if P is None: return None
    x, y = P
    return (x, -y % q)

def pontosszeadas(P, Q, a, q):
    if P is None: return Q
    if Q is None: return P

    x_p, y_p = P
    x_q, y_q = Q

    if x_p == x_q and y_p == (-y_q) % q: return None
    if P == Q: return pontduplazas(P, a, q)

    lam = ((y_q - y_p)*pow(x_q - x_p, -1, q)) % q
    x_r = (lam ** 2 - x_p - x_q) % q
    y_r = (lam * (x_p - x_r) - y_p) % q

    return (x_r, y_r)

def pontduplazas(P, a, q):
    if P is None: return None
    
    x_p, y_p = P

    if y_p == 0: return None

    lam = ((3 * x_p ** 2 + a) * pow(2 * y_p, -1, q)) % q
    x_r = (lam ** 2 - 2 * x_p) % q
    y_r = (lam * (x_p - x_r) - y_p) % q

    return (x_r, y_r)

def skalarral_szorzas(k, P, a, q):
    R = None
    addend = P

    while k > 0:
        if k % 2 == 1:
            R = pontosszeadas(R, addend, a, q)
        addend = pontduplazas(addend, a, q)
        k //= 2

    return R

def titkositas(üzenet, publikus_kulcs, G, a, q, n):
    r = random.randint(1, n-1)

    C1 = skalarral_szorzas(r, G, a ,q)

    kozos_titok = skalarral_szorzas(r, publikus_kulcs, a, q)

    C2 = pontosszeadas(üzenet, kozos_titok, a, q)

    return C1, C2

def visszafejtes(C1, C2, privat_kulcs, a, q):
    kozos_titok = skalarral_szorzas(privat_kulcs, C1, a, q)

    kozos_titok_inverz = additiv_inverz(kozos_titok, q)

    üzenet = pontosszeadas(C2, kozos_titok_inverz, a, q)
    
    return üzenet