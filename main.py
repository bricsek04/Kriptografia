from elliptikus_gorbe_v2 import *
from blokklanc import *
import json

def main():
    print("Elliptikus görbe titkosítás:")
    q = 17
    a = 2
    b = 2
    G = (5,1)

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

    C1, C2 = titkositas(üzenet, publikus_kulcs, G, a, q, n=19)

    print(f"titkos_üzenet_C1: {C1}")
    print(f"titkos_üzenet_C2: {C2}")

    visszafejtett_üzenet = visszafejtes(C1, C2, privat_kulcs, a, q)
    
    print(f"visszafejtett_üzenet: {visszafejtett_üzenet}")

    print("---------------------")

    print("Blokklánc: ")
    print("\n================ BLOKKLÁNC INDÍTÁSA ================\n")

    lanc = []
    nehezseg = 4

    # --- 1. LÉPÉS: Genesis blokk ---
    print("=== 1. LÉPÉS: Genesis blokk létrehozása és bányászata ===")
    elso_blokk = uj_blokk(0, ["Genesis Blokk"], "0")
    print("Bányászat folyamatban...")
    talalt_hash_0 = banyaszat(elso_blokk, nehezseg)
    lanc.append(elso_blokk)

    print(f"-> Genesis blokk sikeresen kibányászva!")
    print(f"-> Talált Hash: {talalt_hash_0}")
    print(f"-> Szükséges próbálkozások (nonce): {elso_blokk['nonce']}\n")


    # --- 2. LÉPÉS: Első tranzakció ---
    print("=== 2. LÉPÉS: 1-es indexű blokk (Alice -> Bob) ===")
    tranzakcio_1 = [
        {"kuldo": "Alice", "fogado": "Bob", "osszeg": 10}
    ]
    elozo_blokk_hash = blokk_hash(lanc[-1])
    print(f"Hivatkozás a Genesis hash-re: {elozo_blokk_hash}")

    uj_blokk_1 = uj_blokk(1, tranzakcio_1, elozo_blokk_hash)
    print("Bányászat folyamatban...")
    talalt_hash_1 = banyaszat(uj_blokk_1, nehezseg)
    lanc.append(uj_blokk_1)

    print(f"-> 1-es blokk kibányászva!")
    print(f"-> Új Hash: {talalt_hash_1}\n")


    # --- 3. LÉPÉS: Második tranzakció ---
    print("=== 3. LÉPÉS: 2-es indexű blokk (Bob -> Csaba) ===")
    tranzakcio_2 = [
        {"kuldo": "Bob", "fogado": "Csaba", "osszeg": 5}
    ]
    elozo_blokk_hash = blokk_hash(lanc[-1])
    print(f"Hivatkozás az 1-es blokk hash-ére: {elozo_blokk_hash}")

    uj_blokk_2 = uj_blokk(2, tranzakcio_2, elozo_blokk_hash)
    print("Bányászat folyamatban...")
    talalt_hash_2 = banyaszat(uj_blokk_2, nehezseg)
    lanc.append(uj_blokk_2)

    print(f"-> 2-es blokk kibányászva!")
    print(f"-> Új Hash: {talalt_hash_2}\n")


    # --- LÁTVÁNYOS KIÍRATÁS ---
    print("=== A TELJES, ÉRVÉNYES BLOKKLÁNC TARTALMA ===")
    # A json.dumps(..., indent=4) gyönyörűen, behúzásokkal írja ki a listát/szótárakat
    print(json.dumps(lanc, indent=4))
    print("---------------------------------------------------")


    # --- 4. LÉPÉS: Ellenőrzés ---
    print("\n=== 4. LÉPÉS: Biztonsági ellenőrzés ===")
    print(f"A blokklánc kriptográfiailag sértetlen és érvényes? -> {ellenorzes(lanc, nehezseg)}\n")


    # --- 5. LÉPÉS: Támadás / Manipuláció ---
    print("=== 5. LÉPÉS: Rosszindulatú támadás ===")
    print("Támadó akció: Alice utólag átírja az 1-es blokkban lévő 10-es összeget 5000-re...")
    lanc[1]["tranzakciok"][0]["osszeg"] = 5000

    print(f"A manipulált tranzakció tartalma: {lanc[1]['tranzakciok']}")
    print("A blokk tartalma megváltozott, de a hash nem frissült, illetve a következő blokk a régi hash-t keresi.")

    print("\nLánc ellenőrzése a támadás után:")
    print(f"A blokklánc érvényes maradt? -> {ellenorzes(lanc, nehezseg)}")


if __name__ == "__main__":
    main()