# PizzaMart

## Description
A simple Pizza ordering service

### Functions 
* Order pizzas:
	* It should be possible to specify the desired flavors of pizza (margarita, marinara, salami), the number of pizzas and their size (small, medium, large).
    * An order should contain information regarding the customer.
	* It should be possible to track the status of delivery.
    * It should be possible to order the same flavor of pizza but with different sizes multiple times
* Update an order:
	* It should be possible to update the details — flavours, count, sizes — of an order
    * It should not be possible to update an order for some statutes of delivery (e.g. delivered).
	* It should be possible to change the status of delivery.
* Remove an order.
	* Retrieve an order:
	* It should be possible to retrieve the order by its identifier.
* List orders:
	* It should be possible to retrieve all the orders at once.
	* Allow filtering by status / customer.


<br>

### SET DATABSE ENV VARIABLES
.env
```
export POSTGRES_DB=postgres
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=postgres
```

### SET UP APP

This assumes you have docker installed. <br>Run these commands below in your terminal in the directory where `Dockerfile` and `docker-compose.yml` can be found.

`cd PizzaMart`

`virtuanlenv venv`

`source venv/bin/activate`

`source .env`

`docker-compose up --build`


Go to  `http://0.0.0.0:8000/`


### API 
| Function                                   | Request| Command                 |
| ------------------------------------------ | -------| ------------------------|
| `/api/`                                    |`GET`   | API root                |
| `/api/customers`                           |`GET`, `POST`   | List, Add a customer|
| `/api/customers/<int:customer_id>/`         |`GET`, `PUT`, `PATCH`, `DELETE`| Get, Update, Partial Update, Delete a single Customer|
| `/api/orders/`                             |`POST`, `GET`  | Create, List Order            |
| `/api/orders/<int:order_id>/`              |`GET`, `PUT`, `PATCH`, `DELETE`| Get, Update, Partial Update, Delete Order|
| `/api/orders/<int:order_id>/status`        |`GET`   | Get Order delivery status|
| `/api/orders-list/?customer=<int:order_id>&order_status=<STATUS>`|`GET`   | Sort Orders|

<br>

### Documentation
https://documenter.getpostman.com/view/10026788/TzRNDpAV



# Tests
`sudo docker-compose run web python manage.py test`