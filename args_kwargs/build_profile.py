def build_profile(username, email = None, **kwargs):
    print(f'Username = {username}')
    if email:
        print(f'Email = {email}')
    for key, values in kwargs.items():
        print(f'{key} = {values}')

build_profile('alice', email='alice@example.com', age=30, location='Wonderland')
print()
build_profile('bob', age=25, hobby='chess')
print()
build_profile('charlie', email='charlie@example.com', profession='engineer', city='New York')