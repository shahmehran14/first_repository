#!/usr/bin/env python
# coding: utf-8

# # Overview :
# 
# As we want to buy a laptop so we want to grab all the laptops from flipkart website that have a given customer rating along with their prices. We are using a concept called web scraping for this project so that we can save our time surfing flipkart website.
# 
# 
# ### Goal :
# Our Goal is to create a funcion that will take parameters as rating i.e what customer rating laptops we are looking for example : 4.1,4.5,4.6, and highest_lowest_full where highest means we want top 5 expensive laptops of that customer rating category,lowest means we want least expensive laptops and full means a full list of all laptops for that customer rating category. We have to convert  all the names and prices of that rating laptop into a dataframe

# ### Libraries
# 
# Libraries Used | Reason
# ---------- | ----------
# Requests | Imported to push a request to scrape a particular website page and get the text.
# BeautifulSoup | Imported to change the requests data text into a python readable format and then perform operating with bs4 lib
# Lxml | Imported to change the requests data text into HTML source code format
# Pandas | Imported to change the dictionary into a dataframe and perform operating such as sorting on a particular column

# ### Python Script for Web Scraping :

# In[1]:


def scrape_flipkart (rating,highest_lowest): 
    
    # importing all libraries that are required for web scraping
    import bs4
    import lxml
    import requests
    
    # crating a dictionary place holder so that we can create key-value pair where key will be the product name and value be price
    d = {}   
    
    check = True
    
    # page will serve as a page number of the website as it is assumed that we don't know the pages of the website
    page = 1 
    # using while loop so that when all pages will be iterated through the page on which there is no data will be detected and we will break out of loop 
    
    while check:
        data = requests.get(f'https://www.flipkart.com/search?q=laptops&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off&page={page}')
        scrape_data = bs4.BeautifulSoup(data.text,'lxml')
        
        # Below is condition to break out of the loop using class of HTML
        if len(scrape_data.select('.col.col-7-12'))<1:
            break  
            
        else:
            # Using range function to get all number of laptop's per page and then will iterate through all the laptops to match the rating
            for x in range(len(scrape_data.select('._3pLy-c.row'))):
                try:
                # Using try-except so that whenever there will be a laptop with no rating (will give an error) it will simply pass with except
                # and if the rating matched it will add the laptop : price in the dictionary so that we can create a Pandas Dataframe later
                    if len(scrape_data.select('._3pLy-c.row')[x].select('._3LWZlK')[0].getText())>0:
                        if str(rating) == str(scrape_data.select('._3pLy-c.row')[x].select('._3LWZlK')[0].getText()):
                            d[scrape_data.select('._3pLy-c.row')[x].select('.col.col-7-12')[0].select('._4rR01T')[0].getText().split(')')[0]+')'] = scrape_data.select('._3pLy-c.row')[x].select('._30jeq3._1_WHN1')[0].getText()
                except:
                    pass
            #After every laptop will be checked for rating for match on a page then page+=1 will increment the page number to go on next page
            page+=1
            
    # Imporing pandas to create a dataframe       
    import pandas as pd
    df=pd.DataFrame(pd.Series(d))
    df.reset_index(inplace=True)
    
    #Changing the column name for better name and understanding
    df.columns = ['Laptop_name','Price']
    
    #Changing the price format so that it can be converted into an int
    df['price'] = df['Price'].apply(lambda a : a.replace('₹','').replace(',',''))
    df.drop('Price',axis=1,inplace=True)
    
    #Connverting the price from object to int
    df['price'] = pd.to_numeric(df['price'])
    
    #Adding a column of Rating
    df['Rating'] = rating
    
    #Using if-else statement to check for the f() parameter
    if highest_lowest =='highest':
        return df.sort_values('price',ascending=False)[:5]
    
    elif highest_lowest == 'lowest':
        return df.sort_values('price',ascending=True)[:5]
    
    else:
        # Sorting the df on price column in asc
        df = df.sort_values('price',ascending=True)
        # Changing the index for no order to asc order
        df.index = range(len(df))
        return df


# In[4]:


laptop_data = scrape_flipkart(5,'full')


# In[8]:


laptop_data


# In[10]:


#Loading the data to csv file
laptop_data.to_csv('E:\\laptop_data.csv')


# In[ ]:




