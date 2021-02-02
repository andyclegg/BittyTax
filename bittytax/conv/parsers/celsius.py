# -*- coding: utf-8 -*-
# (c) Nano Nano Ltd 2020

from decimal import Decimal
import datetime
import dateutil.tz

from ..out_record import TransactionOutRecord
from ..dataparser import DataParser
from ..exceptions import UnexpectedTypeError

WALLET = "Celsius"

def parse_celsius(data_row, parser, _filename):
    in_row = data_row.in_row
    data_row.timestamp = datetime.datetime.strptime(in_row[1], '%B %d, %Y %I:%M %p').replace(tzinfo=dateutil.tz.UTC)

    if in_row[2] in ("referred_award", "promo_code_reward"):
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_INCOME,
                                                 data_row.timestamp,
                                                 buy_quantity=Decimal(in_row[4]),
                                                 buy_asset=in_row[3],
                                                 wallet=WALLET)
    elif in_row[2] == "deposit":
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_DEPOSIT,
                                                 data_row.timestamp,
                                                 buy_quantity=Decimal(in_row[4]),
                                                 buy_asset=in_row[3],
                                                 wallet=WALLET)
    elif in_row[2] == "interest":
        data_row.t_record = TransactionOutRecord(TransactionOutRecord.TYPE_INTEREST,
                                                 data_row.timestamp,
                                                 buy_quantity=Decimal(in_row[4]),
                                                 buy_asset=in_row[3],
                                                 wallet=WALLET)
    # todo - withdrawal
    else:
        raise UnexpectedTypeError(2, parser.in_header[2], in_row[2])

DataParser(DataParser.TYPE_WALLET,
           "Celsius",
           ['Internal id', ' Date and time', ' Transaction type', ' Coin type',
           ' Coin amount', ' USD Value', ' Original Interest Coin',
           ' Interest Amount In Original Coin', ' Confirmed'],
           worksheet_name="Celsius",
           row_handler=parse_celsius)
