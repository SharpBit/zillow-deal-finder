# Zillow Deal Finder

### How it Works
It searches for houses for purchase or rent in a given neighborhood and calculates the difference between the list price and the Zestimate® and recommends the houses with the best value. Property with list prices lower than the Zestimate will appear in green text, and property with list prices above the Zestimate will appear in red.

### Keep in mind
- Just because a list price is lower than a Zestimate or on the lower end of the value range doesn't mean you should purchase it.
- There are many factors into buying a house such as location, taxes, environment, lot size, maintenance costs, property condition, comfortability, etc. Do **not** solely use this tool to make a purchase.
- The 3rd property always needs to "load", therefore we cannot get any data about that property and it is removed.
- This is technically not allowed as Zillow only allows collection of data through one of their APIs, and since they do not have an API to search for property in a neighborhood with specific filters, this scrapes their site to find those properties. However, parts of this project **do** use multiple APIs provided by Zillow. (They also require an end user product on a website and API branding to be located visibly on the website).

### Config structure
Create a file called `config.json`, copy over the text from `config.json.example`, and edit the necessary information.
```
{
    "ZWSID": "Your ZWS-ID you got from registering",
    "neighborhood": "Great Neck, NY",
    "sort": "days",           // sort by parameter: see options below
    "filters": {
        "price_min": 0,       // minimum house price
        "price_max": 1000000, // maximum house price (leave at 0 for no maximum, -1 for rent only)
        "rent_min": 0,        // minimum rent price
        "rent_max": 3000,     // maximum rent price (leave at 0 for no maximum, -1 for purchase only)
        "beds": "2+",         // Number of bedrooms (str) can be i, i+, 0 for studio: from 0-5, or -1 for Any
        "baths": 3,           // Sets minimum number of baths: 0 (Any), 1, 1.5, 2, 3, or 4
        "sqft_min": 1400,     // minimum square footage
        "sqft_max": 3000      // maximum square footage (set to 0 for no maximum)
    }
}
```
**Sort options:**
- "priced" - Sort by price from high to low
- "pricea" - Sort by price from low to high
- "days" - Sort by new
- "beds" - Sort by bedrooms
- "baths" - Sort by bathrooms
- "size" - Sort by square footage
- "lot" - Sort by lot size
- "zest" - Sort by Zestimate price from high to low
- "zesta" - Sort by Zestimate price from low to high


### How to Use
Clone the repo:
```bash
$ git clone https://github.com/SharpBit/zillow-deal-finder
$ cd zillow-deal-finder
```
Install dependencies:
```bash
$ pip install -r requirements.txt
```
Run the file:
```bash
$ python app.py
```

