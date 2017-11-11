# Notes

These notes were taken while completeing this challenge. 


## Data Modelling [9/11/17]

I am first going to understand the raw data files and come up with a data model for it.
I've listed the models below, with their source field name and what relationships exist.
I've made some normalizations according to what I think will help build the required API.


### Company

- id (index) - int
- name (company) - str

### Person (Naming based on README spec)

- hash_id (_id) - str
- id (index) - unique int
- guid (guid) - uuid
- has_died (has_died) - bool
- balance (balance) - int (in cents)
- picture_url (picture) - str
- age (age) - int
- eye_color (eyeColor) - str
- name (name) - str
- gender (gender) - ENUM (male, female, other)
- company_id (company_id -> Company.id) - int
- email (email) - str 
- phone (phone) - str (this could be normalised to an int, but seems unneccessary)
- address (address) - str (this could be split up into seperate fields, but unneccessary)
- about (about) - blob
- greeting (greeting) - blob
- registered_at (registered) - datetime 


### PersonTags

- person_id (person_id -> Person.id)
- tag ([tags]) - str (each tag could be put into a Tag table, but seems unneccessary)


### FriendRelationship

- person_1_id (friends.index -> Person.id)
- person_2_id (friends.index -> Person.id)

\* Note: Need a unique index on (person_1_id, person_2_id)


### Food

- id (auto generated) - int
- name ([favouriteFood]) - str (unique)


### FavouriteFood

- person_id (Person.id)
- food_id (Food.id)

\* Note: Need a unique index on (person_id, food_id)


## Technology Used

- Python 3.4+
- Django 1.11
- Django-Rest-Framework
- MySQL

## Import Scripts [9/11/17]

After creating the models and the relevant migrations, I made the import scripts.

The script to import companies was quite straightfoward, however the one for people was more complex.
It required that the data be imported in a specific order to ensure that the constraints in the database
would not break.

A second issue was that some of the people had company references which did not exist in the company table / file.
I simply NULLed out those columns in their rows.

I scanned the data to extract out the unique food items and hand classified them. There were only 8 so it was quite simple.

### Import Order

1. Companies
2. Food
3. Persons
4. Friendships
5. Favourite Foods

## Building the API [10/11/17]

Once the data was in the system, building out the 3 endpoints was fairly straightworward.
I used Django Rest Framework to build the endpoints.

The only tricky part came in writing an optimised query to find mutual friends. I managed to 
solve it with only one query, but it wasn't the most optimised since MySQL does not have INTERSECT.

### Endpoints

- Company Employees - `/companies/api/<ID>/employees`
- Person Details - `/people/api/<ID>`
- Mutual Friends - `/people/api/mutual_friends/<USER1_ID>/<USER2_ID>`
 
 
### Installation

1. Ensure you have python3.4+, MySQL (locally, user=root) and virtualenv installed
2. Clone this repository and `cd` into the root of this directory
3. Run `./setup.sh`. Type in password if you need to, otherwise press enter.
4. To run server - `./runserver.sh`
 
## Final Thoughts

The challenge was straightforward for the most part. Obviously the biggest
time sinks are in understanding the data model, finding the issues with the raw data,
and solving tricky issues with MySQL. 

I was pretty stretched for time to do this task, so I'm sorry if there are some glaring oversights.
I wanted to finish this task by writing a set of unit tests. If you would like me to finish this off, just
send me an email at `ashramesh1992@gmail.com` and ask me :\).
