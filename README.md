# 🍽️ FoodFusion

### Full-Stack Online Food Ordering System

FoodFusion is a full-stack web-based online food ordering platform developed using **Python and Django**. It provides a complete digital food-ordering workflow where customers can register, browse food items, add items to their cart, place orders, track order history, and share food reviews and ratings.

The system also provides dedicated functionality for restaurants and an administrative dashboard for monitoring users, restaurants, food items, orders, reviews, and revenue-related statistics.

🌐 **Live Demo:** [FoodFusion](https://foodfusion-ilgu.onrender.com)

---

## 📌 Project Overview

FoodFusion is designed to simplify the online food ordering process by connecting customers, restaurants, and administrators through a centralized web application.

The application follows a role-based approach:

* 👤 **Customers** can browse food, manage their cart, place orders, and submit reviews.
* 🏪 **Restaurants** can manage food items and monitor incoming orders.
* 🛠️ **Administrators** can manage the platform and view operational analytics.

The project also includes authentication, order management, food reviews and ratings, and an analytics-oriented administration dashboard.

---

## ✨ Key Features

### 👤 Customer Features

* Customer registration and login
* Secure authentication
* Customer account management
* Browse available food items
* View food details and prices
* Add food items to cart
* Update item quantities
* Remove items from cart
* Checkout and place orders
* View order history
* Track order status
* Submit food reviews
* Rate food items from 1–5 stars

### 🏪 Restaurant Features

* Restaurant registration and authentication
* Restaurant profile management
* Add food items
* Upload food images
* Manage menu items
* View customer orders
* Update order status
* Monitor restaurant-related activity

### 🛒 Cart & Ordering

* Add products to cart
* Quantity management
* Automatic subtotal calculation
* Automatic total calculation
* Checkout form
* Delivery address collection
* Order creation
* Order history
* Order status tracking

### ⭐ Reviews & Ratings

FoodFusion includes a food review and rating system where customers can:

* Give a rating from **1 to 5 stars**
* Write comments about food
* View reviews associated with food items
* Display food ratings within the menu interface

### 📊 Admin Dashboard

The administrative dashboard provides an overview of important application statistics, including:

* Total customers
* Total restaurants
* Total food items
* Total reviews
* Total orders
* Revenue information
* Order-status distribution
* Rating distribution
* Restaurant statistics
* Top food items
* Recent orders
* Recent reviews

This provides administrators with a centralized view of platform activity.

---

## 🛠️ Technology Stack

### Backend

* **Python**
* **Django**
* Django Authentication
* Django ORM
* SQLite for local development

### Frontend

* HTML5
* CSS3
* JavaScript
* Django Templates

### Database

* SQLite

### Additional Technologies

* Pillow
* django-phonenumber-field
* WhiteNoise
* Gunicorn
* dj-database-url
* PostgreSQL support for production configuration

### Deployment

* Render

---

## 🏗️ Application Architecture

```text
                    ┌──────────────────────┐
                    │      Customer        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      FoodFusion      │
                    │    Django Web App     │
                    └──────────┬───────────┘
                               │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
       ┌────────────┐   ┌────────────┐   ┌────────────┐
       │   Menu     │   │   Orders   │   │  Reviews   │
       └────────────┘   └────────────┘   └────────────┘
              │                │                │
              └────────────────┼────────────────┘
                               ▼
                    ┌──────────────────────┐
                    │       Database       │
                    │       SQLite         │
                    └──────────────────────┘

       ┌──────────────────┐       ┌──────────────────┐
       │    Restaurant    │──────▶│ Admin Dashboard  │
       └──────────────────┘       └──────────────────┘
```

---

## 👥 User Roles

| Role              | Main Responsibilities                                                |
| ----------------- | -------------------------------------------------------------------- |
| 👤 Customer       | Register, login, browse food, manage cart, place orders, review food |
| 🏪 Restaurant     | Manage food items and process customer orders                        |
| 🛠️ Administrator | Manage application data and monitor platform analytics               |

---

## 📁 Project Structure

```text
FoodFusion/
│
├── Food Ordering/
│   │
│   ├── foodOrderSystem/
│   │   │
│   │   ├── customer/
│   │   │   ├── migrations/
│   │   │   ├── templates/
│   │   │   ├── admin.py
│   │   │   ├── admin_views.py
│   │   │   ├── models.py
│   │   │   ├── urls.py
│   │   │   └── views.py
│   │   │
│   │   ├── menu/
│   │   │
│   │   ├── order/
│   │   │
│   │   ├── restaurant/
│   │   │
│   │   ├── foodOrderSystem/
│   │   │   ├── settings.py
│   │   │   ├── urls.py
│   │   │   ├── wsgi.py
│   │   │   └── asgi.py
│   │   │
│   │   ├── manage.py
│   │   └── db.sqlite3
│   │
│   └── requirements.txt
│
├── build.sh
├── render.yaml
├── .gitignore
├── Documentation.docx
├── Project PPT.pptx
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone https://github.com/Nithin-marri68/FoodFusion.git
```

### 2. Navigate to the project

```bash
cd FoodFusion
cd "Food Ordering"
cd foodOrderSystem
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

#### Windows PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

#### Windows Command Prompt

```cmd
venv\Scripts\activate
```

### 5. Install dependencies

```bash
pip install -r ../requirements.txt
```

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create an administrator account

```bash
python manage.py createsuperuser
```

Follow the prompts to create the admin account.

### 8. Collect static files

```bash
python manage.py collectstatic --noinput
```

### 9. Run the development server

```bash
python manage.py runserver
```

Open the application at:

```text
http://127.0.0.1:8000/
```

---

## 🔐 Authentication

FoodFusion provides authentication for different types of users.

### Customer

Customers can:

```text
Register
   ↓
Login
   ↓
Browse Menu
   ↓
Add Food to Cart
   ↓
Checkout
   ↓
Place Order
   ↓
View Orders
   ↓
Review Food
```

### Restaurant

Restaurants can authenticate separately and manage their food items and incoming orders.

### Administrator

The Django administration interface provides centralized management of application data.

---

## 🛒 Ordering Workflow

The typical customer workflow is:

```text
Customer Registration
        ↓
Customer Login
        ↓
Browse Food Menu
        ↓
Select Food
        ↓
Add to Cart
        ↓
Review Cart
        ↓
Checkout
        ↓
Enter Delivery Information
        ↓
Place Order
        ↓
Order Confirmation
        ↓
Order History
        ↓
Order Status Tracking
```

---

## ⭐ Food Review Workflow

After interacting with food items, customers can provide feedback through the review system.

```text
Customer
   ↓
Select Food
   ↓
Give Rating
   ↓
Write Comment
   ↓
Submit Review
   ↓
Review Stored
   ↓
Rating Displayed
```

Ratings are represented on a **1–5 star scale**.

---

## 📊 Admin Analytics

FoodFusion includes an analytics-oriented administration dashboard.

The dashboard can provide information such as:

```text
                    ADMIN DASHBOARD
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
        ▼                  ▼                  ▼
    Customers         Restaurants          Food Items
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                           ▼
                        Orders
                           │
                ┌──────────┴──────────┐
                ▼                     ▼
          Order Status             Revenue
                │
                ▼
             Reviews
                │
                ▼
         Rating Distribution
```

---

## 🌐 Live Deployment

FoodFusion is deployed using **Render**.

### Live Application

https://foodfusion-ilgu.onrender.com

### Deployment Configuration

The project includes:

```text
render.yaml
build.sh
```

The build process performs:

```text
Install Python dependencies
        ↓
Collect static files
        ↓
Apply Django migrations
        ↓
Start Gunicorn
        ↓
Run FoodFusion
```

---

## 🖼️ Screenshots

Add screenshots of the major application pages to the repository using a `screenshots` folder.

Recommended screenshots:

```text
screenshots/
├── home.png
├── menu.png
├── reviews.png
├── cart.png
├── orders.png
├── restaurant-dashboard.png
├── restaurant-orders.png
└── admin-dashboard.png
```

Then they can be displayed in this README using:

```markdown
## 📸 Screenshots

### Home Page

![FoodFusion Home](screenshots/home.png)

### Menu

![FoodFusion Menu](screenshots/menu.png)

### Cart

![FoodFusion Cart](screenshots/cart.png)

### Orders

![FoodFusion Orders](screenshots/orders.png)

### Admin Dashboard

![FoodFusion Admin Dashboard](screenshots/admin-dashboard.png)
```

---

## 🔒 Security & Validation

FoodFusion incorporates Django's built-in security mechanisms and application-level validation.

Key areas include:

* Django authentication
* CSRF protection
* Password validation
* Session management
* Role-based functionality
* Form validation
* Database-level relationships
* Secure production configuration
* Environment-based secret configuration

Production deployment uses environment variables for important configuration values.

---

## 🚀 Future Enhancements

Planned improvements include:

* 📱 Fully responsive mobile-first UI
* 💳 Online payment gateway integration
* 📍 Real-time order tracking
* 🔔 Order notifications
* 📧 Email notifications
* 🗺️ Delivery location tracking
* 🤖 AI-based food recommendations
* 🔎 Advanced food search and filtering
* ❤️ Wishlist functionality
* 🏪 Enhanced restaurant analytics
* 📈 Advanced sales analytics
* 🗄️ Persistent production database
* ☁️ Persistent cloud media storage

---

## 💡 Future Production Architecture

A production-oriented version can evolve toward:

```text
                  ┌───────────────────┐
                  │   FoodFusion UI   │
                  │ HTML/CSS/JS       │
                  └─────────┬─────────┘
                            │
                            ▼
                  ┌───────────────────┐
                  │ Django Application│
                  │      Backend      │
                  └─────────┬─────────┘
                            │
             ┌──────────────┼──────────────┐
             │              │              │
             ▼              ▼              ▼
        PostgreSQL      Cloud Storage   Payment API
        Database        for Media       Gateway
             │
             ▼
        Analytics &
        Order Data
```

---

## 🧪 Local Development

For development, the project uses SQLite and Django's development server.

Start the application with:

```bash
cd "Food Ordering/foodOrderSystem"
python manage.py runserver
```

For deployment builds:

```bash
./build.sh
```

---

## 📦 Dependencies

The project dependencies are maintained in:

```text
Food Ordering/requirements.txt
```

Major dependencies include:

* Django
* Pillow
* django-phonenumber-field
* phonenumbers
* Gunicorn
* WhiteNoise
* dj-database-url
* psycopg2-binary

Install them using:

```bash
pip install -r "Food Ordering/requirements.txt"
```

---

## 📝 Project Documentation

Additional project documentation is available in the repository:

* `Documentation.docx` — Project documentation
* `Project PPT.pptx` — Project presentation
* `README.md` — Project setup and overview

---

## 👨‍💻 Developer

### Nithin Marri

B.Tech Student | Full-Stack Developer | Python & Django

FoodFusion was developed and maintained as a full-stack web application with a focus on:

* Web application development
* Django backend development
* Database management
* Authentication
* E-commerce workflows
* Order management
* Dashboard analytics
* Deployment

### GitHub

[Nithin-marri68](https://github.com/Nithin-marri68)

### Project Repository

[FoodFusion](https://github.com/Nithin-marri68/FoodFusion)

---

## 📄 License

This project is intended for educational and portfolio purposes.

---

## ⭐ Support

If you find FoodFusion useful or interesting, consider giving the repository a ⭐ on GitHub.

---

### 🍽️ FoodFusion

**Order. Enjoy. Review.**

> Developed and maintained by **Nithin Marri**.
