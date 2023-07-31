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
               'AAVE/USDT', 'ACH/USDT', 'AGIX/USDT', 'ALGO/USDT', 'ALICE/USDT', \
               'ALPHA/USDT', 'ANKR/USDT', 'ANT/USDT', 'APE/USDT', 'APT/USDT', 'ARB/USDT', 'ARPA/USDT', 'AR/USDT', \
               'ATA/USDT', 'ATOM/USDT', 'AUDIO/USDT', 'AVAX/USDT', 'AXS/USDT', \
               'BAKE/USDT', 'BAND/USDT', 'BAT/USDT', 'BEL/USDT', 'BLUR/USDT', 'C98/USDT', 'CELO/USDT', 'CELR/USDT', \
               'CFX/USDT', 'CHZ/USDT', 'CHR/USDT', 'COMBO/USDT', 'COMP/USDT', 'CRV/USDT', 'CTSI/USDT', 'DAR/USDT', \
               'DASH/USDT',  'DENT/USDT', \
               'DGB/USDT', 'DOGE/USDT', 'DOT/USDT', 'DUSK/USDT', 'DYDX/USDT', 'EDU/USDT', 'EGLD/USDT', 'ENJ/USDT', \
               'ENS/USDT', 'FET/USDT', 'FIL/USDT', 'FLM/USDT', 'FLOW/USDT', 'FOOTBALL/USDT', 'FTM/USDT', 'FXS/USDT', \
               'GALA/USDT', \
               'GAL/USDT', 'GMT/USDT', 'GMX/USDT', 'GRT/USDT', 'GTC/USDT', 'HBAR/USDT', 'HIGH/USDT', 'HOOK/USDT', \
               'ICP/USDT', 'ICX/USDT', 'ID/USDT', 'IMX/USDT', 'INJ/USDT', 'IOST/USDT', 'IOTA/USDT', 'JASMY/USDT', \
               'JOE/USDT', 'KAVA/USDT', 'KEY/USDT', 'KSM/USDT', 'LDO/USDT', 'LINA/USDT', 'LINK/USDT', \
               'LIT/USDT', \
               'LPT/USDT', 'LQTY/USDT', 'LRC/USDT', 'LUNA2/USDT', 'MAGIC/USDT', 'MANA/USDT', 'MASK/USDT', \
               'MATIC/USDT', 'MAV/USDT', 'MDT/USDT', 'MINA/USDT', 'MKR/USDT', 'MTL/USDT', 'NEAR/USDT', 'NEO/USDT', \
               'NMR/USDT', 'NKN/USDT', \
               'OCEAN/USDT', 'OMG/USDT', 'ONE/USDT', 'ONT/USDT', 'OP/USDT', 'PEOPLE/USDT', 'RDNT/USDT', \
               'REEF/USDT', 'REN/USDT', 'RLC/USDT', 'RSR/USDT', \
               'SFP/USDT', 'SNX/USDT', 'SOL/USDT', 'STG/USDT', 'STORJ/USDT', 'SUSHI/USDT', 'TOMO/USDT', 'TRB/USDT', \
               'UNFI/USDT', 'WOO/USDT', 'YFI/USDT'
               ]  # 리스트 바꿨으면 밑에 종료 시 시간 측정하는 코드에서 심볼 바꿔줘야 함.

