import random
from typing import List, Tuple
import os
import time
from pandas import DataFrame
from colorama import Fore, Back, Style
import json

dobas_lehetosegek = [1, 2, 3, 4, 5, 6]


def jatek():
    def adatbekeres() -> Tuple[str, str, str]:
        nev = input("Ird be a neved: ")

        nehezseg = ''
        while nehezseg != 'k' and nehezseg != 'n':
            nehezseg = input("Konnyu vagy nehez jatek (k/n): ")

        animacio = ''
        while animacio != 'i' and animacio != 'n':
            animacio = input("Legyenek animaciok, igen vagy nem (i/n) ")

        return nev, nehezseg, animacio

    def dobas():
        tablastring = DataFrame(tabla).to_string().replace('-1', '')

        if animacio == 'i':
            for i in range(30, 1, -1):
                print(tablastring + '\n')
                print(statusz)
                szamlista = random.choices(dobas_lehetosegek, k=5)
                print(' '.join(map(str, szamlista)) + '  =>  ' + str(sum(szamlista)))
                time.sleep(1/i)
                os.system('cls')

        os.system('cls')
        print(tablastring + '\n')

        if statusz == 'gep dob':
            print('gep dobasa')
        elif statusz == 'jatekos dob':
            print('jatekos dobasa')

        szamlista = random.choices(dobas_lehetosegek, k=5)
        print(' '.join(map(str, szamlista)) + '  =>  ' + str(sum(szamlista)))

        if statusz == 'gep dob':
            mentes_adatok = {
                'statusz': 'valasztas',
                'tabla': tabla,
                'szamlista': szamlista,
                'kor_szama': kor_szama + elozo_korok_szama,
                'kijon': 'gep',
                'nev': nev,
                'nehezseg': nehezseg,
                'animacio': animacio
            }
        elif statusz == 'jatekos dob':
            mentes_adatok = {
                'statusz': 'valasztas',
                'tabla': tabla,
                'szamlista': szamlista,
                'kor_szama': kor_szama + elozo_korok_szama,
                'kijon': 'jatekos',
                'nev': nev,
                'nehezseg': nehezseg,
                'animacio': animacio,
            }

        with open('mentes.json', 'w') as file:
            json.dump(mentes_adatok, file)

        time.sleep(2)
        return szamlista

    def valasztas(szamlista):
        os.system('cls')
        if statusz == 'gep valaszt':
            if nehezseg == 'k':
                lehetseges_dontesek = {key: kalkulacio(key, szamlista) for key, value in tabla['gep'].items() if
                                       value == -1 and kalkulacio(key, szamlista) > 0}
                if not lehetseges_dontesek:
                    lehetseges_dontesek = {key: kalkulacio(key, szamlista) for key, value in tabla['gep'].items() if
                                           value == -1}

                tabla['gep'][tuple(lehetseges_dontesek.keys())[0]] = kalkulacio(tuple(lehetseges_dontesek.keys())[0], szamlista)

                print(DataFrame(tabla).to_string().replace('-1', '') + '\n')
                print('gep dobasa')
                print(' '.join(map(str, szamlista)) + '  =>  ' + str(sum(szamlista)))

            elif nehezseg == 'n':
                szabad_mezok = [key for key, value in tabla['gep'].items() if value == -1]
                kalkulaciok = [kalkulacio(szabad_mezo, szamlista) for szabad_mezo in szabad_mezok]
                legnagyobb_index = kalkulaciok.index(max(kalkulaciok))

                tabla['gep'][szabad_mezok[legnagyobb_index]] = kalkulaciok[legnagyobb_index]

                print(DataFrame(tabla).to_string().replace('-1', '') + '\n')
                print('gep dobasa')
                print(' '.join(map(str, szamlista)) + '  =>  ' + str(sum(szamlista)))

        elif statusz == 'jatekos valaszt':
            print(DataFrame(tabla).to_string().replace('-1', '') + '\n')
            print('jatekos dobasa')
            print(' '.join(map(str, szamlista)) + '  =>  ' + str(sum(szamlista)))

            lehetseges_dontesek = {key: kalkulacio(key, szamlista) for key, value in tabla['jatekos'].items() if value == -1 and kalkulacio(key, szamlista) > 0}
            if not lehetseges_dontesek:
                lehetseges_dontesek = {key: kalkulacio(key, szamlista) for key, value in tabla['jatekos'].items() if value == -1}
            dontes = ''
            while dontes not in lehetseges_dontesek:
                dontes = input(f'Melyik mezot szeretned kitolteni {lehetseges_dontesek}\n')
                if dontes == 'quit':
                    quit()

            tabla['jatekos'][dontes] = kalkulacio(dontes, szamlista)

            os.system('cls')
            print(DataFrame(tabla).to_string().replace('-1', '') + '\n')
            print('jatekos dobasa')
            print(' '.join(map(str, szamlista)) + '  =>  ' + str(sum(szamlista)))

        if statusz == 'gep valaszt':
            mentes_adatok = {
                'statusz': 'dobas',
                'tabla': tabla,
                'kor_szama': kor_szama + elozo_korok_szama,
                'kijon': 'jatekos',
                'nev': nev,
                'nehezseg': nehezseg,
                'animacio': animacio,
            }
        elif statusz == 'jatekos valaszt':
            mentes_adatok = {
                'statusz': 'bobas',
                'tabla': tabla,
                'kor_szama': kor_szama + elozo_korok_szama + 1,
                'kijon': 'gep',
                'nev': nev,
                'nehezseg': nehezseg,
                'animacio': animacio,
            }

        with open('mentes.json', 'w') as file:
            json.dump(mentes_adatok, file)

        time.sleep(2.5)

    def kalkulacio(elnevezes, szamlista: List[int]) -> int:
        szamlista = sorted(szamlista, reverse=True)

        if elnevezes == 'tetszoleges':
            return sum(szamlista)

        elif elnevezes == 'par':
            for i, szam in enumerate(szamlista):
                try:
                    if szam == szamlista[i+1]:
                        return szam * 2

                except IndexError:
                    return 0

        elif elnevezes == 'drill':
            for i, szam in enumerate(szamlista):
                try:
                    if szam == szamlista[i+1] == szamlista[i+2]:
                        return szam * 3

                except IndexError:
                    return 0

        elif elnevezes == 'ket par':
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
                    if szam == szamlista[i+1]:
                        szamok.append(szam)
                        talalat = True

                except IndexError:
                    return 0

            return 0

        elif elnevezes == 'kis poker':
            for i, szam in enumerate(szamlista):
                try:
                    if szam == szamlista[i+1] == szamlista[i+2] == szamlista[i+3]:
                        return szam * 4

                except IndexError:
                    return 0

        elif elnevezes == 'full':
            if (szamlista[0] == szamlista[1] == szamlista[2] and szamlista[3] == szamlista[4]) or (szamlista[0] == szamlista[1] and szamlista[2] == szamlista[3] == szamlista[4]):
                return sum(szamlista)

            return 0

        elif elnevezes == 'kis sor':
            if szamlista == [5, 4, 3, 2, 1]:
                return 15

            return 0

        elif elnevezes == 'nagy sor':
            if szamlista == [6, 5, 4, 3, 2]:
                return 20

            return 0

        elif elnevezes == 'nagy poker':
            if len(set(szamlista)) == 1:
                return 50

            return 0

    tabla = {
        'gep': {
            'tetszoleges': -1,
            'par': -1,
            'drill': -1,
            'ket par': -1,
            'kis poker': -1,
            'full': -1,
            'kis sor': -1,
            'nagy sor': -1,
            'nagy poker': -1
        },
        'jatekos': {
            'tetszoleges': -1,
            'par': -1,
            'drill': -1,
            'ket par': -1,
            'kis poker': -1,
            'full': -1,
            'kis sor': -1,
            'nagy sor': -1,
            'nagy poker': -1
        },
    }
    try:
        with open('eredmenyek.txt', 'r') as file:
            pass

    except FileNotFoundError:
        with open('eredmenyek.txt', 'w') as file:
            pass

    valasztasnal_indul = False
    kijon = ''
    elozo_korok_szama = 0
    try:
        with open('mentes.json', 'r') as file:
            pass

    except FileNotFoundError:
        korok_szama = 9
        nev, nehezseg, animacio = adatbekeres()

    else:
        dontes = ''
        while dontes != 'i' and dontes != 'n':
            dontes = input('Mentett jatek folytatasa (i/n) ')
            if dontes == 'i':
                with open('mentes.json', 'r') as file:
                    mentes = json.load(file)

                tabla = mentes['tabla']
                korok_szama = 9 - mentes['kor_szama']
                elozo_korok_szama = mentes['kor_szama']
                kijon = mentes['kijon']
                nev = mentes['nev']
                nehezseg = mentes['nehezseg']
                animacio = mentes['animacio']
                if mentes['statusz'] == 'valasztas':
                    szamlista = mentes['szamlista']
                    valasztasnal_indul = True

            elif dontes == 'n':
                korok_szama = 9
                os.remove('mentes.json')
                nev, nehezseg, animacio = adatbekeres()

    for kor_szama in range(korok_szama):
        if kijon == 'gep':
            if valasztasnal_indul:
                statusz = 'gep valaszt'
                valasztas(szamlista)

                statusz = 'jatekos dob'
                szamlista = dobas()
                statusz = 'jatekos valaszt'
                valasztas(szamlista)

            else:
                statusz = 'gep dob'
                szamlista = dobas()
                statusz = 'gep valaszt'
                valasztas(szamlista)

                statusz = 'jatekos dob'
                szamlista = dobas()
                statusz = 'jatekos valaszt'
                valasztas(szamlista)

        elif kijon == 'jatekos':
            if valasztasnal_indul:
                statusz = 'jatekos valaszt'
                valasztas(szamlista)

            else:
                statusz = 'jatekos dob'
                szamlista = dobas()
                statusz = 'jatekos valaszt'
                valasztas(szamlista)

        else:
            statusz = 'gep dob'
            szamlista = dobas()
            statusz = 'gep valaszt'
            valasztas(szamlista)

            statusz = 'jatekos dob'
            szamlista = dobas()
            statusz = 'jatekos valaszt'
            valasztas(szamlista)

        kijon = ''

    os.system('cls')
    print(DataFrame(tabla).to_string().replace('-1', '') + '\n')

    gep_pontja = sum(tabla['gep'].values())
    jatekos_pontja = sum(tabla['jatekos'].values())

    with open('eredmenyek.txt', 'r', encoding='UTF-8') as file:
        sorok = file.readlines()

    fileba_kerult = False
    if gep_pontja < jatekos_pontja:
        print('Te nyertel!\nAz eredmeny ' + str(gep_pontja) + ' - ' + Fore.CYAN + str(jatekos_pontja) + Style.RESET_ALL + '\n')

        if not sorok:
            with open('eredmenyek.txt', 'w', encoding='UTF-8') as file:
                file.write(f'{nev} {jatekos_pontja}\n')

            fileba_kerult = True

        else:
            nagyobb_eredmeny = False
            for sor_szam, pont in enumerate(map(lambda x: int(x.split(' ')[1]), sorok)):
                if jatekos_pontja > pont:
                    sorok.insert(sor_szam, f'{nev} {jatekos_pontja}\n')

                    with open('eredmenyek.txt', 'w') as file:
                        file.writelines(sorok)

                    fileba_kerult = True

                    nagyobb_eredmeny = True

                    break

            if not nagyobb_eredmeny and len(sorok) < 10:
                with open('eredmenyek.txt', 'a') as file:
                    file.write(f'{nev} {jatekos_pontja}\n')

                fileba_kerult = True

    elif jatekos_pontja < gep_pontja:
        print('Gep nyert!\nAz eredmeny ' + Fore.CYAN + str(gep_pontja) + Style.RESET_ALL + ' - ' + str(jatekos_pontja) + '\n')

        if not sorok:
            with open('eredmenyek.txt', 'w', encoding='UTF-8') as file:
                file.write(f'szamitogep {gep_pontja}\n')

            fileba_kerult = True

        else:
            nagyobb_eredmeny = False
            for sor_szam, pont in enumerate(map(lambda x: int(x.split(' ')[1]), sorok)):
                if gep_pontja > pont:
                    sorok.insert(sor_szam, f'szamitogep {gep_pontja}\n')

                    with open('eredmenyek.txt', 'w') as file:
                        file.writelines(sorok)

                    fileba_kerult = True

                    nagyobb_eredmeny = True

                    break

            if not nagyobb_eredmeny and len(sorok) < 10:
                with open('eredmenyek.txt', 'a') as file:
                    file.write(f'szamitogep {gep_pontja}\n')

                fileba_kerult = True

    else:
        print('Dontetlen!\nAz eredmeny ' + str(gep_pontja) + ' - ' + str(jatekos_pontja) + '\n')

    with open('eredmenyek.txt', 'r') as file:
        sorok = file.readlines()

    if len(sorok) > 10:
        with open('eredmenyek.txt', 'w') as file:
            file.writelines(sorok[:-1])

    with open('eredmenyek.txt', 'r') as file:
        sorok = file.readlines()

    print(''.join(sorok))
    if fileba_kerult:
        print('Felkerult a legjobb 10 koze!')
    else:
        print('Nem kerult fel a legjobb 10 koze')

    os.remove('mentes.json')


jatek()
