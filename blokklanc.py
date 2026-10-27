import hashlib
import json
import time
from elliptikus_gorbe_v2 import schnorr_alairas, schnorr_ellenorzes

def blokk_hash(blokk):
    string_blokk = json.dumps(blokk, sort_keys=True).encode()
    return hashlib.sha256(string_blokk).hexdigest()

def uj_blokk(index, tranzakciok, elozo_hash, nonce=0):
    return{
        "index": index,
        "timestamp": time.time(),
        "tranzakciok": tranzakciok,
        "elozo_hash": elozo_hash,
        "nonce": nonce
    }

def banyaszat(blokk, nehezseg):
    cel = "0" * nehezseg
    aktualis_hash = blokk_hash(blokk)
    while aktualis_hash[:nehezseg] != cel:
        blokk["nonce"] += 1
        aktualis_hash = blokk_hash(blokk)
    return aktualis_hash

def tranzakcio_kuldese(kuldo, fogado, osszeg, privat_kulcs, publikus_kulcs, G, a, q, n):
    uzenet = f"{kuldo}->{fogado}:{osszeg}"
    alairas = schnorr_alairas(uzenet, privat_kulcs, G, a, q, n)
    return {
        "kuldo": kuldo,
        "fogado": fogado,
        "osszeg": osszeg,
        "publikus_kulcs": publikus_kulcs,
        "alairas": alairas
    }

def tranzakcio_ellenorzese(tranzakcio, G, a, q, n):
    uzenet = f"{tranzakcio['kuldo']}->{tranzakcio['fogado']}:{tranzakcio['osszeg']}"
    return schnorr_ellenorzes(
        uzenet,
        tranzakcio["alairas"],
        tranzakcio["publikus_kulcs"],
        G, a, q, n
    )

def ellenorzes(lanc, nehezseg, G, a, q, n):
    for i in range(1, len(lanc)):
        aktualis_blokk = lanc[i]
        elozo_blokk = lanc[i-1]

        aktualis_hash = blokk_hash(aktualis_blokk)

        if aktualis_hash[:nehezseg] != "0" * nehezseg:
            return False
        
        if aktualis_blokk["elozo_hash"] != blokk_hash(elozo_blokk):
            return False

        for tx in aktualis_blokk["tranzakciok"]:
            if not tranzakcio_ellenorzese(tx, G, a, q, n):
                return False

    return True