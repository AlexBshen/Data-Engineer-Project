#  Data Engineering Project

**Author: Luis A. Santiago Andino**


**Institutional Email: luis.santiago102@upr.edu**


**Personal Email: lsanderandino@gmail.com**


## Project Overview ##
This project is a data engineering solution for Venmito, a payment company facilitating transactions among users and participating stores. The purpose of this project is to ingest, clean, match, and analyze client and transaction data from various sources, and provide meaningful insights through a RESTful API.


## Solution Description ##
The project uses Python and Flask to create a RESTful API that serves data from a PostgreSQL database. The solution organizes code into DAOs (Data Access Objects), Handlers, and a central API routing file (app.py). This structure promotes readability, modularity, and ease of maintenance, ensuring that database interactions are separate from application logic.

The API provides CRUD operations and statistical insights for four main entities:

- **Clients**: Information about users and demographics.
- **Promotions**: Client promotion engagement data.
- **Transactions**: Transaction data including item details and revenue insights.
- **Transfers**: Fund transfer data with statistics on activity levels and amounts.
The API also offers statistical endpoints, allowing Venmito to derive insights about user behavior, transaction trends, and promotion engagement.


## Instructions for Running the Code

### Prerequisites

To run this project, you’ll need:
- **Python 3.8+**
- **PostgreSQL** database
- **Packages**: Flask, psycopg2, pandas (for data ingestion)

### Install Dependencies

All required packages are listed in the `requirements.txt` file. To install them, run the following command from the project’s root directory:
```bash
pip install -r requirements.txt
```


### Database Setup

This project uses PostgreSQL, running in a Docker container, for database management. Follow these steps to set up the database:

1. **Login to Docker Hub**:
   - Open your terminal and log in to Docker Hub using the following command:
     ```bash
     docker login
     ```
   - You’ll be prompted to enter your Docker Hub username and password.

2. **Run PostgreSQL in Docker**:
   - Pull the PostgreSQL image from Docker Hub and start a new PostgreSQL container with the following command:
     ```bash
     docker run --name some-postgres -p 5432:5432 -e POSTGRES_PASSWORD=mysecretpassword -d postgres
     ```
   - This command creates a new container named `some-postgres` running PostgreSQL, accessible on port `5432` with the password `mysecretpassword`.
   - Remember you can use your desired info in --name , -e and -d

3. **Connect to the Database**:
   - Use a database management tool, like **DataGrip**, to connect to the PostgreSQL database.
   - Create a new PostgreSQL data source and enter the following credentials:
     - **Host**: `localhost`
     - **Port**: `5432`
     - **User**: `postgres`
     - **Password**: `mysecretpassword`

4. **Create the Tables**:
   - Once connected to the database, use the following SQL commands to create the necessary tables:

     ```sql
     CREATE TABLE Clients (
         client_id SERIAL PRIMARY KEY,
         first_name VARCHAR(255),
         last_name VARCHAR(255),
         telephone VARCHAR(15) UNIQUE,
         email VARCHAR(255) UNIQUE,
         city VARCHAR(100),
         country VARCHAR(100)
         devices (TEXT)
     );

     CREATE TABLE Promotions (
         promotion_id SERIAL PRIMARY KEY,
         client_id INT REFERENCES Clients(client_id),
         promotion TEXT,
         responded BOOLEAN
     );

     CREATE TABLE Transactions (
         transaction_id SERIAL PRIMARY KEY,
         client_id INT REFERENCES Clients(client_id),
         store VARCHAR(255),
         item_name VARCHAR(255),
         price NUMERIC(10, 2),
         price_per_item NUMERIC(10, 2),
         quantity INT
     );

     CREATE TABLE Transfers (
         transfer_id SERIAL PRIMARY KEY,
         sender_id INT REFERENCES Clients(client_id),
         recipient_id INT REFERENCES Clients(client_id),
         amount NUMERIC(10, 2),
         date DATE
     );
     ```

