# SuperPy Documentation

## Introduction

SuperPy is a command-line tool designed to manage inventory and generate reports for a large supermarket chain. This documentation provides an overview of the SuperPy tool, its functionality, and how to use it effectively.

## Features

SuperPy offers the following features:

1. **Inventory Management**: Keep track of the supermarket's product inventory, including product names, quantities, purchase prices, and expiration dates.

2. **Buying Products**: Add new products to the inventory by specifying the product name, purchase price, and expiration date.

3. **Selling Products**: Record product sales by specifying the product name and selling price.

4. **Dynamic Date Tracking**: SuperPy tracks the current date, allowing reports to be generated for specific dates and the ability to advance the date for simulation purposes.

5. **Reports**: Generate reports on various aspects of the inventory, including the current inventory, revenue, and profit.

6. **Data Export**: Export selected data from SuperPy to CSV files for further analysis or integration with other systems.

7. **External Module Integration**: SuperPy supports the use of external modules such as Rich for improved application output and Matplotlib for data visualization.

## Usage Guide

SuperPy provides a user-friendly command-line interface with clear descriptions of each argument. Here are some example commands:

```
python super.py buy --product-name orange --price 0.8 --expiration-date 2020-01-01
```

This command adds the product "orange" to the inventory with a purchase price of 0.8 and an expiration date of January 1, 2020.

```
python super.py report inventory --now
```

This command generates a report of the current inventory, including product names, quantities, purchase prices, and expiration dates.

For a complete list of available commands and their descriptions, refer to the SuperPy tool's `--help` section.

## Technical Elements

The SuperPy implementation includes several notable technical elements:

1. **Dynamic Tracking of Current Date**: SuperPy uses a text file to store and update the current date, allowing accurate simulation of time passage.

2. **Incremental ID Generation for Records**: Each new record added to the inventory or sales data is assigned a unique ID, ensuring proper identification and matching of records.

3. **CSV File Handling with the csv Module**: SuperPy utilizes the `csv` module for efficient reading, writing, and manipulation of data stored in CSV files.

For detailed information on these technical elements and their benefits, refer to the Technical Elements section in the SuperPy documentation.

## Conclusion

SuperPy is a powerful command-line tool for inventory management and reporting. With its intuitive command-line interface, dynamic date tracking, and robust data handling capabilities, SuperPy offers a reliable and efficient solution for supermarket inventory management.
