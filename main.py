# Main app


import ccxt
import pprint
import time
import pandas as pd
import datetime
from datetime import timedelta

with open("C:/Users/CJH/Desktop/keys/binance.txt") as f:
    lines = f.readlines()
    api_key = lines[0].strip()
    secret = lines[1].strip()

binance = ccxt.binance(config={
    'apiKey': api_key,
    'secret': secret,
    'enableRateLimit': True,
    'options': {
        'defaultType': 'future'
    }
})

symbol_list = ['1000FLOKI/USDT', '1000LUNC/USDT', '1000PEPE/USDT', '1000SHIB/USDT', '1000XEC/USDT', '1INCH/USDT', \
               'AAVE/USDT', 'ACH/USDT', 'AGIX/USDT', 'ALGO/USDT', \
               'ALPHA/USDT', 'ANKR/USDT', 'ANT/USDT', 'APE/USDT', 'APT/USDT', 'ARB/USDT', 'ARPA/USDT', 'AR/USDT', \
               'ATOM/USDT', 'AUDIO/USDT', 'AVAX/USDT', 'AXS/USDT', \
               'BAND/USDT', 'BAT/USDT', 'BEL/USDT', 'BLUR/USDT', 'C98/USDT', 'CELR/USDT', \
               'CFX/USDT', 'CHZ/USDT', 'CHR/USDT', 'COMBO/USDT', 'COMP/USDT', 'CTSI/USDT', \
               'DASH/USDT', \
               'DOGE/USDT', 'DOT/USDT', 'DUSK/USDT', 'DYDX/USDT', 'EDU/USDT', 'EGLD/USDT', 'ENJ/USDT', \
               'ENS/USDT', 'FET/USDT', 'FIL/USDT', 'FOOTBALL/USDT', 'FTM/USDT', 'FXS/USDT', \
               'GALA/USDT', \
               'GAL/USDT', 'GMT/USDT', 'GMX/USDT', 'GRT/USDT', 'HBAR/USDT', 'HIGH/USDT', \
               'ICP/USDT', 'ICX/USDT', 'ID/USDT', 'IMX/USDT', 'INJ/USDT', 'IOST/USDT', 'IOTA/USDT', 'JASMY/USDT', \
               'JOE/USDT', 'KAVA/USDT', 'KEY/USDT', 'KNC/USDT', 'KSM/USDT', 'LDO/USDT', 'LINA/USDT', 'LINK/USDT', \
               'LPT/USDT', 'LQTY/USDT', 'LRC/USDT', 'LUNA2/USDT', 'MAGIC/USDT', 'MANA/USDT', 'MASK/USDT', \
               'MATIC/USDT', 'MAV/USDT', 'MDT/USDT', 'MINA/USDT', 'MKR/USDT', 'MTL/USDT', 'NEAR/USDT', 'NEO/USDT', \
               'NMR/USDT', 'NKN/USDT', \
               'OCEAN/USDT', 'OGN/USDT', 'OMG/USDT', 'ONE/USDT', 'ONT/USDT', 'OP/USDT', 'PEOPLE/USDT', 'RDNT/USDT', \
               'REEF/USDT', 'REN/USDT', 'RLC/USDT', 'RNDR/USDT', 'ROSE/USDT', 'RSR/USDT', 'RVN/USDT', \
               'SAND/USDT', 'SFP/USDT', 'SKL/USDT', 'SNX/USDT', 'SOL/USDT', 'SPELL/USDT', 'SSV/USDT', 'STG/USDT', \
               'STORJ/USDT', 'STX/USDT', 'SUI/USDT', 'SUSHI/USDT', 'SXP/USDT', 'TOMO/USDT', 'THETA/USDT', 'TRB/USDT', \
               'TRU/USDT', 'TRX/USDT', 'T/USDT', 'UNFI/USDT', 'UNI/USDT', 'USDC/USDT', 'VET/USDT', 'WAVES/USDT', \
               'WLD/USDT', 'WOO/USDT', 'XLM/USDT', 'XMR/USDT', 'XVG/USDT', 'YFI/USDT', 'ZEC/USDT', 'ZEN/USDT', \
               'ZIL/USDT', 'ZRX/USDT'
               ]  # 리스트 바꿨으면 밑에 종료 시 시간 측정하는 코드에서 심볼 바꿔줘야 함.

