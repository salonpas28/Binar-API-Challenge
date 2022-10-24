from flask import Flask, render_template, request, redirect, url_for
import os
from os.path import join, dirname, realpath
import sqlite3
import pandas as pd

# connect sqlite3
con = sqlite3.connect("api.db")
cur = con.cursor()  # cursor for sqlite

# create new table in api.db
con.execute("CREATE TABLE data (tweet varchar(280), HS int, Abusive int, HS_Individual int, HS_Group int, HS_Religion int, HS_Race int, HS_Physical int, HS_Gender int, HS_Other int, HS_Weak int, HS_Moderate int, HS_Strong int)")
con.commit()

print('Table creation successful')  # indicator that table is created

df = pd.read_csv(
    r'D:/Binar Data Science/simple_api1/datasets/data.csv', encoding='latin-1')
df.to_sql('data', con, if_exists='replace', index=False)
con.commit()

print('Dataframe read success')  # indicator that df to sql is successful
con.close()
