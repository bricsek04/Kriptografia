from elliptikus_gorbe_v2 import *
from blokklanc import *
import json

def main():
    print("Elliptikus görbe titkosítás:")
    q = 17
    a = 2
    b = 2
    G = (5,1)
    n = 19

    if not rajta_van_e(G, a, b, q):
        print("A generátorpont nincs rajta a görbén.")
        return

    privat_kulcs = 13
    publikus_kulcs = skalarral_szorzas(privat_kulcs, G, a, q)

    üzenet = (10, 6)

    if not rajta_van_e(üzenet, a, b, q):
        print("Az üzenetpont nincs rajta a görbén.")
        return

    print(f"eredeti_üzenet: {üzenet}")
    print(f"publikus_kulcs: {publikus_kulcs}")

    C1, C2 = titkositas(üzenet, publikus_kulcs, G, a, q, n)

    print(f"titkos_üzenet_C1: {C1}")
    print(f"titkos_üzenet_C2: {C2}")

    visszafejtett_üzenet = visszafejtes(C1, C2, privat_kulcs, a, q)
    print(f"visszafejtett_üzenet: {visszafejtett_üzenet}")

    print("\n---------------------")
    print("Blokklánc:")

    lanc = []
    nehezseg = 4

    alice_priv = 13
    alice_pub = skalarral_szorzas(alice_priv, G, a, q)

    bob_priv = 7
    bob_pub = skalarral_szorzas(bob_priv, G, a, q)

    elso_blokk = uj_blokk(0, ["Genesis Blokk"], "0")
    banyaszat(elso_blokk, nehezseg)
    lanc.append(elso_blokk)

    tx1 = tranzakcio_kuldese("Alice", "Bob", 10, alice_priv, alice_pub, G, a, q, n)
    print(f"1. tranzakció aláírása érvényes: {tranzakcio_ellenorzese(tx1, G, a, q, n)}")
    blokk_1 = uj_blokk(1, [tx1], blokk_hash(lanc[-1]))
    banyaszat(blokk_1, nehezseg)
    lanc.append(blokk_1)

    tx2 = tranzakcio_kuldese("Bob", "Csaba", 5, bob_priv, bob_pub, G, a, q, n)
    print(f"2. tranzakció aláírása érvényes: {tranzakcio_ellenorzese(tx2, G, a, q, n)}")
    blokk_2 = uj_blokk(2, [tx2], blokk_hash(lanc[-1]))
    banyaszat(blokk_2, nehezseg)
    lanc.append(blokk_2)

    print("\nBlokklánc tartalma:")
    print(json.dumps(lanc, indent=4))

    print(f"\nBlokklánc érvényes: {ellenorzes(lanc, nehezseg, G, a, q, n)}")

    lanc[1]["tranzakciok"][0]["osszeg"] = 5000
    print("\nManipuláció után (összeg átírva 5000-re):")
    print(f"Manipulált tranzakció aláírása érvényes: {tranzakcio_ellenorzese(lanc[1]['tranzakciok'][0], G, a, q, n)}")
    print(f"Blokklánc érvényes: {ellenorzes(lanc, nehezseg, G, a, q, n)}")

if __name__ == "__main__":
    main()