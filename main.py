import cv2
import numpy as np
import pytesseract
import pyautogui
import re
import tkinter as tk
from tkinter import ttk
from PIL import Image as PILImage, ImageTk
from datetime import datetime
import os
import time
from tkinter import *
import asyncio


from ib_insync import IB, Stock, MarketOrder, util, Option

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Text Detection App")

        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=1, sticky="nswe")

        left_frame = ttk.Frame(self.root)
        left_frame.grid(row=0, column=0, sticky="nswe")

        right_frame = ttk.Frame(self.root)
        right_frame.grid(row=0, column=2, sticky="nswe")

        self.x, self.y, self.width, self.height = 360, 570, 280, 75

        self.open_trades = {'SPY': False, 'SPX': False, 'AAPL': False, 'TSLA': False, 'AMZN': False, 'MSFT': False,
                            'NVDA': False, 'AMD': False, 'META': False, 'NFLX': False, 'QQQ': False}
        self.opened_trade_details = {'SPY': {}, 'SPX': {}, 'AAPL': {}, 'TSLA': {}, 'AMZN': {}, 'MSFT': {}, 'NVDA': {},
                                     'AMD': {}, 'META': {}, 'NFLX': {}, 'QQQ': {}, 'SQ': {}, 'SHOP': {}, 'BA': {},
                                    'WMT': {}, 'HD': {}, 'COIN': {}}
        # ...

        self.detect_spy = tk.BooleanVar(value=True)
        self.detect_spx = tk.BooleanVar(value=True)
        self.detect_aapl = tk.BooleanVar(value=True)
        self.detect_tsla = tk.BooleanVar(value=True)
        self.detect_amzn = tk.BooleanVar(value=True)
        self.detect_msft = tk.BooleanVar(value=True)
        self.detect_nvda = tk.BooleanVar(value=True)
        self.detect_amd = tk.BooleanVar(value=True)
        self.detect_meta = tk.BooleanVar(value=True)
        self.detect_nflx = tk.BooleanVar(value=True)
        self.detect_qqq = tk.BooleanVar(value=True)
        self.detect_sq = tk.BooleanVar(value=True)
        self.detect_shop = tk.BooleanVar(value=True)
        self.detect_ba = tk.BooleanVar(value=True)
        self.detect_wmt = tk.BooleanVar(value=True)
        self.detect_hd = tk.BooleanVar(value=True)
        self.detect_coin = tk.BooleanVar(value=True)

        self.total_trades = 0

        self.img_label = ttk.Label(main_frame)
        self.img_label.pack()

        self.text_widget = tk.Text(main_frame, width=50, height=5)
        self.text_widget.pack()

        self.detected_label = ttk.Label(main_frame, text="", font=("Helvetica", 16))
        self.detected_label.pack()

        self.total_trades_label = ttk.Label(main_frame, text=f"Total Trades: {self.total_trades}")
        self.total_trades_label.pack()

        self.stocktotrade = tk.Label(left_frame, text="Stocks To Trade:", font=("Helvetica", 16))
        self.stocktotrade.pack(anchor='w')

        self.spy_checkbox = ttk.Checkbutton(left_frame, text="Detect SPY Trades", variable=self.detect_spy)
        self.spy_checkbox.pack(anchor='w')

        self.spx_checkbox = ttk.Checkbutton(left_frame, text="Detect SPX Trades", variable=self.detect_spx)
        self.spx_checkbox.pack(anchor='w')

        self.aapl_checkbox = ttk.Checkbutton(left_frame, text="Detect AAPL Trades", variable=self.detect_aapl)
        self.aapl_checkbox.pack(anchor='w')

        self.tsla_checkbox = ttk.Checkbutton(left_frame, text="Detect TSLA Trades", variable=self.detect_tsla)
        self.tsla_checkbox.pack(anchor='w')

        self.amzn_checkbox = ttk.Checkbutton(left_frame, text="Detect AMZN Trades", variable=self.detect_amzn)
        self.amzn_checkbox.pack(anchor='w')

        self.msft_checkbox = ttk.Checkbutton(left_frame, text="Detect MSFT Trades", variable=self.detect_msft)
        self.msft_checkbox.pack(anchor='w')

        self.nvda_checkbox = ttk.Checkbutton(left_frame, text="Detect NVDA Trades", variable=self.detect_nvda)
        self.nvda_checkbox.pack(anchor='w')

        self.amd_checkbox = ttk.Checkbutton(left_frame, text="Detect AMD Trades", variable=self.detect_amd)
        self.amd_checkbox.pack(anchor='w')

        self.meta_checkbox = ttk.Checkbutton(left_frame, text="Detect META Trades", variable=self.detect_meta)
        self.meta_checkbox.pack(anchor='w')

        self.nflx_checkbox = ttk.Checkbutton(left_frame, text="Detect NFLX Trades", variable=self.detect_nflx)
        self.nflx_checkbox.pack(anchor='w')

        self.qqq_checkbox = ttk.Checkbutton(left_frame, text="Detect QQQ Trades", variable=self.detect_qqq)
        self.qqq_checkbox.pack(anchor='w')

        self.sq_checkbox = ttk.Checkbutton(left_frame, text="Detect SQ Trades", variable=self.detect_sq)
        self.sq_checkbox.pack(anchor='w')

        self.shop_checkbox = ttk.Checkbutton(left_frame, text="Detect SHOP Trades", variable=self.detect_shop)
        self.shop_checkbox.pack(anchor='w')

        self.ba_checkbox = ttk.Checkbutton(left_frame, text="Detect BA Trades", variable=self.detect_ba)
        self.ba_checkbox.pack(anchor='w')

        self.wmt_checkbox = ttk.Checkbutton(left_frame, text="Detect WMT Trades", variable=self.detect_wmt)
        self.wmt_checkbox.pack(anchor='w')

        self.hd_checkbox = ttk.Checkbutton(left_frame, text="Detect HD Trades", variable=self.detect_hd)
        self.hd_checkbox.pack(anchor='w')

        self.coin_checkbox = ttk.Checkbutton(left_frame, text="Detect COIN Trades", variable=self.detect_coin)
        self.coin_checkbox.pack(anchor='w')

        self.detect_button = ttk.Button(left_frame, text="Start Detection", command=self.toggle_detection)
        self.detect_button.pack(anchor='w')

        self.available_funds_label = ttk.Label(main_frame, text="")
        self.available_funds_label.pack()


        self.detecting = False

        self.ib = None
        self.contract = None
        self.connect_ib()

    def get_available_funds(self):
        account_summary = self.ib.accountSummary()
        available_funds = None
        for summary in account_summary:
            if summary.tag == "AvailableFunds":
                available_funds = float(summary.value)
                break
        return available_funds

    def update_available_funds(self):
        available_funds = self.get_available_funds()
        self.available_funds_label.config(text=f"Available Funds: ${available_funds:,.2f}")


    def connect_ib(self):
        self.ib = IB()
        self.ib.connect('127.0.0.1', 7497, clientId=1)
        self.stock_contracts = {'SPY': Stock('SPY', 'SMART', 'USD'),
                                'SPX': Stock('SPX', 'SMART', 'USD'),
                                'AAPL': Stock('AAPL', 'SMART', 'USD'),
                                'TSLA': Stock('TSLA', 'SMART', 'USD'),
                                'AMZN': Stock('AMZN', 'SMART', 'USD'),
                                'MSFT': Stock('MSFT', 'SMART', 'USD'),
                                'NVDA': Stock('NVDA', 'SMART', 'USD'),
                                'AMD': Stock('AMD', 'SMART', 'USD'),
                                'META': Stock('META', 'SMART', 'USD'),
                                'NFLX': Stock('NFLX', 'SMART', 'USD'),
                                'QQQ': Stock('QQQ', 'SMART', 'USD'),
                                'SQ': Stock('SQ', 'SMART', 'USD'),
                                'SHOP': Stock('SHOP', 'SMART', 'USD'),
                                'BA': Stock('BA', 'SMART', 'USD'),
                                'WMT': Stock('WMT', 'SMART', 'USD'),
                                'HD': Stock('HD', 'SMART', 'USD'),
                                'COIN': Stock('COIN', 'SMART', 'USD')}

    def place_order(self, action, quantity, symbol, strike, expiry, option_type):
        option_contract = Option(symbol, expiry, strike, option_type, 'SMART')
        option_contract_details = self.ib.reqContractDetails(option_contract)[0].contract
        order = MarketOrder(action, quantity)
        trade = self.ib.placeOrder(option_contract_details, order)
        self.ib.sleep(1)
        return trade

    def toggle_detection(self):
        if self.detecting:
            self.detecting = False
            self.detect_button.config(text="Start Detection")
        else:
            self.detecting = True
            self.detect_button.config(text="Stop Detection")
            self.root.after(0, self.detect_text)
            self.update_available_funds()

    def detect_text(self):
        if not self.detecting:
            return

        img = pyautogui.screenshot(region=(self.x, self.y, self.width, self.height))
        gray = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2GRAY)
        _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        text = pytesseract.image_to_string(PILImage.fromarray(thresh))

        text = text.replace('¢', 'c')

        self.detected_label.config(text=text)

        bto_match = re.search(r'.*[Bb][TtI][Oo]\s*\d*\s*(SPY|SPX|AAPL|TSLA|AMZN|MSFT|NVDA|AMD|META|NFLX|QQQ|SQ|SHOP|BA|WMT|HD|COIN)\s*\d+([CcPp])', text, re.IGNORECASE)
        if bto_match:
            symbol = bto_match.group(1).upper()

            if (symbol == 'SPY' and self.detect_spy.get() and not self.open_trades['SPY']) or \
                    (symbol == 'SPX' and self.detect_spx.get() and not self.open_trades['SPX']) or \
                    (symbol == 'AAPL' and self.detect_aapl.get() and not self.open_trades['AAPL']) or \
                    (symbol == 'TSLA' and self.detect_tsla.get() and not self.open_trades['TSLA']) or \
                    (symbol == 'AMZN' and self.detect_amzn.get() and not self.open_trades['AMZN']) or \
                    (symbol == 'MSFT' and self.detect_msft.get() and not self.open_trades['MSFT']) or \
                    (symbol == 'NVDA' and self.detect_nvda.get() and not self.open_trades['NVDA']) or \
                    (symbol == 'AMD' and self.detect_amd.get() and not self.open_trades['AMD']) or \
                    (symbol == 'META' and self.detect_meta.get() and not self.open_trades['META']) or \
                    (symbol == 'NFLX' and self.detect_nflx.get() and not self.open_trades['NFLX']) or \
                    (symbol == 'QQQ' and self.detect_qqq.get() and not self.open_trades['QQQ']) or \
                    (symbol == 'SQ' and self.detect_sq.get() and not self.open_trades['SQ']) or \
                    (symbol == 'SHOP' and self.detect_shop.get() and not self.open_trades['SHOP']) or \
                    (symbol == 'BA' and self.detect_ba.get() and not self.open_trades['BA']) or \
                    (symbol == 'WMT' and self.detect_wmt.get() and not self.open_trades['WMT']) or \
                    (symbol == 'HD' and self.detect_hd.get() and not self.open_trades['HD']) or \
                    (symbol == 'COIN' and self.detect_coin.get() and not self.open_trades['COIN']):
                strike_price = re.search(r'[Bb][TtI][Oo]\s*\d*\s*(?:SPY|SPX|AAPL|TSLA|AMZN|MSFT|NVDA|AMD|META|NFLX|QQQ|SQ|SHOP|BA|WMT|HD|COIN)\s*(\d+)[CcPp]', text,
                                     re.IGNORECASE).group(1)
                option_type = re.search(r'[Bb][TtI][Oo]\s*\d*\s*(?:SPY|SPX|AAPL|TSLA|AMZN|MSFT|NVDA|AMD|META|NFLX|QQQ|SQ|SHOP|BA|WMT|HD|COIN)\s*\d+([CcPp])', text,
                                    re.IGNORECASE).group(1)
                expiry_date_match = re.search(
                    r'[Bb][Tt][Oo]\s*\d*\s*(?:SPY|SPX|AAPL|TSLA|AMZN|MSFT|NVDA|AMD|META|NFLX|QQQ|SQ|SHOP|BA|WMT|HD|COIN)\s*\d+[CcPp]\s+((?:\d{4}/)?(?:0?\d)/\d{1,2})',
                    text, re.IGNORECASE)

                if expiry_date_match:
                    expiry_date = expiry_date_match.group(1)
                    expiry_date = datetime.strptime(f"{expiry_date}/2023", "%m/%d/%Y").strftime("%Y%m%d")
                else:
                # Handle the case when the regex pattern does not match
                    return

                self.text_widget.insert("end",f"Trade opened: BTO {symbol} {strike_price}{option_type.lower()} {expiry_date}\n")

            # Place the order
                trade = self.place_order('BUY', 1, symbol, float(strike_price), expiry_date,
                                     option_type.upper())  # Change the quantity as needed
                print(f"Order placed: {trade}")

                self.open_trades[symbol.upper()] = True
                self.opened_trade_details[symbol.upper()] = {'strike_price': strike_price,
                                                         'option_type': option_type.upper(),
                                                         'expiry_date': expiry_date}

        stc_match = re.search(r'[Ss][Tt][Cc]\s*\d*\s*(SPY|SPX|AAPL|TSLA|AMZN|MSFT|NVDA|AMD|META|NFLX|QQQ|SQ|SHOP|BA|WMT|HD|COIN)\s*\d+([CcPp])', text, re.IGNORECASE)
        if stc_match:
            symbol = stc_match.group(1).upper()

            if self.open_trades[symbol]:
                strike_price = re.search(r'[Ss][Tt][Cce]\s*\d*\s*(?:SPY|SPX|AAPL|TSLA|AMZN|MSFT|NVDA|AMD|META|NFLX|QQQ|SQ|SHOP|BA|WMT|HD|COIN)\s*(\d+)[CcPp]', text,
                                         re.IGNORECASE).group(1)
                option_type = re.search(r'[Ss][Tt][Cc]\s*\d*\s*(?:SPY|SPX|AAPL|TSLA|AMZN|MSFT|NVDA|AMD|META|NFLX|QQQ|SQ|SHOP|BA|WMT|HD|COIN)\s*\d+([CcPp])', text,
                                        re.IGNORECASE).group(1)
                expiry_date_match = re.search(
                    r'[Ss][Tt][Cc]\s*\d*\s*(?:SPY|SPX|AAPL|TSLA|AMZN|MSFT|NVDA|AMD|META|NFLX|QQQ|SQ|SHOP|BA|WMT|HD|COIN)\s*\d+[CcPp]\s+((?:\d{4}/)?(?:0?\d)/\d{2})',
                    text, re.IGNORECASE)

                if expiry_date_match:
                    expiry_date = expiry_date_match.group(1)
                    expiry_date = datetime.strptime(f"{expiry_date}/2023", "%m/%d/%Y").strftime("%Y%m%d")
                else:
                    return

                if (self.opened_trade_details[symbol]['strike_price'] == strike_price and
                        self.opened_trade_details[symbol]['option_type'] == option_type.upper() and
                        self.opened_trade_details[symbol]['expiry_date'] == expiry_date):
                    self.text_widget.insert("end",
                                            f"Trade closed: STC {symbol} {strike_price}{option_type.lower()} {expiry_date}\n")

                    trade = self.place_order('SELL', 1, symbol, float(strike_price), expiry_date,option_type.upper())
                    print(f"Order placed: {trade}")
                    self.open_trades[symbol] = False
                    self.total_trades += 1
                    self.total_trades_label.config(text=f"Total Trades: {self.total_trades}")
                    self.update_available_funds()

# Update the image label with the latest screenshot
        img = PILImage.fromarray(np.array(img))
        imgtk = ImageTk.PhotoImage(image=img)
        self.img_label.imgtk = imgtk
        self.img_label.configure(image=imgtk)
        self.root.update()
        self.root.after(100, self.detect_text)
        self.root.update()

def main():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
