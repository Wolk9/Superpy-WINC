# Imports
import argparse
import csv
import datetime
import os
from tabulate import tabulate

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.

DATA_DIR = os.path.join(os.getcwd(), "data")
TODAY_FILE = os.path.join(DATA_DIR, "today.txt")
BOUGHT_FILE = os.path.join(DATA_DIR, "bought.csv")
SOLD_FILE = os.path.join(DATA_DIR, "sold.csv")
BOUGHT_HEADER = ["id", "product_name", "buy_date", "buy_price", "expiration_date"]
SOLD_HEADER = ["id", "bought_id", "sell_date", "sell_price"]

# function to create the data files at first
def create_data_files():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    # Create initial CSVs with headers if they don't exist
    if not os.path.exists(BOUGHT_FILE):
        with open(BOUGHT_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(BOUGHT_HEADER)

    if not os.path.exists(SOLD_FILE):
        with open(SOLD_FILE, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(SOLD_HEADER)

# funtion to set the date to work with 
def set_today(date):
    with open(TODAY_FILE, "w") as file:
        file.write(date.strftime("%Y-%m-%d"))
    print("Today's date set to:", date)

# function to get the set fictive day to work with
def get_today():
    if not os.path.exists(TODAY_FILE):
        return datetime.date.today()

    with open(TODAY_FILE, "r") as file:
        today_str = file.read().strip()
    return datetime.datetime.strptime(today_str, "%Y-%m-%d").date()

# function to get the date from the parser to generate the report with.
def get_report_date(args):
    today = get_today()
    if args.report_type == "inventory":
        if args.now:
            return today
        elif args.yesterday:
            return today - datetime.timedelta(days=1)
        elif args.date:
            return datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
    elif args.report_type == "revenue" or args.report_type == "profit":
        if args.today:
            return today
        elif args.date:
            return datetime.datetime.strptime(args.date, "%Y-%m-%d").date()
    return None

# function to advance the fictive date with the parser
def advance_time(days):
    today = get_today()
    new_date = today + datetime.timedelta(days=days)
    set_today(new_date)

# function to buy products. I have added the quantity function.
def buy_product(product_name, price, expiration_date, quantity=1):
    for _ in range(quantity):
        bought_id = get_next_id(BOUGHT_FILE)
        row = [bought_id, product_name, get_today().strftime("%Y-%m-%d"), price, expiration_date]
        with open(BOUGHT_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)
    print(f"Bought {quantity} {product_name}(s)")


# function to sell products.
def sell_product(product_name, price):
    bought_id = find_product_in_stock(product_name)
    if bought_id:
        sold_id = get_next_id(SOLD_FILE)
        row = [sold_id, bought_id, get_today().strftime("%Y-%m-%d"), price]
        with open(SOLD_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)
        print("OK")
    else:
        print("ERROR: Product not in stock.")

# function to get the next ID of a product in the list
def get_next_id(file_path):
    with open(file_path, "r") as file:
        reader = csv.reader(file)
        next(reader) # Skip the header row
        rows = list(reader)  # Read all rows into a list
        if not rows:  # Check if the list is empty
            return 1  # Return 1 as the default ID if there are no rows
        next_id = max(int(row[0]) for row in rows) + 1
    return next_id

# function to get the product in stock if any.
def find_product_in_stock(product_name):
    if row[1] == product_name and not is_product_sold(row[0]):
        return row[0]
    return None

# function to see if a product is sold or not 
def is_product_sold(bought_id, row):
    if row[1] == bought_id:
        return True
    return False


# function to generate the inventory report.
def get_inventory_report():
    inventory_report = []
    with open(BOUGHT_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader) # Skip the header row
        for row in reader:
            if not is_product_sold(row[0], row):
                product_name = row[1]
                found = False
                for item in inventory_report:
                    if item[0] == product_name:
                        item[1] += 1  # Increment quantity for each bought item
                        found = True
                        break
                if not found:
                    inventory_report.append([product_name, 1, float(row[3]), row[4]])
    print(tabulate(inventory_report, headers=["Product Name", "Count", "Buy Price", "Expiration Date"], tablefmt="grid"))
    return inventory_report

# function to generate the revenue report
def get_revenue_report(report_date):
    revenue = 0
    with open(SOLD_FILE, "r") as sold_file:
        reader = csv.reader(sold_file)
        next(reader)  # Skip the header row
        for row in reader:
            sell_date_str = row[2]
            sell_date = datetime.datetime.strptime(sell_date_str, "%Y-%m-%d").date()
            if sell_date == report_date:
                revenue += float(row[3])
    return revenue


# function to generate the profit report
def get_profit_report(date):
    revenue = 0
    cost = 0
    with open(SOLD_FILE, "r") as sold_file:
        reader = csv.reader(sold_file)
        next(reader)  # Skip the header row
        for row in reader:
            sold_date = datetime.datetime.strptime(row[2], "%Y-%m-%d").date()
            if sold_date == date:
                sold_price = float(row[3])
                bought_id = row[1]
                cost += get_buy_price(bought_id)  # Calculate the cost for each sold item
                revenue += sold_price
    return revenue - cost


# function to get the buy price in the bought list
def get_buy_price(bought_id):
    with open(BOUGHT_FILE, "r") as bought_file:
        reader = csv.reader(bought_file)
        next(reader)  # Skip the header row
        for row in reader:
            if row[0] == bought_id:
                return float(row[3])
    return 0.0

# function to get the quantity of a product in the bought list
def get_quantity_bought(bought_id):
    quantity = 0
    with open(BOUGHT_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader) # Skip the header row
        for row in reader:
            if row[0] == bought_id:
                quantity += 1
    return quantity

# function to create a csv file of a list. 
def export_csv(file_name, rows):
    file_path = os.path.join(DATA_DIR, file_name)
    with open(file_path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(rows)
    print(f"Data exported to {file_path}")



def main():
    parser = argparse.ArgumentParser(prog="SuperPy", description="Supermarket Inventory Management")
    subparsers = parser.add_subparsers(dest="command", title="commands")

    parser_set_today = subparsers.add_parser("set_today", help="Set the current date")
    parser_set_today.add_argument("date", help="The date (YYYY-MM-DD) to set as today")

    parser_advance_time = subparsers.add_parser("advance_time", help="Advance the current date")
    parser_advance_time.add_argument("days", type=int, help="The number of days to advance")

    parser_buy = subparsers.add_parser("buy", help="Buy a product")
    parser_buy.add_argument("--product-name", required=True, help="Name of the product")
    parser_buy.add_argument("--price", type=float, required=True, help="Price of the product")
    parser_buy.add_argument("--expiration-date", required=True, help="Expiration date of the product (YYYY-MM-DD)")
    parser_buy.add_argument("--quantity", type=int, default=1, help="Quantity of the product to buy (default is 1)")

    parser_sell = subparsers.add_parser("sell", help="Sell a product")
    parser_sell.add_argument("--product-name", required=True, help="Name of the product")
    parser_sell.add_argument("--price", type=float, required=True, help="Selling price of the product")

    # Report command with sub-parsers for different report types
    parser_report = subparsers.add_parser("report", help="Generate reports")
    subparsers_report = parser_report.add_subparsers(dest="report_type", title="report types")

    # Inventory report
    parser_report_inventory = subparsers_report.add_parser("inventory", help="Generate inventory report")
    parser_report_inventory.add_argument("--now", action="store_true", help="Generate report for today")
    parser_report_inventory.add_argument("--yesterday", action="store_true", help="Generate report for yesterday")

    # Revenue report
    parser_report_revenue = subparsers_report.add_parser("revenue", help="Generate revenue report")
    group_revenue = parser_report_revenue.add_mutually_exclusive_group(required=True)
    group_revenue.add_argument("--today", action="store_true", help="Generate report for today")
    group_revenue.add_argument("--date", help="Generate report for a specific date (YYYY-MM-DD)")

    # Profit report
    parser_report_profit = subparsers_report.add_parser("profit", help="Generate profit report")
    group_profit = parser_report_profit.add_mutually_exclusive_group(required=True)
    group_profit.add_argument("--today", action="store_true", help="Generate report for today")
    group_profit.add_argument("--date", help="Generate report for a specific date (YYYY-MM-DD)")

    args = parser.parse_args()

    create_data_files()

    if args.command == "set_today":
        set_today(datetime.datetime.strptime(args.date, "%Y-%m-%d").date())
    elif args.command == "advance_time":
        advance_time(args.days)
    elif args.command == "buy":
        buy_product(args.product_name, args.price, args.expiration_date, args.quantity)
    elif args.command == "sell":
        sell_product(args.product_name, args.price)
    elif args.command == "report":
        report_date = get_report_date(args)

        if args.report_type == "inventory":
            if report_date:
                inventory_report = get_inventory_report()
                if inventory_report:
                    header = ["Product Name", "Count", "Buy Price", "Expiration Date"]
                    inventory_report.insert(0, header)
                    export_csv("inventory_report.csv", inventory_report)
                else:
                    print("No products in inventory.")
            else:
                parser_report_inventory.print_help()

        elif args.report_type == "revenue":
            if report_date:
                revenue = get_revenue_report(report_date)
                print(f"Revenue for {report_date}: {revenue}")
            else:
                parser_report_revenue.print_help()

        elif args.report_type == "profit":
            if report_date:
                profit = get_profit_report(report_date)
                print(f"Profit for {report_date}: {profit}")
            else:
                parser_report_profit.print_help()

if __name__ == "__main__":
    main()

