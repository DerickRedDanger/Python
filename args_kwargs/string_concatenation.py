def string_concatenation(*arg, separator = ' '):
  strings = [item for item in arg if isinstance(item,(str))]
  result = separator.join(strings)
  print(result)
  
string_concatenation(1, 2, 3, 4, 5, 6, 7, 8, 9, 10,'a', 'b', 'c', 0.14, 0.57,)
string_concatenation(1, 2, 3, 4, 5, 6, 7, 8, 9, 10,'a', 'b', 'c', 0.14, 0.57, separator = ',')