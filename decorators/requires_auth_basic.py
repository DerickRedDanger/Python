auth_data= {'user1': True, 'user2': False}

def Requires_auth(auth_data):

    def decorator(function):

        def wrapper(user, *args, **kwargs):
            if user in auth_data and auth_data[user]:
                return function(user, *args, **kwargs)
            
            else:
                print(f'User is not authorized')
                return None
            
        return wrapper
    
    return decorator



@Requires_auth(auth_data)
def sensitive_function(user, data):
    print(f"Sensitive data for {user}: {data}")

sensitive_function("user1", "some data")
sensitive_function("user2", "some data")