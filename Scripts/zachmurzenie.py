from __future__ import division

with open('dane_zachmurzenie.txt', 'r') as plik:    x = [float(liczba) for liczba in plik.readlines()[0].split(' ')]
pk = open('zachmurzenie.csv', 'w')
krok = 15
licznik = -90 + krok / 2
ilosc_paseczkow = int(krok / 2.5)

for i in range(0, len(x), 144 * ilosc_paseczkow):
    pk.write(str(licznik) + ',' + str(
        sum(x[i:i + 144 * ilosc_paseczkow]) / len(x[i:i + 144 * ilosc_paseczkow]) / 100) + '\n')
    licznik += krok
pk.close()
# wyrzucony plik w formacie latitude,average cloud coverage [%]