5. **Populate the Tables**:
   - Data for the tables is populated through the code provided in `data/dataInjection.py`.
   - Run this script to populate the tables with sample data. Ensure that the `data` directory contains the necessary files (`people.json`, `transfers.csv`, `transactions.xml`, `promotions.csv`).

6. **Verify the Setup**:
   - Once the tables are created and populated, you can verify the setup by running test queries in DataGrip or by interacting with the API endpoints to retrieve data.

Your database setup is complete, and you’re ready to start the Flask API and interact with the data.



### Running the Flask API

Once the dependencies are installed and the database setup is complete, you can start the Flask API by following these steps:

1. **Navigate to the Project Directory**:
   - Open a terminal and navigate to the root directory of the project:
     ```bash
     cd path/to/your/project
     ```


3. **Start the Flask Development Server**:
   - Run the Flask API with the following command:
     ```bash
     flask run
     ```
   - By default, this will start the server at `http://127.0.0.1:5001`.

4. **Verify the API is Running**:
   - Open a browser or a tool like **Postman** and visit `http://127.0.0.1:5001`. You should see a response indicating the API is live and ready to accept requests.

5. **Access the Endpoints**:
   - You can now interact with the API endpoints as described in the **API Documentation** section. For example:
     ```bash
        http://127.0.0.1:5001/clients
     ```
   - This will return a list of all clients in the database.

The Flask API is now running and ready for use. You can explore various endpoints to interact with the data, perform CRUD operations, and retrieve analytics.


## API Documentation

This section provides an overview of all available endpoints, organized by entity: **Clients**, **Promotions**, **Transactions**, and **Transfers**. Each endpoint includes its HTTP method and description.

### Clients

- **Get All Clients**  
  - **Endpoint**: `GET /clients`  
  - **Description**: Retrieves a list of all clients.

- **Get Client by ID**  
  - **Endpoint**: `GET /clients/<client_id>`  
  - **Description**: Retrieves details of a specific client by `client_id`.

- **Search Clients by Location**  
  - **Endpoint**: `GET /clients/search`  
  - **Description**: Searches for clients by location or country.

- **Add New Client**  
  - **Endpoint**: `POST /clients`  
  - **Description**: Adds a new client to the database.

- **Update Client by ID**  
  - **Endpoint**: `PUT /clients/<client_id>`  
  - **Description**: Updates an existing client's information.

- **Delete Client by ID**  
  - **Endpoint**: `DELETE /clients/<client_id>`  
  - **Description**: Deletes a specific client by `client_id`.

#### Client Demographics

- **Client Count by Country**  
  - **Endpoint**: `GET /clients/demographics/country`  
  - **Description**: Retrieves the count of clients by country.

- **Client Count by City and Country**  
  - **Endpoint**: `GET /clients/demographics/city_country`  
  - **Description**: Retrieves client distribution by city and country.

### Promotions

- **Get All Promotions**  
  - **Endpoint**: `GET /promotions`  
  - **Description**: Retrieves a list of all promotions.

- **Get Promotions by Client**  
  - **Endpoint**: `GET /promotions/<client_id>`  
  - **Description**: Retrieves all promotions for a specific client.

- **Add New Promotion**  
  - **Endpoint**: `POST /promotions`  
  - **Description**: Adds a new promotion for a client.

- **Update Promotion Response**  
  - **Endpoint**: `PUT /promotions/<promotion_id>`  
  - **Description**: Updates the response status of a specific promotion.

- **Delete Promotion**  
  - **Endpoint**: `DELETE /promotions/<promotion_id>`  
  - **Description**: Deletes a promotion by ID.

#### Promotions Statistics

- **Overall Engagement Rate**  
  - **Endpoint**: `GET /promotions/stats/overall_engagement`  
  - **Description**: Retrieves the overall engagement rate for promotions.

