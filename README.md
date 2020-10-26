# Battery Backend

Api documentation is located on ```/api/docs``` when runned.

## Scripts
#### Debug
```docker-compose up web```

Runs on ```localhost:5000```.
#### Run tests
```docker-compose up --build tests```

#### Production
```docker-compose -f docker-compose.prod.yml up --build```

Uses 3 workers on gunicorn and Nginx for reverse proxy, serving static files and load balancing.

###### Info

Website is located in ```/nginx/static```. Can be viewed on ```localhost/static``` when ran.

**Warning** - In ```script.js``` we need to change the ```urlPrefix``` variable for production.


## Migrations

Run migrations when server is running

```docker-compose exec web flask migrate```

```docker-compose exec web flask upgrade```

## ToDo

Just some tasks that could be implemented in the feature

- Getting voltage for each cell
- Add tests for routes, not only services
- Add ```.prod``` environment files to ```.gitignore```
- Try_to_commit add to ```common_functions.py``` file and refactor services
- (website) Fix form bug on when modals are active when **enter** key is clicked
- (website) Refresh Charge info after **End Charge**
- Refactor validators with Marshmallow schemas