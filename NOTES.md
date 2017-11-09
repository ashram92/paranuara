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


## Import Scripts [9/11/17]

After creating the models and the relevant migrations, I made the import scripts.

The script to import companies was quite straightfoward, however the one for people was more complex.
It required that the data be imported in a specific order to ensure that the constraints in the database
would not break.

### Import Order

1. Companies
2. Food
3. Persons
4. Friendships
5. Favourite Foods
