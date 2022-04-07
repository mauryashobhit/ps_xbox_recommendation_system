import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import LabelEncoder
import pandasql as ps


data=pd.read_csv("final_xbox.csv")
print(data.head(5))

game=["Assassin's Creed Valhalla"]

genre=data.query('Title =={}'.format(game))['Genre(s)'].iloc[0]

df=data.loc[data['Genre(s)']==genre]
df=df['Title'].tolist()
print(genre)
print(df)


{% for title in df %}
<div class="card" style="width: 15rem;" title="{{title}}" >
  <div class="imghvr" style="display:inline-block">
    &nbsp&nbsp&nbsp&nbsp<img class="card-img-top" style="display:inline-block" height="360" width="240" src="/static/images/{{title}}.png" alt="{{title}}">
    <div class="centered" style="color:yellow"><h5>{{title}}<h5></div>
 </div>
</div>
{% endfor %}
