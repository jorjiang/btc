BlockchainInfoConfig = {
    "url_header": "https://api.blockchain.info/charts/",
    "ts_charts": ["market-price",
                  "avg-block-size",
                  "n-transactions",
                  "mempool-size",
                  "total-bitcoins",
                  "market-cap",
                  "trade-volume",
                  "blocks-size",
                  "avg-block-size",
                  "n-orphaned-blocks",
                  "n-transactions-per-block",
                  "median-confirmation-time",
                  "hash-rate",
                  "difficulty",
                  "miners-revenue",
                  "transaction-fees",
                  "transaction-fees-usd",
                  "cost-per-transaction-percent",
                  "cost-per-transaction",
                  "n-unique-addresses",
                  "n-transactions",
                  "n-transactions-total",
                  "transactions-per-second",
                  "mempool-count",
                  "mempool-growth",
                  "mempool-size",
                  "utxo-count",
                  "n-transactions-excluding-popular",
                  "n-transactions-excluding-chains-longer-than-100",
                  "output-volume",
                  "estimated-transaction-volume",
                  "estimated-transaction-volume-usd",
                  "my-wallet-n-users"],
    "url_tail": "",
    "time_span": "all",
    "format": "csv"
}

BitinfochartConfig = {
    "url_header": "https://bitinfocharts.com/comparison/bitcoin-",
    "ts_charts": ['transactions',
                  'size',
                  'sentbyaddress',
                  'difficulty',
                  'hashrate',
                  'price',
                  'mining_profitability',
                  'sentinusd',
                  'transactionfees',
                  'median_transaction_fee',
                  'confirmationtime',
                  'marketcap',
                  'transactionvalue',
                  'mediantransactionvalue',
                  'tweets',
                  'google_trends',
                  'activeaddresses',
                  'top100cap'],
    "url_tail": '.html'
}
BtcDataConfig = {
    'blockchaininfo_ts_data_file': '/Users/Jiang.Ji/PycharmProjects/btc/data/blockchaininfo_ts.pkl.z'
}
