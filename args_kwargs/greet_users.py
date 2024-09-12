def greet_users(*users, Initial_greeting = 'hello ', final_greeting =''):
  for user in users:
    print(f"{Initial_greeting}{user}{final_greeting}")
        
greet_users('Harry', 'Rony', 'Hermioni')
greet_users('Jack', 'Jhon', 'Marc', Initial_greeting = "Hey ", final_greeting = ", what'sup?")