import pandas as pd
inp = pd.read_csv("kc_new_listings.csv")
pred = pd.read_csv("predictions_kc_new.csv")
df_pred = inp.reset_index(drop=True).join(pred)
print(df_pred.shape)
print(df_pred["predicted_price"].describe())
