#Python is static type
#https://www.youtube.com/watch?v=fM4O9bModsE

#Type hints:
""" Annotation that specifies the expected value of a variable, a class attribute, or a function parameter or retun value """

""" 
Type hinting:
aka. annotations
Add type information to function, parameters, retun values
impove readibility, creates self documented code 
python ignores types at runtime, even if its wrong, it wont say anything, they dont enforce anything, they only give us hints

"""

def create_user(first_name:str, last_name:str, age:int) -> dict:
    email = f"{first_name.lower()}_{last_name.lower()}@gmail.com"

    return {
        "first_name": first_name,
        "first_name": last_name,
        "email": email,
        "age": age
    }

user1: dict = create_user("pandi", "ceron", 9)
print(user1)

""" 
Type checking:
static Analyzis of type
External tool, eg. MyPy, checktype missmatch. Helps us to find errors before running, but dont prevent us to run it.
Cant guard dynamic data

"""

""" 

Data validation

at run time, check if data meets our requirements
run time validation, during runtime excecution
validtes types, values, ranges
if it fails, raises validation erorr
data validation existed before type hinting

Can be manual validation, but its hard to maintain, its a lot of code

Therefore, tools like pydantic were created: which uses type hinting for data validation

Not so usefull when we hard code inputs,
mainly used with dynamic data fron other sources, protecting 

API, payload,s external sources
 """

def create_user_data_validation(first_name:str, last_name:str, age:int) -> dict:
    email = f"{first_name.lower()}_{last_name.lower()}@gmail.com"

    # example manual validation
    if not isinstance(first_name, str):
        raise TypeError("First name must be a string")
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")

    return {
        "first_name": first_name,
        "first_name": last_name,
        "email": email,
        "age": age
    }

user2: dict = create_user_data_validation("rocco", "ceron", 6)
print(user2)


from pydantic import validate_call

@validate_call
def create_user_data_validation_pydantic(first_name:str, last_name:str, age:int) -> dict:
    email = f"{first_name.lower()}_{last_name.lower()}@gmail.com"

    # example manual validation
    if not isinstance(first_name, str):
        raise TypeError("First name must be a string")
    if not isinstance(age, int):
        raise TypeError("Age must be an integer")

    return {
        "first_name": first_name,
        "first_name": last_name,
        "email": email,
        "age": age
    }

user3: dict = create_user_data_validation_pydantic("rocco", "ceron", "fff")
print(user3)