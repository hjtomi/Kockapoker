import random
from typing import List
import os
import time
from colorama import Fore, Back, Style
import json
from tablastring import TABLASTRING
from unidecode import unidecode

# Szines printeles
# Valasztasi lehetosegek tablazatban is mutatasa - tabla kirajzolas atalakitasa

# Ha van mas lehetoseg a tetszoleges mezot mellozi


class Kockapoker:
    def __init__(self):
        self.DOBAS_LEHETOSEGEK = [1, 2, 3, 4, 5, 6]
        self.GEP_DOBAS_ALVAS = 3
        self.GEP_VALASZTAS_ALVAS = 3
        self.JATEKOS_VALASZTAS_ALVAS = 1
        self.GEP_FORMATOK = 'gt gp gd gkp gkip gf gks gns gnp'.split()
        self.JATEKOS_FORMATOK = 'jt jp jd jkp jkip jf jks jns jnp'.split()
        self.MEZOK = 'tetszoleges,par,drill,ket par,kis poker,full,kis sor,nagy sor,nagy poker'.split(',')

        self.statusz = 'gep dob'
        self.tabla = {
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
        self.szamlista = [0, 0, 0, 0, 0]
        self.nev = 'debug_ertek'
        self.nehezseg = 'n'
        self.animacio = 'i'

        self.most_beirt = ''
        self.lehetosegek_ertekei = ''

        self.mentest_betoltott = False

        if not self.eredmeny_file_van():
            with open('eredmenyek.txt', 'w') as _:
                pass

        if self.mentes_van():
            if self.valasztas(szoveg='Mentes betoltese? (i/n) ', opciok=['i', 'n']) == 'i':
                self.mentes_betoltes()
                self.mentest_betoltott = True

        if not self.mentest_betoltott:
            self.adatbekeres()

        while not self.tabla_tele():
            if self.statusz == 'gep dob':
                self.dobas() if self.animacio == 'n' else self.dobas_animacioval()
                self.kirajzolas()
                self.statusz = 'gep valaszt'
                self.mentes()
                time.sleep(self.GEP_DOBAS_ALVAS)

            if self.statusz == 'gep valaszt':
                self.kirajzolas()
                self.hely_valasztas(self.szamlista)
                self.statusz = 'jatekos dob'
                self.mentes()
                time.sleep(self.GEP_VALASZTAS_ALVAS)

            if self.statusz == 'jatekos dob':
                self.dobas() if self.animacio == 'n' else self.dobas_animacioval()
                self.kirajzolas()
                self.statusz = 'jatekos valaszt'
                self.mentes()

            if self.statusz == 'jatekos valaszt':
                self.kirajzolas()
                self.hely_valasztas(self.szamlista)
                self.statusz = 'gep dob'
                self.mentes()
                time.sleep(self.JATEKOS_VALASZTAS_ALVAS)

        gyoztes, gyoztes_pontja, vesztes_pontja, fileba_kerult = self.eredmenykalkulacio()
        self.eredmenyhirdetes(gyoztes, gyoztes_pontja, vesztes_pontja, fileba_kerult)

    @staticmethod
    def eredmeny_file_van() -> bool:
        """Megnezi, hogy van-e eredmeny file."""

        return os.path.isfile('eredmenyek.txt')

    @staticmethod
    def mentes_van() -> bool:
        """Megnezi, hogy van-e mentes file."""

        return os.path.isfile('mentes.json')

    def tabla_tele(self) -> bool:
        """Megnezi, hogy tele van-e a tabla."""

        for (gep_ertek, jatekos_ertek) in zip(self.tabla['gep'].values(), self.tabla['jatekos'].values()):
            if gep_ertek == None or jatekos_ertek == None:
                return False

        return True

    def mentes(self):
        """Elmenti a jatekot egy mentes.json fileba."""

        adatok = {
            'statusz': self.statusz,
            'tabla': self.tabla,
            'szamlista': self.szamlista,
            'nev': self.nev,
            'nehezseg': self.nehezseg,
            'animacio': self.animacio,
            'most_beirt': self.most_beirt,
        }

        with open('mentes.json', 'w') as file:
            json.dump(adatok, file)

    def mentes_betoltes(self):
        """Betolti a mentest a mentes.json filebol."""

        with open('mentes.json') as file:
            mentes = json.load(file)

        self.statusz = mentes['statusz']
        self.tabla = mentes['tabla']
        self.szamlista = mentes['szamlista']
        self.nev = mentes['nev']
        self.nehezseg = mentes['nehezseg']
        self.animacio = mentes['animacio']
        self.most_beirt = mentes['most_beirt']

    @staticmethod
    def valasztas(szoveg: str, opciok: list):
        """Egyszerusites az olyan inputok beirasara ami bizonyos valaszokat fogad el."""

        valasz = 'valami hulyeseg'
        while valasz not in opciok:
            valasz = unidecode(input(szoveg)).lower()

        return valasz

    def adatbekeres(self):
        """Bekeri a nev, nehezseg es animacio adatokat."""

        self.nev = input('Felhasznalonev: ')
        self.nehezseg = self.valasztas('Konnyu vagy nehez jatek (k/n): ', opciok=['k', 'n'])
        self.animacio = self.valasztas('Szeretnel dobas animaciot? (i/n): ', opciok=['i', 'n'])

    def dobas(self):
        """Visszaad 5 random szamot es kirajzolja az allast."""

        self.szamlista = random.choices(self.DOBAS_LEHETOSEGEK, k=5)

    def dobas_animacioval(self):
        """Dobas animacio logika."""

        for i in range(30, 1, -1):
            self.dobas()
            self.kirajzolas()
            time.sleep(1/i)

        self.dobas()

    def hely_valasztas(self, szamlista):
        """A helyvalasztasert felelos logika"""

        def ures_helyek() -> List[str]:
            """Megnezi melyik helyek szabadok az epp soronlevo jatekosnak."""

            uresek = []
            for key, value in self.tabla[self.statusz.split(' ')[0]].items():
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
            self.kirajzolas(kalkulaciokkal=True, ures_szabalyos_kalkulacioi=ures_szabalyos_kalkulacioi)
            dontes = self.valasztas(f'Melyik helyre szeretned beirni?\n', ures_szabalyosak + ['quit'])
            if dontes == 'quit':
                quit()
            self.tabla['jatekos'][dontes] = ures_szabalyos_kalkulacioi[dontes]
            self.most_beirt = self.JATEKOS_FORMATOK[self.MEZOK.index(dontes)]

        def konnyu_gep_valaszt():
            dontes = tuple(ures_szabalyos_kalkulacioi.keys())[0]
            self.tabla['gep'][dontes] = tuple(ures_szabalyos_kalkulacioi.values())[0]
            self.most_beirt = self.GEP_FORMATOK[self.MEZOK.index(dontes)]

        def nehez_gep_valaszt():
            legtobb_pont = max(ures_szabalyos_kalkulacioi.values())
            forditott_ures_szabalyos_kalkulacioi = dict(reversed(list(ures_szabalyos_kalkulacioi.items())))
            for key, value in forditott_ures_szabalyos_kalkulacioi.items():
                if value == legtobb_pont:
                    self.tabla['gep'][key] = value
                    self.most_beirt = self.GEP_FORMATOK[self.MEZOK.index(key)]
                    break

        kalkulaciok = self.kalkulacio(szamlista)

        uresek = ures_helyek()
        szabalyosak = szabalyos_helyek(kalkulaciok)

        ures_szabalyosak = ures_szabalyos_helyek(uresek, szabalyosak)
        ures_szabalyos_kalkulacioi = {ures_szabalyos: kalkulaciok[ures_szabalyos] for ures_szabalyos in ures_szabalyosak}

        if self.statusz.split(' ')[0] == 'jatekos':
            jatekos_valasztas()

        elif self.nehezseg == 'k':
            konnyu_gep_valaszt()

        elif self.nehezseg == 'n':
            nehez_gep_valaszt()

        self.kirajzolas()

    @staticmethod
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

    def kirajzolas(self, kalkulaciokkal=False, ures_szabalyos_kalkulacioi=None):
        """Kirajzolja a jatekot."""

        os.system('cls')

        tablastring = TABLASTRING
        tablamap = {
            'gt': self.tabla['gep']['tetszoleges'],
            'gp': self.tabla['gep']['par'],
            'gd': self.tabla['gep']['drill'],
            'gkp': self.tabla['gep']['ket par'],
            'gkip': self.tabla['gep']['kis poker'],
            'gf': self.tabla['gep']['full'],
            'gks': self.tabla['gep']['kis sor'],
            'gns': self.tabla['gep']['nagy sor'],
            'gnp': self.tabla['gep']['nagy poker'],

            'jt': self.tabla['jatekos']['tetszoleges'],
            'jp': self.tabla['jatekos']['par'],
            'jd': self.tabla['jatekos']['drill'],
            'jkp': self.tabla['jatekos']['ket par'],
            'jkip': self.tabla['jatekos']['kis poker'],
            'jf': self.tabla['jatekos']['full'],
            'jks': self.tabla['jatekos']['kis sor'],
            'jns': self.tabla['jatekos']['nagy sor'],
            'jnp': self.tabla['jatekos']['nagy poker'],
        }

        if self.most_beirt:
            tablamap[self.most_beirt] = Fore.CYAN + str(tablamap[self.most_beirt]) + Style.RESET_ALL

        if kalkulaciokkal:
            for key, value in ures_szabalyos_kalkulacioi.items():
                mezo_nev = self.JATEKOS_FORMATOK[self.MEZOK.index(key)]
                tablamap[mezo_nev] = Fore.YELLOW + str(value) + Style.RESET_ALL

        str_szamlista = ' '.join(map(str, self.szamlista))

        print(tablastring.format(**tablamap).replace('None', ''))
        print(self.statusz)
        print(str_szamlista)

    def eredmenykalkulacio(self):
        """Kiaklkulalja a jatek vegeredmenyet. Ha dontetlen akkor ki is irja."""

        gep_pontja = sum(self.tabla['gep'].values())
        jatekos_pontja = sum(self.tabla['jatekos'].values())

        gyoztes = ''
        gyoztes_nev = ''
        gyoztes_pontja = 0
        vesztes_pontja = 0
        if jatekos_pontja > gep_pontja:
            gyoztes = 'jatekos'
            gyoztes_nev = self.nev
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
            self.kirajzolas()

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

    def eredmenyhirdetes(self, gyoztes, gyoztes_pontja, vesztes_pontja, fileba_kerult):
        """Kirajzolja az eredmeny file-t is.
        Ha az eredmeny nem dontetlen, kihirdeti a gyoztest."""

        self.kirajzolas()
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


Kockapoker()
