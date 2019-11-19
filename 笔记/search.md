```
#!/usr/bin/env python3

def search(original_items, key):
    for index, element in enumerate(original_items):
        if element == key: 
            return index
    return -1
        

def binary_search(original_items, key):
    start, end = 0, len(original_items) - 1
    while start <= end:
        mid = (start + end) // 2
        if key < original_items[mid]:
            end = mid - 1
        elif key > original_items[mid]:
            start = mid + 1
        else:
            return mid
    return -1 

def dictionary_search():
    prices = {
        'AAPL': 191.88,
        'GOOG': 1186.96,
        'IBM': 149.24,
        'ORCL': 48.44,
        'ACN': 166.89,
        'FB': 208.09,
        'SYMC': 21.29
    }

    price = {key:value for key,value in prices.items() if value > 100 }
    return price

if __name__ == "__main__":
    #item = [ x for x in range(9) ]
    print(dictionary_search())
```

