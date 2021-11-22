'''From FHC to now: The trajectory of Euro and Dollar prices'''

# Importando bibliotecas

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

exchange_rates = pd.read_csv('euro-daily-hist_1999_2020.csv')

# Renomeando Colunas

exchange_rates.rename(columns={'[US dollar ]': 'Dollar',
                      '[Brazilian real ]': 'Euro', 'Period\\Unit:': 'Time'},
                      inplace=True)
exchange_rates['Time'] = pd.to_datetime(exchange_rates['Time'])
exchange_rates.sort_values('Time', inplace=True)

# Criando novo dataset
#Desabilitando falso positivo
# pylint: disable=no-member
real_rates = exchange_rates.filter(['Time', 'Euro', 'Dollar']).copy()

real_rates = real_rates[real_rates['Dollar'] != '-']
real_rates = real_rates[real_rates['Euro'] != '-']
real_rates = real_rates.dropna()
real_rates['Dollar'] = pd.to_numeric(real_rates['Dollar'], errors='coerce')
real_rates['Euro'] = pd.to_numeric(real_rates['Euro'], errors='coerce')
real_rates['Dollar'] = real_rates['Euro'] / real_rates['Dollar']
real_rates.sort_values('Time', inplace=True)
real_rates.reset_index(drop=True, inplace=True)

# Calculando medias

real_rates['rolling_mean_usd'] = real_rates['Dollar'].rolling(30).mean()
real_rates['rolling_mean_eur'] = real_rates['Euro'].rolling(30).mean()

# Separando periodo de cada presidente

fhc = real_rates.copy()[real_rates['Time'].dt.year < 2003]
lula = real_rates.copy()[(real_rates['Time'].dt.year >= 2003) &
                         (real_rates['Time'].dt.year < 2011)]
dilma = real_rates.copy()[(real_rates['Time'].dt.year >= 2011) &
                          (real_rates['Time'] < '2016-08-31')]
temer = real_rates.copy()[(real_rates['Time'] >= '2016-08-31') &
                          (real_rates['Time'].dt.year < 2019)]
bolsonaro = real_rates.copy()[real_rates['Time'].dt.year >= 2019]

# Gerando grafico

style.use('seaborn-pastel')

(fig, (ax1, ax2)) = plt.subplots(2, sharex=True, figsize=(12, 6))
plt.suptitle('From FHC to now: The trajectory of Euro and Dollar prices',
             fontsize=20, ha='center')

# Dollar

ax1.plot(fhc['Time'], fhc['rolling_mean_usd'], color='#BF5FFF',
         label='FHC')
ax1.plot(lula['Time'], lula['rolling_mean_usd'], color='#ffa500',
         label='Lula')
ax1.plot(dilma['Time'], dilma['rolling_mean_usd'], color='#00B2EE',
         label='Dilma')
ax1.plot(temer['Time'], temer['rolling_mean_usd'], color='#A912CE',
         label='Temer')
ax1.plot(bolsonaro['Time'], bolsonaro['rolling_mean_usd'],
         color='#D7E70E', label='Bolsonaro')
ax1.grid(alpha=0.5)
ax1.legend(loc='upper center', frameon=False, fontsize=12, ncol=5)
ax1.set_title('BRL x USD')

# Euro

ax2.plot(fhc['Time'], fhc['rolling_mean_eur'], color='#BF5FFF')
ax2.plot(lula['Time'], lula['rolling_mean_eur'], color='#ffa500')
ax2.plot(dilma['Time'], dilma['rolling_mean_eur'], color='#00B2EE')
ax2.plot(temer['Time'], temer['rolling_mean_eur'], color='#A912CE')
ax2.plot(bolsonaro['Time'], bolsonaro['rolling_mean_eur'],
         color='#D7E70E')
ax2.grid(alpha=0.5)
ax2.set_title('BRL x EUR')

plt.tight_layout()
plt.subplots_adjust(top=0.8, wspace=0.3)

plt.show()
