[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# PyRacetimeGG
This is wrapper library of racetime.gg Public API endpoints.   
[API document](https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints)

This library has the following features.
* Object-mapping style wrapper. Data automatically fetching when it is needed. And store the data in cache.
* Fully type information. Autocomplete is work well at your editor.
* Thread safe


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
- [Tips](#tips)

# install
```
pip install pyracetimegg
```
[PyPI pyracetimegg](https://pypi.org/project/pyracetimegg/)

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

## fetch_by_url
get data instance by url.  
user page, race page, category page url can be use.

## search_user
by name or/and discriminator  
(name:head match search)  
https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#user-search

## search_user_by_term
name partial match serch  
https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#user-search


# Tips
## Update data or manage fetch timing
'load' method will be useful, when you'd like to get latest data or manage fetch timing.
User, Category, Race, PastRace have load.


## How to know id or slug
### How to know user id
1. Check user page URL ( e.g. https://racetime.gg/user/xldAMBlqvY3aOP57 )
1. The string after /user/ is user ID ( e.g. xldAMBlqvY3aOP57)

### How to know Category slug
In racetime.gg, Game title is called "Category".  
"slug" is an identifier for "Category".  
In many cases, it is an abbreviation using the first letter of the game title.
1. Check category page URL ( e.g. https://racetime.gg/smw )
1. The last string is category slug ( e.g. swm).

### How to know race slug
Every race has a separate identifier called slug
It is a form of two words and a four-digit number joined by a hyphen. (word-word-1234)

1. Check race page URL ( e.g. https://racetime.gg/smw/comic-baby-9383 )
2. The last string is race slug ( e.g. comic-baby-9383).

