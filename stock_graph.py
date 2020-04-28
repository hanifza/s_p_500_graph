from time import sleep #Waiting every X seconds
from bs4 import BeautifulSoup #Gathers live data
import requests #Opens webpage
import turtle #Graphics
from datetime import datetime, date #Time and Date
import calendar #Time and Date

#Screen setup
screen = turtle.Screen()
screen.bgcolor("lightblue")
turtle.setup(780, 780)

#Price marker
current_price = turtle.Turtle()
current_price.color("red")
current_price.shape("arrow")
current_price.penup()

#Date
my_date = date.today()
weekday = calendar.day_name[my_date.weekday()]
time_now = datetime.now()

#Prices
current = 0
opening = 0
change = 0

#Other
next_x = -768 #The next x cord for the new iteration
i = 0

#Function gets live data
def update():
  page = requests.get('https://finance.yahoo.com/quote/%5EGSPC?p=^GSPC') #Website of stock (Actually the S&P 500 index, but will soon be changeable)
  soup = BeautifulSoup(page.content, 'html.parser') #Opens source code of website
  price = str(list(soup.find_all('span')[8])) #Line with the current $
  #Reformatting data to become float
  price = price.replace('[\'', '')
  price = price.replace(',', '')
  price = price.replace("']", '')

  return (float(price))

#=====LIVE LOOP=====#
while True:
  #This loop basically prevents the graph from starting till there is a opening day price, so the code MUST begin before the market opens to function properly
  while opening == 0:
    if weekday != 'Sunday' and  weekday != 'Saturday':
      opening = update()
      current_price.setposition(-770, 0) #Start of the graph
      current_price.pendown()
      #Reseting variables for future days
      next_x = -768
      i = 0
    else:
      opening == 0

  #repeating update
  while (weekday != 'Sunday' and  weekday != 'Saturday' and time_now.hour != 16) or i != 390: #If its a weekday before 4:00 PM (Market closes) or the chart has been maxed out
    sleep(60) #Updates every minute for a total of 390 iterations of change
    current = update()
    change = (current - opening) * 10
    current_price.seth(current_price.towards(next_x, change)) #Setting angle of the turtle to face new position
    current_price.forward(2)
    next_x += 2 #Changing variable to work with next iteration
    i += 1
  #Clearing screen for next day
  current_price.penup()
  sleep(62700) #Number of seconds till 9:25 AM from 4:00 PM
  current_price.clear()
  current = 0
  previous = 0
  change = 0
  #After these 2 lines are passed above, the while loop for opening == 0 will start and a new day will begin
