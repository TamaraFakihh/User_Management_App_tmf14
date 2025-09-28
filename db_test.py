from database import insert_user, get_users
u = {
    "name": "Tamara Fakih", 
    "email": "tmf14@gamil.com", 
    "phone": "067765434567",
    "address": "Hamra Street, Beirut", 
    "country": "Lebanon" 
}
print(insert_user(u))

