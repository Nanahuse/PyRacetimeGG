# PyRacetimeGG
This is wrapper library of racetime.gg Public API endpoints. ([Link API document](https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints))  
This library has the following features.
  
* Object-mapping style wrapper. Data automatically fetching when it is needed. And store the data in a cache to accelerate subsequent access.
* Complete type information. Autocomplete is work well at your editor.


Please refer to the [Test Code](https://github.com/Nanahuse/PyRacetimeGG/tree/main/test) for how to use. 


```python
from pyracetimegg import RacetimeGGAPI
api = RacetimeGGAPI()
user = api.search_user(name="Nanahuse")[0]
user.past_race[0].started_at
```    

# index
- [install](#install)
- [functions](#functions)
- [How to know id or slug](#how-to-know-id-or-slug)

# install
```
pip install git+https://github.com/Nanahuse/PyRacetimeGG
```

# functions
## fetch_user
by user_id    
https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#user-data

## fetch_category
by category slug  
https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#category-detail

## fetch_race
by race slug  
https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#race-detail

## search_user
by name or/and discriminator  
(name:head match search)  
https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#user-search

## search_user_by_term
name partial match serch  
https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#user-search

# How to know id or slug
## How to know user id
1. Check user page URL ( e.g. https://racetime.gg/user/xldAMBlqvY3aOP57 )
1. The string after /user/ is user ID ( e.g. xldAMBlqvY3aOP57)

## How to know Category slug
In racetime.gg, Game title is called "Category".  
"slug" is an identifier for "Category".  
In many cases, it is an abbreviation using the first letter of the game title.
1. Check category page URL ( e.g. https://racetime.gg/smw )
1. The last string is category slug ( e.g. swm).

## How to know race slug
Every race has a separate identifier called slug
It is a form of two words and a four-digit number joined by a hyphen. (word-word-1234)

1. Check race page URL ( e.g. https://racetime.gg/smw/comic-baby-9383 )
2. The last string is race slug ( e.g. comic-baby-9383).

