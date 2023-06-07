# PyRacetimeGG
This is wrapper library of racetime.gg Public API endpoints.  
Please refer to the following documents
* racetime.gg API Document  
  https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints  
  ("All races" is not implemented in this library)

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
get -> https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#user-data

## fetch_category
by category slug
get -> https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#category-detail

## fetch_race
by race slug
get -> https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#race-detail

## fetch_category_leaderboard
by category slug
get -> https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#category-leaderboards

## fetch_past_user_races
by user_id
get -> https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#past-user-races

## fetch_past_user_races_show_entrants
by user_id 
(option show_entrants=yes)
https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#past-user-races

## fetch_past_category_races
by category slug
get -> https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#past-category-races

## fetch_past_category_races_show_entrants
by category slug, get race outline & race entrants
(option show_entrants=yes)
get -> https://github.com/racetimeGG/racetime-app/wiki/Public-API-endpoints#past-category-races

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
Every race has a separate identifier called slug as well as "Category"  
It is a form of two words and a four-digit number joined by a hyphen. (word-word-1234)

1. Check race page URL ( e.g. https://racetime.gg/smw/comic-baby-9383 )
1. The last string is race slug ( e.g. comic-baby-9383).


# Tips
## Connect other racetimeGG site
All fetch function have a site_url argument.
When you connect other racetimeGG site, use site_url argument. 

# Tips
## Request Throttle
This library has a request throttle (default 10[/s])
When you change request limit, use following code.
```python
from pyracetimegg import REQUEST_THROTTLE
REQUEST_THROTTLE.set_request_throttling_per_second(number: int)
```