import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("imdb_top_1000.csv")
df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce")
df = df.dropna(subset=["Released_Year"])
df["Released_Year"] = df["Released_Year"].astype(int)

df["Runtime"] = df["Runtime"].str.replace(" min", "", regex=False)
df["Runtime"] = pd.to_numeric(df["Runtime"], errors="coerce")
df = df.dropna(subset=["Runtime"])

df["Gross"] = df["Gross"].str.replace(",", "", regex=False)
df["Gross"] = pd.to_numeric(df["Gross"], errors="coerce")
df = df.dropna(subset=["Gross"])

drama = df[df["Genre"].str.contains("Drama", na=False)]
comedy = df[df["Genre"].str.contains("Comedy", na=False)]

print("Broj Drama filmova:", len(drama))
print("Broj Comedy filmova:", len(comedy))

print("Prosjecni rating Drama:", drama["IMDB_Rating"].mean())
print("Prosjecni rating Comedy:", comedy["IMDB_Rating"].mean())

df["Decade"] = (df["Released_Year"] // 10) * 10

print("\nBroj filmova po deceniji:")
print(df["Decade"].value_counts().sort_index())

print("\nProsjecni rating po deceniji:")
print(df.groupby("Decade")["IMDB_Rating"].mean())

print("\nNajbolji film po deceniji:")
best_movies = df.loc[df.groupby("Decade")["IMDB_Rating"].idxmax()]
print(best_movies[["Series_Title", "Decade", "IMDB_Rating"]])

avg_runtime_by_director = df.groupby("Director")["Runtime"].mean()
max_director = avg_runtime_by_director.idxmax()
max_value = avg_runtime_by_director.max()

print("\nDirektor sa najduzim prosjecnim trajanjem filmova:")
print(max_director)
print("Prosjecno trajanje:", max_value)

max_gross_movie = df.loc[df["Gross"].idxmax()]
print("\nFilm sa najvecom zaradom:")
print(max_gross_movie[["Series_Title", "Released_Year", "Gross"]])

print("\nTop 5 filmova po zaradi:")
print(df.sort_values(by="Gross", ascending=False)[["Series_Title", "Gross"]].head(5))

actors_df = pd.concat([
    df[["Star1", "No_of_Votes"]].rename(columns={"Star1": "Actor"}),
    df[["Star2", "No_of_Votes"]].rename(columns={"Star2": "Actor"}),
    df[["Star3", "No_of_Votes"]].rename(columns={"Star3": "Actor"}),
    df[["Star4", "No_of_Votes"]].rename(columns={"Star4": "Actor"})
])

popular_actors = actors_df.groupby("Actor")["No_of_Votes"].sum().sort_values(ascending=False)

print("\nNajpopularniji glumac:")
print(popular_actors.head(1))

print("\nTop 10 najpopularnijih glumaca:")
print(popular_actors.head(10))

top_directors = avg_runtime_by_director.sort_values(ascending=False).head(10)
plt.figure()
top_directors.plot(kind="bar")
plt.title("Top 10 direktora po prosjecnom trajanju filmova")
plt.xlabel("Direktor")
plt.ylabel("Prosjecno trajanje (min)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure()
plt.scatter(df["IMDB_Rating"], df["Gross"])
plt.title("IMDB Rating vs Zarada")
plt.xlabel("IMDB Rating")
plt.ylabel("Zarada (Gross)")
plt.tight_layout()
plt.show()