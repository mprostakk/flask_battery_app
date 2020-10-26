# Battery Backend

## Live demo 

Go visit the live 
[Dashboard](http://178.128.44.159/static).

Checkout out example API requests in 
[Swagger](http://178.128.44.159/api/doc).


## Contributors 

<div style="padding: 10px;">
<a href="https://github.com/mprostakk">
  <img src="https://github.com/mprostakk.png?size=100" style="border-radius:50%">
</a>

<a href="https://github.com/NorbertOzga">
  <img src="https://github.com/NorbertOzga.png?size=100" style="border-radius:50%">
</a>

<a href="https://github.com/xszym">
  <img src="https://github.com/xszym.png?size=100" style="border-radius:50%">
</a>
</div>


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

Api documentation is located on ```/api/docs``` when runned.

Website is located in ```/nginx/static```. Can be viewed on ```localhost/static``` when ran.

**Warning** - In ```script.js``` we need to change the ```urlPrefix``` variable for production.


## Migrations

Run migrations when server is running

```docker-compose exec web flask migrate```

```docker-compose exec web flask upgrade```