### An Example
Configuration Used: (8/18/19)
```json
{
    "ZWSID": "censored",
    "neighborhood": "Great Neck, NY",
    "sort": "days",
    "filters": {
        "price_min": 600000,
        "price_max": 1000000,
        "rent_min": 2000,
        "rent_max": 4000,
        "beds": "3+",
        "baths": 3,
        "sqft_min": 2000,
        "sqft_max": 3000
    }
}
```
Output:
```
----------------------------------------------------------------------------------------------------
House for sale at $998,000 - 88 Wooleys Ln, Great Neck, NY 11023
No data

Want to read more?
Home Details: https://www.zillow.com/homedetails/88-Wooleys-Ln-Great-Neck-NY-11023/31067863_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31067863_zpid/
----------------------------------------------------------------------------------------------------
Apartment for rent at $5,000/mo - 27 Olive St, Great Neck, NY 11020
Current Zestimate: $4100 (Last updated: 08/17/2019)
Zestimate change in the last 30 days: $-400
List Price relative to Zestimate: +900
                                           v
Valuation Range: |=========================|
              $2501                   $4961

Want to read more?
Home Details: https://www.zillow.com/homedetails/27-Olive-St-Great-Neck-NY-11020/31098419_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31098419_zpid/
----------------------------------------------------------------------------------------------------
House for rent at $3,950/mo - 57 Berkshire Rd, Great Neck, NY 11023
Current Zestimate: $4870 (Last updated: 08/17/2019)
Zestimate change in the last 30 days: $-13
List Price relative to Zestimate: -920
                 v
Valuation Range: |=========================|
              $4578                   $6428

Want to read more?
Home Details: https://www.zillow.com/homedetails/57-Berkshire-Rd-Great-Neck-NY-11023/31062386_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31062386_zpid/
----------------------------------------------------------------------------------------------------
House for sale at $998,000 - 42 Jayson Ave, Great Neck, NY 11021
Current Zestimate: $946904 (Last updated: 08/17/2019)
Zestimate change in the last 30 days: $-3933
List Price relative to Zestimate: +51096
                                           v
Valuation Range: |=========================|
              $899559                   $994249

Want to read more?
Home Details: https://www.zillow.com/homedetails/42-Jayson-Ave-Great-Neck-NY-11021/31069745_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31069745_zpid/
----------------------------------------------------------------------------------------------------
House for sale at $995,000 - 7 Edgewood Pl, Great Neck, NY 11024
Current Zestimate: $953803 (Last updated: 08/17/2019)
Zestimate change in the last 30 days: $-40617
List Price relative to Zestimate: +41197
                                        v
Valuation Range: |=========================|
              $906113                   $1001493

Want to read more?
Home Details: https://www.zillow.com/homedetails/7-Edgewood-Pl-Great-Neck-NY-11024/31064142_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31064142_zpid/
----------------------------------------------------------------------------------------------------
For sale by owner at $799,999 - 79 Susquehanna Ave, Great Neck, NY 11021
Current Zestimate: $1256601 (Last updated: 08/17/2019)
Zestimate change in the last 30 days: $-24591
List Price relative to Zestimate: -456602
                 v
Valuation Range: |=========================|
              $1093243                   $1407393

Want to read more?
Home Details: https://www.zillow.com/homedetails/79-Susquehanna-Ave-Great-Neck-NY-11021/31069200_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31069200_zpid/
----------------------------------------------------------------------------------------------------
House for sale at $855,000 - 8 Windsor Rd, Great Neck, NY 11021
Current Zestimate: $875479 (Last updated: 08/17/2019)
Zestimate change in the last 30 days: $-11081
List Price relative to Zestimate: -20479
                        v
Valuation Range: |=========================|
              $831705                   $919253

Want to read more?
Home Details: https://www.zillow.com/homedetails/8-Windsor-Rd-Great-Neck-NY-11021/31068433_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31068433_zpid/
----------------------------------------------------------------------------------------------------
House for sale at $938,000 - 10 Pickwood Ln, Great Neck, NY 11024
Current Zestimate: $904258 (Last updated: 08/17/2019)
Zestimate change in the last 30 days: $-98
List Price relative to Zestimate: +33742
                                       v
Valuation Range: |=========================|
              $859045                   $949471

Want to read more?
Home Details: https://www.zillow.com/homedetails/10-Pickwood-Ln-Great-Neck-NY-11024/31065937_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31065937_zpid/
----------------------------------------------------------------------------------------------------
House for sale at $999,000 - 25 Willow Ln, Great Neck, NY 11023
Current Zestimate: $964876 (Last updated: 08/17/2019)
Zestimate change in the last 30 days: $46016
List Price relative to Zestimate: +34124
                                      v
Valuation Range: |=========================|
              $916632                   $1013120

Want to read more?
Home Details: https://www.zillow.com/homedetails/25-Willow-Ln-Great-Neck-NY-11023/31065642_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31065642_zpid/
----------------------------------------------------------------------------------------------------
House for sale at $798,000 - 1 Shadow Ln, Great Neck, NY 11021
Current Zestimate: $771617 (Last updated: 08/17/2019)
Zestimate change in the last 30 days: $-17138
List Price relative to Zestimate: +26383
                                      v
Valuation Range: |=========================|
              $733036                   $810198

Want to read more?
Home Details: https://www.zillow.com/homedetails/1-Shadow-Ln-Great-Neck-NY-11021/31068474_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31068474_zpid/
----------------------------------------------------------------------------------------------------
House for sale at $948,000 - 2 Sheffield Rd, Great Neck, NY 11021
Current Zestimate: $916653 (Last updated: 08/17/2019)
Zestimate change in the last 30 days: $-646
List Price relative to Zestimate: +31347
                                      v
Valuation Range: |=========================|
              $870820                   $962486

Want to read more?
Home Details: https://www.zillow.com/homedetails/2-Sheffield-Rd-Great-Neck-NY-11021/31066245_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31066245_zpid/
----------------------------------------------------------------------------------------------------
House for sale at $999,999 - 200 Overlook Ave, Great Neck, NY 11021
Current Zestimate: $941294 (Last updated: 08/17/2019)
Zestimate change in the last 30 days: $-37208
List Price relative to Zestimate: +58705
                                           v
Valuation Range: |=========================|
              $894229                   $988359

Want to read more?
Home Details: https://www.zillow.com/homedetails/200-Overlook-Ave-Great-Neck-NY-11021/31069188_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31069188_zpid/
----------------------------------------------------------------------------------------------------
House for sale at $950,000 - 35 Valley View Rd, Great Neck, NY 11021
Current Zestimate: $911318 (Last updated: 08/17/2019)
Zestimate change in the last 30 days: $-24152
List Price relative to Zestimate: +38682
                                        v
Valuation Range: |=========================|
              $865752                   $956884

Want to read more?
Home Details: https://www.zillow.com/homedetails/35-Valley-View-Rd-Great-Neck-NY-11021/31068282_zpid/
Comparable Homes: http://www.zillow.com/homes/comps/31068282_zpid/
----------------------------------------------------------------------------------------------------
```