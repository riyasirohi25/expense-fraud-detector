import sqlite3
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
def load_data():
	conn=sqlite3.connect('data/expenses.db')
	query="SELECT Amount, date, description, is_fraud FROM expenses"
	df=pd.read_sql_query(query,conn)
	print("Columns:", df.columns.tolist()) #added this line to debug
	conn.close()
	return df
def prepare_data(df):
#convert date to numerical features
	df['date']=pd.to_datetime(df['date'])
	min_date=df['date'].min()
	df['days_since']=(df['date']-min_date).dt.days
	df['desc_length']=df['description'].str.len()
	#features and target
	X=df[['amount','days_since','desc_length']]
	Y=df['is_fraud']
	return X,Y
def train_model(X,Y):
	#split the data
	X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=42)
	#train a radom forest model
	model=RandomForestClassifier(n_estimators=100,random_state=42)
	model.fit(X_train,Y_train)
	Y_pred=model.predict(X_test)
	accuracy=accuracy_score(Y_test,Y_pred)
	print(f"Model accuracy:{accuracy:.2f}")
	return model
if __name__=="__main__":
	#load and prepare data
	df=load_data()
	X,Y=prepare_data(df)
	#train and evaluate model
	model=train_model(X,Y)
