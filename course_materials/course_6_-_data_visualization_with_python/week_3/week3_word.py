# import package and its set of stopwords
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image  # converting images into arrays

# download file and save as alice_novel.txt
# !wget --quiet https://ibm.box.com/shared/static/m54sjtrshpt5su20dzesl5en9xa5vfz1.txt -O alice_novel.txt
# download image
# !wget --quiet https://ibm.box.com/shared/static/3mpxgaf6muer6af7t1nvqkw9cqj85ibm.png -O alice_mask.png

# http://www.gutenberg.org/cache/epub/20727/pg20727.txt


# open the file and read it into a variable alice_novel
alice_novel = open('./47436-0.txt', 'r').read()

# save mask to alice_mask
alice_mask = np.array(Image.open('alice_mask.png'))

stopwords = set(STOPWORDS)
stopwords.add('said')  # add the words said to stopwords

# instantiate a word cloud object
alice_wc = WordCloud(
    background_color='white',
    max_words=2000,
    stopwords=stopwords
)

# instantiate a word cloud object
# alice_wc = WordCloud(
#     background_color='white',
#     max_words=2000,
#     mask=alice_mask,
#     stopwords=stopwords)


# generate the word cloud
alice_wc.generate(alice_novel)

fig = plt.figure(figsize=(10,6))
# fig.set_figwidth(14)  # set width
# fig.set_figheight(18)  # set height

# display the cloud
plt.imshow(alice_wc, interpolation='bilinear')
# plt.imshow(alice_mask, cmap=plt.cm.gray, interpolation='bilinear')

plt.axis('off')
# plt.show()
plt.tight_layout()
plt.savefig('articles.png')