- **Engagement Rate by Promotion Type**  
  - **Endpoint**: `GET /promotions/stats/engagement_by_type`  
  - **Description**: Retrieves engagement rates by each promotion type.

- **Non-Responding Clients**  
  - **Endpoint**: `GET /promotions/stats/non_responding_clients`  
  - **Description**: Lists clients who have not responded to any promotions.

- **Top Promotion Types by Responses**  
  - **Endpoint**: `GET /promotions/stats/top_promotion_types`  
  - **Description**: Shows promotion types with the highest number of responses.

### Transactions

- **Get All Transactions**  
  - **Endpoint**: `GET /transactions`  
  - **Description**: Retrieves a list of all transactions.

- **Get Transactions by Client ID**  
  - **Endpoint**: `GET /transactions/<client_id>`  
  - **Description**: Retrieves all transactions associated with a specific client.

- **Add New Transaction**  
  - **Endpoint**: `POST /transactions`  
  - **Description**: Adds a new transaction to the database.

#### Transactions Statistics

- **Total Revenue by Store**  
  - **Endpoint**: `GET /transactions/stats/revenue_per_store`  
  - **Description**: Retrieves total revenue generated by each store.

- **Total Revenue by Item**  
  - **Endpoint**: `GET /transactions/stats/revenue_by_item`  
  - **Description**: Retrieves total revenue by item.

- **Most Sold Items**  
  - **Endpoint**: `GET /transactions/stats/most_sold_items`  
  - **Description**: Lists the most sold items by quantity.

- **Top Clients by Spending**  
  - **Endpoint**: `GET /transactions/stats/top_clients`  
  - **Description**: Lists top clients by total spending.

- **Average Transaction Value**  
  - **Endpoint**: `GET /transactions/stats/average_transaction_value`  
  - **Description**: Shows the average value of transactions.

### Transfers

- **Get All Transfers**  
  - **Endpoint**: `GET /transfers`  
  - **Description**: Retrieves a list of all transfers.

- **Get Transfers by Sender ID**  
  - **Endpoint**: `GET /transfers/<sender_id>`  
  - **Description**: Lists transfers initiated by a specific sender.

- **Add New Transfer**  
  - **Endpoint**: `POST /transfers`  
  - **Description**: Adds a new transfer record.

#### Transfers Statistics

- **Total Transfer Amount by Sender**  
  - **Endpoint**: `GET /transfers/stats/total_amount_by_sender`  
  - **Description**: Shows total transfer amount by each sender.

- **Top Recipients by Received Amount**  
  - **Endpoint**: `GET /transfers/stats/top_recipients`  
  - **Description**: Lists recipients who have received the highest total amounts.

- **Average Transfer Amount**  
  - **Endpoint**: `GET /transfers/stats/average_transfer_amount`  
  - **Description**: Calculates the average transfer amount across all transfers.

- **Monthly Transfer Volume**  
  - **Endpoint**: `GET /transfers/stats/monthly_volume`  
  - **Description**: Shows monthly total of transfer volumes.

- **Most Frequent Senders**  
  - **Endpoint**: `GET /transfers/stats/most_frequent_senders`  
  - **Description**: Lists the clients with the highest number of transfers.

---

## Data Consumption

### Primary Method: RESTful API

The primary method to consume the data is through the RESTful API outlined above. Users can interact with the API endpoints for CRUD operations and access analytical insights on clients, promotions, transactions, and transfers.

### Usage with Tools

- **Postman**: 
  - Technical users can interact with the API via **Postman** or browser by entering endpoint URLs, configuring request methods, and viewing responses.


### Advanced Data Access 

For additional analysis and visualization, connect the PostgreSQL database directly to a visualization tool, such as **Power BI**. This setup allows you to create visual reports and dashboards using the data.
You can view the Power BI report with all visualizations [here](visualizations/NonTech.pdf).



These options provide flexible access to both technical and non-technical users, enabling a comprehensive view of the data insights.