# Initialize a dictionary to store the details of each symbol
symbol_details = {symbol1: {'previous_minute': None, 'entering_time': None, 'investment': False, \
                            'long_or_short': None, 'investment_amount': None, 'recent_invest': None, 'from_invest': 61} for symbol1 in
                  symbol_list}

while True:

    try:

        # Binance 서버 시간을 가져옴
        server_time = binance.fetch_time()

        # 서버 시간을 datetime 객체로 변환
        server_datetime = datetime.datetime.fromtimestamp(server_time // 1000)
        server_datetime = server_datetime - timedelta(hours=9)

        # 현재 분 값을 가져옴
        current_minute = server_datetime.minute

        # 계좌 잔고
        balance = binance.fetch_balance(params={"type": "future"})
        free_balance = balance['USDT']['free']

        # 실행 시간 체크
        start_time = time.time()

        # Loop over each symbol
        for symbol1 in symbol_list:
            try:

                # Fetch the previous minute, entering time, investment status, long or short, and investment amount
                previous_minute = symbol_details[symbol1]['previous_minute']
                entering_time = symbol_details[symbol1]['entering_time']
                investment = symbol_details[symbol1]['investment']
                long_or_short = symbol_details[symbol1]['long_or_short']
                investment_amount = symbol_details[symbol1]['investment_amount']
                recent_invest = symbol_details[symbol1]['recent_invest']
                from_invest = symbol_details[symbol1]['from_invest']

                if previous_minute is not None and current_minute != previous_minute:
                    if symbol1 == '1000FLOKI/USDT':
                        time.sleep(1.5)

                    if investment:

                        open_orders = binance.fetch_open_orders(symbol=symbol1)
                        number_of_open_orders = len(open_orders)
                        limit_price = 0.0
                        for order in open_orders:
                            if order['type'] == 'limit':
                                limit_price = order['price']

                        if number_of_open_orders == 1 or number_of_open_orders == 0:
                            investment = False
                            investment_amount = None
                            long_or_short = None
                            entering_time = None
                            recent_invest = server_datetime
                            from_invest = 2

                            for order in open_orders:
                                binance.cancel_order(order['id'], symbol1)

                            balance = binance.fetch_balance(params={"type": "future"})
                            positions = balance['info']['positions']

                            btc_position = next((position for position in positions \
                                                 if position['symbol'] == symbol1.replace('/', '')), None)

                            if btc_position:
                                position_amt = float(btc_position['positionAmt'])

                                # 포지션 종료하기
                                if position_amt > 0:  # LONG 포지션
                                    order = binance.create_market_order(symbol=symbol1, side="sell",
                                                                        amount=position_amt)
                                elif position_amt < 0:  # SHORT 포지션
                                    order = binance.create_market_order(symbol=symbol1, side="buy",
                                                                        amount=-position_amt)

                                print(f"{symbol1} closed. (number of open orders : {number_of_open_orders})")
                            else:
                                print(f"No {symbol1} position found.")

                        elif number_of_open_orders == 2:

                            print(f'{server_datetime} 분이 바뀜. investment : {investment} / symbol : {symbol1}')
                            print(f'진입 시간 : {entering_time}')
                            print('!!!!!!!!!!!!!!!********************!!!!!!!!!!!!!!!!!!!******************')

                            # 이전 분 값을 현재 분 값으로 업데이트
                            previous_minute = current_minute
                            symbol_details[symbol1]['from_invest'] = from_invest
                            symbol_details[symbol1]['previous_minute'] = previous_minute

                            continue

                # 이전 분 값과 현재 분 값이 다른 경우 (분이 넘어간 경우)
                if previous_minute is not None and current_minute != previous_minute:

                    # 계좌 잔고 체크
                    if free_balance <= 6:
                        previous_minute = current_minute
                        from_invest += 1
                        symbol_details[symbol1]['previous_minute'] = previous_minute
                        symbol_details[symbol1]['from_invest'] = from_invest
                        continue


                    # print(f'{server_datetime} 분이 바뀜. investment : {investment} / symbol : {symbol1}')

                    if from_invest >= 61:
                        btc = binance.fetch_ohlcv(
                            symbol=symbol1,
                            timeframe='1m',
                            since=None,
                            limit=61
                        )
                    else:
                        btc = binance.fetch_ohlcv(
                            symbol=symbol1,
                            timeframe='1m',
                            since=None,
                            limit=from_invest
                        )

                    from_invest += 1

                    df = pd.DataFrame(btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
                    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')

                    # Get the last 'open' price
                    last_open_price = df.iloc[-1]['open']

                    # Get all the 'open' prices except for the last one
                    previous_open_prices = df.iloc[:-1]['open']

                    decision = False

                    # Compare the prices
                    for i, price in previous_open_prices[::-1].items():
                        if last_open_price / price >= 1.03:
                            decision = True
                            long_or_short = 'short'
                            entering_time = df.iloc[-1]['datetime']  # Correct the index reference
                            break

                    if decision:
                        investment_amount = 40 / last_open_price
                        investment = True
                        short_enter_price = last_open_price
                        orders = [None] * 3

                        if long_or_short == 'short':
                            # limit price
                            orders[0] = binance.create_market_sell_order(
                                symbol=symbol1,
                                amount=investment_amount
                            )
                            print(f'{symbol1} : order1 okay')

                            balance = binance.fetch_balance(params={"type": "future"})
                            positions = balance['info']['positions']

                            entry_price = 0.0
                            for position in positions:
                                if position['symbol'] == symbol1.replace('/', ''):
                                    entry_price = float(position['entryPrice'])
                                    break

                            downprice = last_open_price * 0.99

                            print(entry_price)

                            if 0.0 < entry_price <= downprice:
                                # take profit
                                orders[1] = binance.create_market_buy_order(
                                    symbol=symbol1,
                                    amount=investment_amount
                                )
                                print('order2 : market buy')

                            else:
                                # take profit
                                orders[1] = binance.create_order(
                                    symbol=symbol1,
                                    type="TAKE_PROFIT",
                                    side="buy",
                                    amount=investment_amount,
                                    price=downprice,
                                    params={'stopPrice': downprice, 'reduceOnly': True}
                                )
                                print('order2 okay')

                            upprice = last_open_price * 1.01

                            if entry_price >= upprice:
                                # stop loss
                                orders[2] = binance.create_market_buy_order(
                                    symbol=symbol1,
                                    amount=investment_amount
                                )
                                print('order3 : market buy')

                            else:
                                # stop loss
                                orders[2] = binance.create_order(
                                    symbol=symbol1,
                                    type="STOP",
                                    side="buy",
                                    amount=investment_amount,
                                    price=upprice,
                                    params={'stopPrice': upprice, 'reduceOnly': True}
                                )
                                print('order3 okay')

                            # 계좌 잔고 업데이트
                            balance = binance.fetch_balance(params={"type": "future"})
                            free_balance = balance['USDT']['free']


                if previous_minute is not None and current_minute != previous_minute and symbol1 == 'ZRX/USDT':
                    # 종료 시간 저장
                    end_time = time.time()

                    # 실행 시간 계산
                    execution_time = end_time - start_time
                    print(f"{server_datetime} Execution time: {execution_time} seconds")

                # 이전 분 값을 현재 분 값으로 업데이트
                previous_minute = current_minute
                # Update the details of the symbol in the symbol_details dictionary
                symbol_details[symbol1]['previous_minute'] = previous_minute
                symbol_details[symbol1]['entering_time'] = entering_time
                symbol_details[symbol1]['investment'] = investment
                symbol_details[symbol1]['long_or_short'] = long_or_short
                symbol_details[symbol1]['investment_amount'] = investment_amount
                symbol_details[symbol1]['recent_invest'] = recent_invest
                symbol_details[symbol1]['from_invest'] = from_invest


            except Exception as e:
                print(f"An error occurred: {e}")
                previous_minute = current_minute
                symbol_details[symbol1]['previous_minute'] = previous_minute
                symbol_details[symbol1]['entering_time'] = entering_time
                symbol_details[symbol1]['investment'] = investment
                symbol_details[symbol1]['long_or_short'] = long_or_short
                symbol_details[symbol1]['investment_amount'] = investment_amount
                symbol_details[symbol1]['recent_invest'] = recent_invest
                symbol_details[symbol1]['from_invest'] = from_invest
                continue

        # API 호출 제한을 피하기 위해 약간의 딜레이를 주는 것이 좋음
        time.sleep(1)


    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(1)
        continue

