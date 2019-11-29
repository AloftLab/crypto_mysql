import ccxt
import database_connect
from datetime import datetime


# connectt to DB
mydbconnobj = database_connect.DBConnection("localhost","kraken","root","yourpasswordhere")
mydbconn = mydbconnobj.get_conn()

#define exchange parameters
bitstamp = ccxt.bitstamp({
	'rateLimit': 2000,
	'enableRateLimit': True,
	'exchangeName': "bitstamp"})

kraken = ccxt.kraken({
	'rateLimit': 1000,
	'enableRateLimit': True,
	'exchangeName': "kraken"})
  
  #will add more exchanges in future... 

#define exchange symbols
bitstamp_symbols = ['BCH/BTC', 'BCH/EUR', 'BCH/USD', 'BTC/EUR', 'BTC/USD', 'ETH/BTC', 'ETH/EUR', 'ETH/USD', 'EUR/USD',
					'LTC/BTC', 'LTC/EUR', 'LTC/USD', 'XRP/BTC', 'XRP/EUR', 'XRP/USD']

kraken_symbols = ['ADA/BTC', 'ADA/CAD', 'ADA/ETH', 'ADA/EUR', 'ADA/USD', 'ATOM/BTC', 'ATOM/CAD', 'ATOM/ETH', 'ATOM/EUR',
			'ATOM/USD', 'BAT/BTC', 'BAT/ETH', 'BAT/EUR', 'BAT/USD', 'BCH/BTC', 'BCH/EUR', 'BCH/USD', 'BTC/CAD',
			'BTC/EUR', 'BTC/GBP', 'BTC/JPY', 'BTC/USD', 'DAI/EUR', 'DAI/USD', 'DAI/USDT', 'DASH/BTC', 'DASH/EUR',
			'DASH/USD', 'DOGE/BTC', 'EOS/BTC', 'EOS/ETH', 'EOS/EUR', 'EOS/USD', 'ETC/BTC', 'ETC/ETH', 'ETC/EUR',
			'ETC/USD', 'ETH/BTC', 'ETH/CAD', 'ETH/DAI', 'ETH/EUR', 'ETH/GBP', 'ETH/JPY', 'ETH/USD', 'GNO/BTC',
			'GNO/ETH', 'GNO/EUR', 'GNO/USD','ICX/BTC', 'ICX/ETH', 'ICX/EUR', 'ICX/USD', 'LINK/BTC', 'LINK/ETH',
			'LINK/EUR', 'LINK/USD', 'LSK/BTC', 'LSK/ETH', 'LSK/EUR', 'LSK/USD', 'LTC/BTC', 'LTC/EUR', 'LTC/USD',
			'MLN/BTC', 'MLN/ETH', 'NANO/BTC', 'NANO/ETH', 'NANO/EUR', 'NANO/USD', 'OMG/BTC', 'OMG/ETH', 'OMG/EUR',
			'OMG/USD', 'PAXG/BTC', 'PAXG/ETH', 'PAXG/EUR', 'PAXG/USD', 'QTUM/BTC', 'QTUM/CAD', 'QTUM/ETH', 'QTUM/EUR',
			'QTUM/USD', 'REP/BTC', 'REP/ETH', 'REP/EUR', 'REP/USD', 'SC/BTC', 'SC/ETH', 'SC/EUR', 'SC/USD', 'USDT/USD',
			'WAVES/BTC', 'WAVES/ETH', 'WAVES/EUR', 'WAVES/USD', 'XLM/BTC', 'XLM/EUR', 'XLM/USD', 'XMR/BTC', 'XMR/EUR',
			'XMR/USD', 'XRP/BTC', 'XRP/CAD', 'XRP/EUR', 'XRP/JPY', 'XRP/USD', 'XTZ/BTC', 'XTZ/CAD', 'XTZ/ETH', 'XTZ/EUR',
			'XTZ/USD', 'ZEC/BTC', 'ZEC/EUR', 'ZEC/JPY', 'ZEC/USD']

    #Use these (once) to create tables in your DB
		"""mycursor = mydbconn.cursor()
		print(bitstamp_symbols)
		for s in bitstamp_symbols:
			la = s.replace("/","")
			print(la)
			mycursor.execute("CREATE TABLE IF NOT EXISTS %s (closing DECIMAL(20,10), timestamp TIMESTAMP(6), open DECIMAL(20,10), high DECIMAL(20,10), low DECIMAL(20,10), volume FLOAT(10), bid DECIMAL(20,10), ask DECIMAL(20,10))" % la)

		#"show tables"
		mycursor.execute("SHOW TABLES")

		for tb in mycursor:
			print(tb)"""



def ticker(exchange, currency):
	print(currency)
	currency2 = currency.replace("/", "")
	ticker = exchange.fetch_ticker(currency)

	closing = ticker['last']
	timestamp = ticker['timestamp']
	open = ticker['open']
	high = ticker['high']
	low = ticker['low']
	volume = ticker['baseVolume']
	bid = ticker['bid']
	ask = ticker['ask']

	# Check for empty values

	if not open:
		open = 0
	if not high:
		high = 0
	if not low:
		low = 0
	if not volume:
		volume = 0
	if not bid:
		bid = 0
	if not ask:
		ask = 0
  
  #changes timestamp from exchange to redable version for humans and mysql
	timestamp = timestamp/1000
	timestamp = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
  
  #connects to DB and store data to DB
	mycursor = mydbconn.cursor()
	data = closing, timestamp, open, high, low, volume, bid, ask
	insert = "INSERT INTO {table} (closing, timestamp, open, high, low, volume, bid, ask) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
	mycursor.execute(insert.format(table=currency2), data)

	mydbconn.commit()
  
while True:
	try:
		for s in kraken_symbols:
			ticker(kraken, s)
      
	except ValueError:
		print("value error")
		continue
    
	else:
		continue




