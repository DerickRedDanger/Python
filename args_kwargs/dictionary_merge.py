def dictionary_merge(*dicts):
    dic=dict()
    for dictionary in dicts:
        for key,value in dictionary.items():
            dic[key] = value
    print(dic)

dict1 = {'a': 'a', 'b': 'b'}
dict2 = {'c': 'c', 'a': 'A'}
dict3 = {'c': 'C', 'b': 'B'}
dictionary_merge(dict1, dict2,)
dictionary_merge(dict1, dict2, dict3)