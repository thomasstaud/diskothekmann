import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

PATH = "data/high_popularity_spotify_data.csv"

df = pd.read_csv(PATH, usecols=["track_id", "track_name", "track_artist", "track_album_release_date"])
df.rename(columns={"track_id": "id", "track_name": "name", "track_artist": "artist", "track_album_release_date": "date"}, inplace=True)
df["year"] = pd.to_datetime(df["date"], format="mixed").dt.year
df = df.drop('date', axis=1)

print(df.head())
print(df.shape[0])

def sample_group(group):
    return group.sample(min(len(group), 15), random_state=17)

df = (
    df.groupby('year', group_keys=False)
      .apply(sample_group)
      .reset_index(drop=True)
)

print(df.head())
print(df.shape[0])

# store in sqlite db
db_engine = create_engine('sqlite:///songs.db')
df.to_sql('songs', con=db_engine, if_exists='replace', index=False)


def plot():
    year_counts = df['year'].value_counts().sort_index()
    # Plot
    ax = year_counts.plot(kind='bar', xlabel='Year', ylabel='Count', title='Number of Songs per Year')

    # Keep all ticks, but only label every second one
    ax.set_xticks(range(len(year_counts)))
    ax.set_xticklabels([str(y) if i % 2 == 0 else '' for i, y in enumerate(year_counts.index)])

    plt.show()
#plot()
