# E-Auction Marketplace

> A Web App built using Django that allows users to buy and sell commodities starting on auctions.

[![made-with-django](https://img.shields.io/static/v1?label=Made%20with&message=Django%203.2&color=informational&style=flat&logo=Django)](https://www.djangoproject.com/)
[![maintainer](https://img.shields.io/static/v1?label=Maintainer&message=nishant-nayak&color=green&style=flat&logo=Github)](https://github.com/nishant-nayak)
[![Open Source Love svg1](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)
---

## Features

- Users can register and login through the web interface
![register-img](/assets/img/register.jpg)

- Users can create auction listings, bid on listings and add listings to their watchlist through the web interface
![listing-img](/assets/img/listing.jpg)

- Users can comment on each individual listing
![comment-img](/assets/img/comments.jpg)

## Requirements

- MySQL version 8.0.22 or higher
- Python 3.7.10

## How to Install

1. Clone the repository using the following command:<br>
`git clone https://github.com/nishant-nayak/e-auctions.git`

2. Run the SQL Commands defined in [MySQLInit.sql](/MySQLInit.sql)

3. Install all the necessary Python package requirements by running the following command:<br>
`pip install -r requirements.txt`

4. Set up the [Environment Variables](#environment-variables)

5. Run the following command to make migrations for the database:<br>
`python manage.py makemigrations`

6. Run the following command to migrate changes to the database:<br>
`python manage.py migrate`

7. To run the Django server on localhost port 8000, run the following command:<br>
`python manage.py runserver`

## Environment Variables

The Django Secret Key is stored in a `.env` file within the [auctions](/auctions/) directory. For the project to work, create a file with the name `.env` and enter the following contents:<br>
`SECRET_KEY=django-insecure-wing%@uugqyp#$xf@n1cbd^ep6h2_d*(-9^o$q_qp-2&k)$n)k`

## Contact
[GitHub](https://github.com/nishant-nayak) | [Email](mailto:nishantnayak2001@gmail.com) | [LinkedIn](https://www.linkedin.com/in/nishant-nayak-01/)