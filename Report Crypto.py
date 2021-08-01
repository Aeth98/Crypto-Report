import requests
import json
import operator
from datetime import datetime
from pprint import pprint

class report:
    def __init__(self):
        self.url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
        self.params = {
            'start': '1',
            'limit': '100',
            'convert': 'usd'
        }
        self.headers = {
            'Accepts': 'application/json',
            'X-CMC_PRO_API_KEY': '22c4a1f0-898a-4897-9cb6-6a7c46c1a988'
        }

    def fetchCurrenciesData(self):
        r = requests.get(url=self.url, headers=self.headers, params=self.params).json()
        return r['data']

    def getreport(self):
        i = 0
        report = {}
        highest_volume = 0
        crypto_performance = {}
        crypto_performance_sorted = {}
        top10_crypto = []
        worst10_crypto = []
        all_crypto_sorted = []
        price_crypto_high_volumes = {}
        currencies = cryptoreport.fetchCurrenciesData()
        sum_price = 0
        volume_elegibility_24h = 76000000
        first_n_crypto = 20
        details_first_n_crypto = {}
        total_holdings_yesterday = 0
        total_holdings_today = 0

        for currency in currencies:
            # trovo la crypto con il maggior volume e ad ogni iterata aggiorno se trovo un nuovo massimo
            if currency['quote']['USD']['volume_24h'] > highest_volume:
                highest_volume = currency['quote']['USD']['volume_24h']
                report['1. currency with highest volume'] = {currency['symbol']: currency['quote']['USD']['volume_24h']}
            # calcolo quantità di denaro necessaria per comprare crypto con abbastanza volume
            if currency['quote']['USD']['volume_24h'] > volume_elegibility_24h:
                price_crypto_high_volumes[currency['symbol']] = currency['quote']['USD']['price']
                sum_price = sum_price + currency['quote']['USD']['price']
            # calcolo percentuale di profitto o perdita comprando le prime 20 crypto
            if currency['cmc_rank'] < first_n_crypto + 1:
                price_today = currency['quote']['USD']['price']
                p = currency['quote']['USD']['percent_change_24h'] / 100
                price_yesterday = price_today / (1 + p)
                details_first_n_crypto[currency['symbol']] = {'price today': currency['quote']['USD']['price'],
                                                              'price yesterday': price_today / (1 + p),
                                                              'percent_change_24h': currency['quote']['USD'][
                                                                  'percent_change_24h']}
                total_holdings_yesterday = total_holdings_yesterday + price_yesterday
                total_holdings_today = total_holdings_today + price_today

            crypto_performance[currency['symbol']] = currency['quote']['USD']['percent_change_24h']

        p_profit = (total_holdings_today - total_holdings_yesterday) / total_holdings_yesterday
        report['7. percentage profit buying first 20 crypto in cmc rank'] = p_profit
        report['6. details first 20 crypto'] = details_first_n_crypto

        #ordino il dizionario per valori in ordine crescente
        crypto_performance_sorted = sorted(crypto_performance.items(), key=operator.itemgetter(1))
        report['2. overall performance'] = crypto_performance_sorted

        for currency in crypto_performance_sorted:
            all_crypto_sorted.append(currency)

        #cerco i migliori 10 e i peggiori 10
        for i in range(0, 10):
            worst10_crypto.append(all_crypto_sorted[i])
            top10_crypto.append(all_crypto_sorted[len(all_crypto_sorted) - 1 - i])
        report['3. top 10 gainers'] = top10_crypto
        report['4. top 10 losers'] = worst10_crypto
        report['5. usd requested to buy crypto with volumes higher then 76000000'] = sum_price
        return report

cryptoreport = report()
#ottenimento anno mese e giorno come stringhe
year = datetime.now().strftime("%Y")
month = datetime.now().strftime("%m")
day = datetime.now().strftime("%d")

#creazione file json
with open(day+month+year+".json", "w") as outfile:
    json.dump(cryptoreport.getreport(), outfile, indent = 4)

#test per verificare il contenuto del report
pprint(cryptoreport.getreport())

















