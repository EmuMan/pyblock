import pyblock

def main() -> None:
    print(len(pyblock.get_auctions()))
    bazaar_product = pyblock.get_bazaar_information().product('STOCK_OF_STONKS')
    print(f'{bazaar_product.product_id}: {bazaar_product.buy_price}, {bazaar_product.sell_price}')

if __name__ == '__main__':
    main()
