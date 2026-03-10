
""" 
age: int | None = None 
means age is either int or None


type alias: new name for existign type
for example, instead of ahaving a complex type retun like dict[str, str|int|None]
we generate an alias fr that type: User

useful to have code readable, but does not prevent us to have 

"""
# type before the alias directly specifies its an alias
# apparently this could lead to conflicts or confusions since RGB and HSL are similar...
type User = dict[str, str | int| None] #Syntax python 3.12
type RGB = tuple[int, int, int]
type HSL = tuple[int, int, int]

# therefore we can use New type from typing module

from typing import NewType
#Either we use NewType to set the types
RGB_n = NewType("RGB_n", tuple[int, int, int])
HSL_n = NewType("HSL_n", tuple[int, int, int])

# or we use alias where we specify completely the posibility of the type
type User_n = dict[str, str | int | None | RGB_n]

# However, this User_n type can get very complex and also can lead to error beucase it 
# doesn't define which type is each key, its ambiguos.
# Therefore, we can set the type of each key using TypedDict

from typing import TypedDict
# Even though it looks like a class, its just a type
class User_t(TypedDict):
    first_name : str
    last_name : str
    age: int | None
    favorite_color: RGB_n | None

from dataclasses import dataclass

@dataclass
class User_class():
    first_name : str
    last_name : str
    email : str
    age: int | None = None
    favorite_color: RGB_n | None = None
    
def create_user(first_name : str, 
                last_name:str, 
                age: int | None = None,
                favorite_color: RGB_n | None=None,
                ) -> User_t:
    
    email = f"{first_name.lower()}_{last_name.lower()}@gmail.com"

    return {
        "first_name": first_name,
        "first_name": last_name,
        "email": email,
        "age": age,
        "favorite_color" : favorite_color
    }
    
    
def create_user_second(first_name : str, 
                last_name:str, 
                age: int | None = None,
                favorite_color: RGB_n | None=None,
                ) -> User_class:
    
    email = f"{first_name.lower()}_{last_name.lower()}@gmail.com"

    return User_class(
        first_name= first_name,
        last_name= last_name,
        email=email,
        age=age,
        favorite_color=favorite_color
    )

name: str = "pandi"
last_name :str = "ceron"
age : int = "9"
user1: dict = create_user(name, last_name,favorite_color=RGB_n((10,20,36)))
user2: dict = create_user("rocco", "elLoco",favorite_color=RGB_n((10,20,36)))
print(user1)

import random
from typing import Any

# Use generics (Any) when working with external data or invalidated data
# where we dont know the data type

# what the problem here? we loose mypy functionality, because its generic,
# we dont know that rando_user is type User... so, generic use TypeVar 
def random_choice(items: list[Any]) -> Any:
    return random.choice(items)

users = [user1, user2]
rando_user = random_choice(users)

# random choice is using generic type var
# we are passing a list of a specific type and return that same type
# consistency, same type...
# and we recover autocomplition habilities of IDE
def random_choice_g[T](items: list[T]) -> T:
    return random.choice(items)

user3 = create_user_second("pepita", "perez", 25)
user4 = create_user_second("conchita", "lopez", 15)
users_new = [user3, user4]
rando_user_g = random_choice_g(users_new)
rando_user_g.age
print(rando_user_g)

# Best practice:
# inputs: generic
# outputs: specific