# Initialize a dictionary to store the details of each symbol
symbol_details = {symbol1: {'previous_minute': None, 'entering_time': None, 'investment': False, \
                            'long_or_short': None, 'investment_amount': None, 'recent_invest': None} for symbol1 in
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

                if previous_minute is not None and current_minute != previous_minute:
                    if investment:

                        positions = balance['info']['positions']

                        btcusdt_position = next((position for position in positions \
                                                 if position['symbol'] == symbol1.replace('/', '')), None)

                        if btcusdt_position is not None:
                            if float(btcusdt_position['positionAmt']) == 0.0:
                                investment = False
                                investment_amount = None
                                long_or_short = None
                                entering_time = None
                                recent_invest = server_datetime

                                open_orders = binance.fetch_open_orders(
                                    symbol=symbol1
                                )
                                for order in open_orders:
                                    binance.cancel_order(order['id'], symbol1)

                        else:
                            print(f'{symbol1} position not found')

                        if investment:
                            print(f'{server_datetime} 분이 바뀜. investment : {investment} / symbol : {symbol1}')
                            print(f'진입 시간 : {entering_time}')
                            print('!!!!!!!!!!!!!!!********************!!!!!!!!!!!!!!!!!!!******************')

                            '''
                            # Calculate the time difference in minutes
                            time_diff = (server_datetime - entering_time).total_seconds() / 60

                            if (time_diff >= 181 and time_diff <= 190) or (time_diff >= 661 and time_diff <= 670):

                                if long_or_short == 'long':
                                    order = binance.create_market_sell_order(
                                        symbol=symbol1,
                                        amount=investment_amount
                                    )

                                if long_or_short == 'short':
                                    order = binance.create_market_buy_order(
                                        symbol=symbol1,
                                        amount=investment_amount
                                    )

                                open_orders = binance.fetch_open_orders(
                                    symbol=symbol1
                                )
                                for order in open_orders:
                                    result = binance.cancel_order(id=order['id'], symbol=symbol1)
                                    print("Cancelled order")  # 두번 출력되어야 함.

                                investment = False
                                investment_amount = None
                                long_or_short = None
                                entering_time = None
                                recent_invest = server_datetime
                            '''

                            if investment:
                                # 이전 분 값을 현재 분 값으로 업데이트
                                previous_minute = current_minute
                                symbol_details[symbol1]['previous_minute'] = previous_minute

                                continue

                # 이전 분 값과 현재 분 값이 다른 경우 (분이 넘어간 경우)
                if previous_minute is not None and current_minute != previous_minute:

                    # 계좌 잔고 체크
                    if free_balance <= 160:
                        previous_minute = current_minute
                        symbol_details[symbol1]['previous_minute'] = previous_minute
                        continue


                    if symbol1 == '1000FLOKI/USDT':
                        time.sleep(1)


                    # print(f'{server_datetime} 분이 바뀜. investment : {investment} / symbol : {symbol1}')

                    if recent_invest is None or server_datetime - recent_invest >= timedelta(minutes=61):
                        btc = binance.fetch_ohlcv(
                            symbol=symbol1,
                            timeframe='1m',
                            since=None,
                            limit=61
                        )
                    else:
                        # recent_invest를 Unix timestamp로 변환합니다.
                        timest = int(recent_invest.timestamp() * 1000)
                        btc = binance.fetch_ohlcv(
                            symbol=symbol1,
                            timeframe='1m',
                            since=timest,
                            limit=61
                        )

                    df = pd.DataFrame(btc, columns=['datetime', 'open', 'high', 'low', 'close', 'volume'])
                    df['datetime'] = pd.to_datetime(df['datetime'], unit='ms')

                    # Get the last 'open' price
                    last_open_price = df.iloc[-1]['open']

                    # Get all the 'open' prices except for the last one
                    previous_open_prices = df.iloc[:-1]['open']

                    decision = False

                    # Compare the prices
                    for i, price in previous_open_prices[::-1].items():
                        if last_open_price / price >= 1.03 or last_open_price / price <= 0.97:
                            decision = True
                            if last_open_price / price >= 1.03:
                                long_or_short = 'short'
                            else:
                                long_or_short = 'long'

                            entering_time = df.iloc[-1]['datetime']  # Correct the index reference
                            break

                    if decision:
                        investment_amount = 1000 / last_open_price
                        investment = True
                        short_enter_price = last_open_price * 0.95
                        # short_enter_price = last_open_price * 0.995
                        long_enter_price = last_open_price * 1.05
                        # long_enter_price = last_open_price * 1.005
                        orders = [None] * 3

                        if long_or_short == 'short':
                            # limit price
                            orders[0] = binance.create_order(
                                symbol=symbol1,
                                type="LIMIT",
                                side="sell",
                                amount=investment_amount,
                                price=short_enter_price
                            )
                            print(f'{symbol1} : order1 okay')

                            balance = binance.fetch_balance(params={"type": "future"})
                            positions = balance['info']['positions']

                            entry_price = 0.0
                            for position in positions:
                                if position['symbol'] == symbol1.replace('/', ''):
                                    entry_price = float(position['entryPrice'])
                                    break

                            if not entry_price > 0.0:
                                open_orders = binance.fetch_open_orders(
                                    symbol=symbol1
                                )
                                for order in open_orders:
                                    binance.cancel_order(order['id'], symbol1)

                                investment = False
                                investment_amount = None
                                long_or_short = None
                                entering_time = None
                                recent_invest = server_datetime
                                previous_minute = current_minute
                                symbol_details[symbol1]['previous_minute'] = previous_minute
                                symbol_details[symbol1]['entering_time'] = entering_time
                                symbol_details[symbol1]['investment'] = investment
                                symbol_details[symbol1]['long_or_short'] = long_or_short
                                symbol_details[symbol1]['investment_amount'] = investment_amount
                                symbol_details[symbol1]['recent_invest'] = recent_invest
                                continue

                            downprice = entry_price * 0.99 if entry_price <= last_open_price * 0.99 else last_open_price * 0.99

                            print(entry_price)

                            # take profit
                            orders[1] = binance.create_order(
                                symbol=symbol1,
                                type="TAKE_PROFIT",
                                side="buy",
                                amount=investment_amount,
                                price=downprice,
                                params={'stopPrice': downprice}
                            )
                            print('order2 okay')

                            upprice = entry_price * 1.01 if entry_price >= last_open_price * 1.01 else last_open_price * 1.01

                            # stop loss
                            orders[2] = binance.create_order(
                                symbol=symbol1,
                                type="STOP",
                                side="buy",
                                amount=investment_amount,
                                price=upprice,
                                params={'stopPrice': upprice}
                            )
                            print('order3 okay')

                            # 계좌 잔고 업데이트
                            balance = binance.fetch_balance(params={"type": "future"})
                            free_balance = balance['USDT']['free']

                        if long_or_short == 'long':
                            # limit price
                            orders[0] = binance.create_order(
                                symbol=symbol1,
                                type="LIMIT",
                                side="buy",
                                amount=investment_amount,
                                price=long_enter_price
                            )
                            print(f'{symbol1} : order1 okay')

                            balance = binance.fetch_balance(params={"type": "future"})
                            positions = balance['info']['positions']

                            entry_price = 0.0
                            for position in positions:
                                if position['symbol'] == symbol1.replace('/', ''):
                                    entry_price = float(position['entryPrice'])
                                    break

                            if not entry_price > 0.0:
                                open_orders = binance.fetch_open_orders(
                                    symbol=symbol1
                                )
                                for order in open_orders:
                                    binance.cancel_order(order['id'], symbol1)

                                investment = False
                                investment_amount = None
                                long_or_short = None
                                entering_time = None
                                recent_invest = server_datetime
                                previous_minute = current_minute
                                symbol_details[symbol1]['previous_minute'] = previous_minute
                                symbol_details[symbol1]['entering_time'] = entering_time
                                symbol_details[symbol1]['investment'] = investment
                                symbol_details[symbol1]['long_or_short'] = long_or_short
                                symbol_details[symbol1]['investment_amount'] = investment_amount
                                symbol_details[symbol1]['recent_invest'] = recent_invest
                                continue

                            upprice = entry_price * 1.01 if entry_price >= last_open_price * 1.01 else last_open_price * 1.01

                            print(entry_price)

                            # take profit
                            orders[1] = binance.create_order(
                                symbol=symbol1,
                                type="TAKE_PROFIT",
                                side="sell",
                                amount=investment_amount,
                                price=upprice,
                                params={'stopPrice': upprice}
                            )
                            print('order2 okay')

                            downprice = entry_price * 0.99 if entry_price <= last_open_price * 0.99 else last_open_price * 0.99

                            # stop loss
                            orders[2] = binance.create_order(
                                symbol=symbol1,
                                type="STOP",
                                side="sell",
                                amount=investment_amount,
                                price=downprice,
                                params={'stopPrice': downprice}
                            )
                            print('order3 okay')

                            # 계좌 잔고 업데이트
                            balance = binance.fetch_balance(params={"type": "future"})
                            free_balance = balance['USDT']['free']

                if previous_minute is not None and current_minute != previous_minute and symbol1 == 'YFI/USDT':
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


            except Exception as e:
                print(f"An error occurred: {e}")
                previous_minute = current_minute
                symbol_details[symbol1]['previous_minute'] = previous_minute
                symbol_details[symbol1]['entering_time'] = entering_time
                symbol_details[symbol1]['investment'] = investment
                symbol_details[symbol1]['long_or_short'] = long_or_short
                symbol_details[symbol1]['investment_amount'] = investment_amount
                symbol_details[symbol1]['recent_invest'] = recent_invest
                continue

        # API 호출 제한을 피하기 위해 약간의 딜레이를 주는 것이 좋음
        time.sleep(0.5)


    except Exception as e:
        print(f"An error occurred: {e}")
        time.sleep(0.5)
        continue

