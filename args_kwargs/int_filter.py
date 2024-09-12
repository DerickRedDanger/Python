def int_filter(*values,operation = None):
  lis =[value for value in values if isinstance(value,(int))]
  result = 1
  if operation == 'sum':
    result = sum(lis)
  elif operation == 'product':
    for value in lis:
      result *= value
  else:
    result = lis
  print(result)

int_filter(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
int_filter(1, 2, 3, 4, 5, 6, 7, 8, 9, 10,'a', 'b', 'c', 0.14, 0.57,)
int_filter(1, 2, 3, 4, 5, 6, 7, 8, 9, 10,'a', 'b', 'c', 0.14, 0.57, operation ='sum')
int_filter(4, 5, 6,'a', 'b', 'c', 0.14, 0.57, operation ='product')