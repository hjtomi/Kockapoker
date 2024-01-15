import random
from typing import List, Tuple
import os
import time
from pandas import DataFrame
from colorama import Fore, Back, Style
import json
import logging

# Szines printeles
# Jatek vegen mentes torlese?
# valasztasi lehetosegek tablazatban is mutatasa
# nehez foknak ha nincs lehetoseg akkor alulrol haladjon

DOBAS_LEHETOSEGEK = [1, 2, 3, 4, 5, 6]
GEP_DOBAS_ALVAS = 3
GEP_VALASZTAS_ALVAS = 3
JATEKOS_VALASZTAS_ALVAS = 1


def jatek():
    def tabla_tele() -> bool:
        """Megnezi, hogy tele van-e a tabla."""

        for (gep_ertek, jatekos_ertek) in zip(tabla['gep'].values(), tabla['jatekos'].values()):
            if gep_ertek == None or jatekos_ertek == None:
                return False

        return True

    def mentes_van() -> bool:
        """Megnezi, hogy van-e mentes file."""

        return os.path.isfile('mentes.json')

    def mentes():
        adatok = {
            'statusz': statusz,
            'tabla': tabla,
            'szamlista': szamlista,
            'nev': nev,
            'nehezseg': nehezseg,
            'animacio': animacio,
        }

        with open('mentes.json', 'w') as file:
            json.dump(adatok, file)

    def mentes_betoltes() -> Tuple[str, dict, List[int], str, str, str]:
        """Betolti a mentest."""

        with open('mentes.json') as file:
            mentes = json.load(file)

        statusz = mentes['statusz']
        tabla = mentes['tabla']
        szamlista = mentes['szamlista']
        nev = mentes['nev']
        nehezseg = mentes['nehezseg']
        animacio = mentes['animacio']

        return statusz, tabla, szamlista, nev, nehezseg, animacio

    def valasztas(szoveg: str, opciok: list):
        """Egyszerusites az olyan inputok beirasara ami bizonyos valaszokat fogad el."""

        valasz = None
        while valasz not in opciok:
            valasz = input(szoveg)

        return valasz

    def adatbekeres() -> Tuple[str, str, str]:
        """Bekeri az adatokat."""

        nev = input('Felhasznalonev: ')
        nehezseg = valasztas('Konnyu vagy nehez jatek (k/n): ', opciok=['k', 'n'])
        animacio = valasztas('Szeretnel dobas animaciot? (i/n): ', opciok=['i', 'n'])

        return nev, nehezseg, animacio

    def dobas() -> List[int]:
        """Visszaad 5 random szamot."""

        szamlista = random.choices(DOBAS_LEHETOSEGEK, k=5)
        kirajzolas(szamlista)
        return szamlista

    def dobas_animacioval() -> List[int]:
        """Dobas animacio logika."""

        for i in range(30, 1, -1):
            dobas()
            time.sleep(1/i)

        return dobas()

    def hely_valasztas(szamlista):
        def ures_helyek() -> List[str]:
            """Megnezi melyik helyek szabadok az epp soronlevo jatekosnak."""

            uresek = []
            for key, value in tabla[statusz.split(' ')[0]].items():
                if value == None:
                    uresek.append(key)

            return uresek

        def szabalyos_helyek(kalkulaciok) -> List[str]:
            """Megnezi, hogy az ures helyek kozul melyikbe irhato a szamlista.
            Ha egyikbe sem, akkor az osszeset visszaadja."""

            szabalyosak = []
            for key, value in kalkulaciok.items():
                if value > 0:
                    szabalyosak.append(key)

            return szabalyosak

        def ures_szabalyos_helyek(uresek, szabalyosak) -> List[str]:
            """Kiszamitja, hogy az ures es a szabalyos helyeknel mi az atfedes.
            Ha nincs akkor az osszes ureset visszaadja."""

            ures_szabalyosak = []
            for szabalyos in szabalyosak:
                if szabalyos in uresek:
                    ures_szabalyosak.append(szabalyos)

            if ures_szabalyosak:
                return ures_szabalyosak

            return uresek

        def jatekos_valasztas():
            dontes = valasztas(f'Melyik helyre szeretned beirni? {ures_szabalyos_kalkulacioi}\n', ures_szabalyosak)
            tabla['jatekos'][dontes] = ures_szabalyos_kalkulacioi[dontes]

        def konnyu_gep_valaszt():
            tabla['gep'][tuple(ures_szabalyos_kalkulacioi.keys())[0]] = tuple(ures_szabalyos_kalkulacioi.values())[0]

        def nehez_gep_valaszt():
            legtobb_pont = max(ures_szabalyos_kalkulacioi.values())
            for key, value in ures_szabalyos_kalkulacioi.items():
                if value == legtobb_pont:
                    tabla['gep'][key] = value
                    break

        kalkulaciok = kalkulacio(szamlista)

        uresek = ures_helyek()
        szabalyosak = szabalyos_helyek(kalkulaciok)

        ures_szabalyosak = ures_szabalyos_helyek(uresek, szabalyosak)
        ures_szabalyos_kalkulacioi = {ures_szabalyos: kalkulaciok[ures_szabalyos] for ures_szabalyos in ures_szabalyosak}
        logging.info(ures_szabalyos_kalkulacioi)

        if statusz.split(' ')[0] == 'jatekos':
            jatekos_valasztas()

        elif nehezseg == 'k':
            konnyu_gep_valaszt()

        elif nehezseg == 'n':
            nehez_gep_valaszt()

        kirajzolas()

    def kalkulacio(szamlista: List[int]) -> dict:
        """Kiszamitja az osszes mezore, hogy mennyi pontot erne."""

        szamlista = sorted(szamlista, reverse=True)

        def tetszoleges():
            return sum(szamlista)

        def par():
            for i, szam in enumerate(szamlista):
                try:
                    if szam == szamlista[i + 1]:
                        return szam * 2

                except IndexError:
                    return 0

        def drill():
            for i, szam in enumerate(szamlista):
                try:
                    if szam == szamlista[i + 1] == szamlista[i + 2]:
                        return szam * 3

                except IndexError:
                    return 0

        def ket_par():
            talalat = False
            szamok = []
            for i, szam in enumerate(szamlista):
                if len(szamok) == 2:
                    if szamok[0] == szamok[1]:
                        return 0

                    return szamok[0] * 2 + szamok[1] * 2

                if talalat:
                    talalat = False
                    continue

                try:
                    if szam == szamlista[i + 1]:
                        szamok.append(szam)
                        talalat = True

                except IndexError:
                    return 0

            return 0

        def kis_poker():
            for i, szam in enumerate(szamlista):
                try:
                    if szam == szamlista[i + 1] == szamlista[i + 2] == szamlista[i + 3]:
                        return szam * 4

                except IndexError:
                    return 0

        def full():
            if (szamlista[0] == szamlista[1] == szamlista[2] and szamlista[3] == szamlista[4]) or (
                    szamlista[0] == szamlista[1] and szamlista[2] == szamlista[3] == szamlista[4]):
                return sum(szamlista)

            return 0

        def kis_sor():
            if szamlista == [5, 4, 3, 2, 1]:
                return 15

            return 0

        def nagy_sor():
            if szamlista == [6, 5, 4, 3, 2]:
                return 20

            return 0

        def nagy_poker():
            if len(set(szamlista)) == 1:
                return 50

            return 0

        kalkulacio = {
            'tetszoleges': tetszoleges(),
            'par': par(),
            'drill': drill(),
            'ket par': ket_par(),
            'kis poker': kis_poker(),
            'full': full(),
            'kis sor': kis_sor(),
            'nagy sor': nagy_sor(),
            'nagy poker': nagy_poker()
        }

        return kalkulacio

    def kirajzolas(animacios_szamlista=None):
        """Kirajzolja a jatekot."""

        os.system('cls')

        tablastring = DataFrame(tabla).to_string().replace('None', '').replace('NaN', '').replace('.0', '')
        if animacios_szamlista:
            str_szamlista = ' '.join(map(str, animacios_szamlista))
        else:
            str_szamlista = ' '.join(map(str, szamlista))

        print(tablastring + '\n')
        print(statusz)
        print(str_szamlista)

    def eredmeny_file_van():
        return os.path.isfile('eredmenyek.txt')

    def eredmenykalkulacio():
        gep_pontja = sum(tabla['gep'].values())
        jatekos_pontja = sum(tabla['jatekos'].values())

        gyoztes = ''
        gyoztes_nev = ''
        gyoztes_pontja = 0
        vesztes_pontja = 0
        if jatekos_pontja > gep_pontja:
            gyoztes = 'jatekos'
            gyoztes_nev = nev
            gyoztes_pontja = jatekos_pontja
            vesztes_pontja = gep_pontja

        elif gep_pontja > jatekos_pontja:
            gyoztes = 'szamitogep'
            gyoztes_nev = 'szamitogep'
            gyoztes_pontja = gep_pontja
            vesztes_pontja = jatekos_pontja

        uj_sor = f'{gyoztes_nev} {gyoztes_pontja}\n'

        with open('eredmenyek.txt', 'r+') as file:
            eddigi_sorok = file.readlines()

        fileba_kerult = False
        if gyoztes_pontja == 0:
            kirajzolas()

            print(f'Az eredmeny dontetlen {jatekos_pontja}-ponttal.\n')
            print(eddigi_sorok)

        elif not eddigi_sorok:
            with open('eredmenyek.txt', 'w') as file:
                file.write(uj_sor)
            fileba_kerult = True

        else:
            nagyobb_eredmeny = False
            for i, pont in enumerate(map(lambda x: int(x.split(' ')[1]), eddigi_sorok)):
                if gyoztes_pontja > pont:
                    eddigi_sorok.insert(i, uj_sor)
                    nagyobb_eredmeny = True
                    fileba_kerult = True

                    break

            if nagyobb_eredmeny:
                with open('eredmenyek.txt', 'w') as file:
                    file.writelines(eddigi_sorok[:10])

            elif not nagyobb_eredmeny and len(eddigi_sorok) < 10:
                eddigi_sorok.append(uj_sor)
                with open('eredmenyek.txt', 'w') as file:
                    file.writelines(eddigi_sorok)
                fileba_kerult = True

        return gyoztes, gyoztes_pontja, vesztes_pontja, fileba_kerult

    def eredmenyhirdetes(gyoztes, gyoztes_pontja, vesztes_pontja, fileba_kerult):
        kirajzolas()
        print('\n')

        if gyoztes == 'jatekos':
            print('Te nyertel!')
            print(f'Az eredmeny {vesztes_pontja} - {gyoztes_pontja}')

        elif gyoztes == 'gep':
            print('Vesztettel!')
            print(f'Az eredmeny {gyoztes_pontja} - {vesztes_pontja}')

        if fileba_kerult:
            print('Bekerult a legjobb 10 koze\n')
        else:
            print('Nem kerult a legjobb 10 koze\n')

        with open('eredmenyek.txt') as file:
            print(file.read())

    statusz = 'gep dob'
    tabla = {
        'gep': {
            'tetszoleges': None,
            'par': None,
            'drill': None,
            'ket par': None,
            'kis poker': None,
            'full': None,
            'kis sor': None,
            'nagy sor': None,
            'nagy poker': None
        },
        'jatekos': {
            'tetszoleges': None,
            'par': None,
            'drill': None,
            'ket par': None,
            'kis poker': None,
            'full': None,
            'kis sor': None,
            'nagy sor': None,
            'nagy poker': None
        },
    }
    # tabla = {
    #     'gep': {
    #         'tetszoleges': 1,
    #         'par': 1,
    #         'drill': 1,
    #         'ket par': 1,
    #         'kis poker': 1,
    #         'full': 1,
    #         'kis sor': 1,
    #         'nagy sor': 1,
    #         'nagy poker': 1
    #     },
    #     'jatekos': {
    #         'tetszoleges': 1,
    #         'par': 1,
    #         'drill': 1,
    #         'ket par': 1,
    #         'kis poker': 1,
    #         'full': 1,
    #         'kis sor': 1,
    #         'nagy sor': 1,
    #         'nagy poker': 40
    #     },
    # }
    szamlista = []
    nev = ''
    nehezseg = ''
    animacio = ''

    mentest_betoltott = False

    if not eredmeny_file_van():
        with open('eredmenyek.txt', 'w') as file:
            pass

    if mentes_van():
        if valasztas(szoveg='Mentes betoltese? (i/n) ', opciok=['i', 'n']) == 'i':
            statusz, tabla, szamlista, nev, nehezseg, animacio = mentes_betoltes()
            mentest_betoltott = True

    if not mentest_betoltott:
        nev, nehezseg, animacio = adatbekeres()

    while not tabla_tele():
        if statusz == 'gep dob':
            szamlista = dobas() if animacio == 'n' else dobas_animacioval()
            time.sleep(GEP_DOBAS_ALVAS)
            statusz = 'gep valaszt'
            mentes()

        if statusz == 'gep valaszt':
            hely_valasztas(szamlista)
            time.sleep(GEP_VALASZTAS_ALVAS)
            statusz = 'jatekos dob'
            mentes()

        if statusz == 'jatekos dob':
            szamlista = dobas() if animacio == 'n' else dobas_animacioval()
            statusz = 'jatekos valaszt'
            mentes()

        if statusz == 'jatekos valaszt':
            hely_valasztas(szamlista)
            time.sleep(JATEKOS_VALASZTAS_ALVAS)
            statusz = 'gep dob'
            mentes()

    gyoztes, gyoztes_pontja, vesztes_pontja, fileba_kerult = eredmenykalkulacio()
    eredmenyhirdetes(gyoztes, gyoztes_pontja, vesztes_pontja, fileba_kerult)


jatek()
