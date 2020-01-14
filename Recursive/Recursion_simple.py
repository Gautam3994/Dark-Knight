def rescursive_function(n):
    if n == 1:
        return 1
    return n * rescursive_function(n-1)


value = rescursive_function(5)
print(value)
