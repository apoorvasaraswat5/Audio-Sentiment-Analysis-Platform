from wordcloud import WordCloud

import matplotlib.pyplot as plt

text="Jayant Sharma   Yash Sharma  Kavita Deepak rekha Shobha Animal Rose Lilly Pupil Elephant Tiger Apple Banana Cat Rashmi Dixit Kartik Gwalior Pune Calcutta Delhi"

cloud=WordCloud(background_color="White").generate(text)

plt.imshow(cloud)
plt.axis('off')
plt.show()