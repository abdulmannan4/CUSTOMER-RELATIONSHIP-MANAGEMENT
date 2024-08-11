from customers.models import Customer
from faker import Faker
fake =Faker()
def seed_db(n):  
    for i in range(0,n):
        Customer.objects.create(
            name = fake.name(),
            email = fake.email(),
            phone_number=fake.phone_number(),
            address = fake.address())
    
