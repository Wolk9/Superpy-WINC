# SuperPy: Supermarket Inventory Management Tool

SuperPy is a command-line based inventory management tool designed to keep track of supermarket products. It provides features to record buying and selling activities, produce various reports, and maintain the internal date system for managing transactions.

## Features

- **Date Management**: Set and advance the internal date to simulate daily operations.
- **Inventory Control**: Record the buying and selling of products.
- **Reporting**: Generate revenue, profit, and inventory reports.
- **Data Storage**: All transactions are stored in CSV format for easy reference.

## Installation

1. Ensure you have Python 3 installed.
2. Clone or download this repository to your local machine.
3. Navigate to the directory in the command line.
  
## Usage

1. **Set Current Date**:

   python super.py set_today YYYY-MM-DD

2. **Advance Current Date**

   python super.py advance_time <number_of_days>

3. **Buy a Product**

   python super.py buy --product-name "Product Name" --price <buy_price> --expiration-date YYYY-MM-DD --quantity <quantity>

   The --quantity option allows you to specify the quantity of the product to buy (default is 1).

4. **Sell a Product**

   python super.py sell --product-name "Product Name" --price <sell_price>

5. **Generate Reports**:
   - **Inventory Report for Today**:
     python super.py report inventory --now
   - **Inventory Report for Yesterday**:
     python super.py report inventory --yesterday
   - **Revenue Report for Today**:
     python super.py report revenue --today
   - **Revenue Report for a Specific Date**:
     python super.py report revenue --date YYYY-MM-DD
   - **Profit Report for Today**:
     python super.py report profit --today
   - **Profit Report for a Specific Date**:
     python super.py report profit --date YYYY-MM-DD

  The inventory report is created in CSV format with the name inventory_report.csv and displayed 
  with tabulate to the commandline.

## Data Storage

All transaction data is stored in CSV files located in the `data` directory:

- `bought.csv`: Contains details about products bought.
- `sold.csv`: Contains details about products sold.

## Student Author

Martin de Bes
