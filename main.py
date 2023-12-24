import mysql.connector
import requests
from bs4 import BeautifulSoup


def create_database_connection():
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="test"
    )
    return mydb


def fetch_car_data(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser').find_all(
        "div", {"class": "post-card-item-af972 kt-col-6-bee95 kt-col-xxl-4-e9d46"})

    cars = []
    for s in soup:
        text = s.a.h2.text.replace('\u200c', '')
        desc = s.a.article.div.div.div.text
        price = s.a.article.div.div.find_all("div")[1].text
        cars.append((text, desc, price))
    return cars


def insert_car_data(mycursor, cars):
    sql_check = "SELECT * FROM `test`.`cars` WHERE name = %s AND dis_used = %s AND price = %s"
    sql_insert = "INSERT INTO `test`.`cars` (name , dis_used , price) VALUES (%s, %s, %s)"

    for car in cars:
        mycursor.execute(sql_check, car)
        result = mycursor.fetchone()
        if result is None:
            mycursor.execute(sql_insert, car)


def main():
    mydb = create_database_connection()
    mycursor = mydb.cursor()
    url = 'https://divar.ir/s/shiraz/auto?price=5000000-200000000'
    cars = fetch_car_data(url)
    insert_car_data(mycursor, cars)
    mydb.commit()
    print(mycursor.rowcount, "was inserted.")


if __name__ == "__main__":
    main()
