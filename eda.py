import pandas as pd
import matplotlib.pyplot as plt

best_df = pd.read_csv('charts/best_sellers.csv')
non_df = pd.read_csv('charts/non_best_sellers.csv')

fig = plt.figure()
most_books_per_author = best_df.groupby(by = 'author').size().nlargest(15)
plt.xticks(rotation=90)
plt.ylabel('Number of Books')
plt.ticklabel_format(style = 'plain')
ax = plt.bar(most_books_per_author.index,most_books_per_author.values)
plt.title('Top Bestseller Authors')
plt.savefig('graphs/Top_Bestseller_Authors.png',bbox_inches = 'tight')

epoch_scores = [0.7580, 0.7487, 0.7446, 0.7549, 0.7611, 0.7621, 0.7405, 0.7693, 0.7662, 0.7652, 0.7621,  0.7621, 0.7714, 0.7477, 0.7631, 0.7621, 0.7611, 0.7683, 0.7446, 0.7662]
#current at 15 include 16
fig, ax = plt.subplots()
ax.set_xticks(list(range(0,22))[0:21])
ax.set_xticklabels(list(range(0,22))[0:21])
ax.set_title('accuracy as epochs increase')
ax.set_ylabel('test accuracy')
ax.set_xlabel('epochs')
ax.plot(list(range(len(epoch_scores))),epoch_scores)
plt.savefig('graphs/epoch_scores.png', bbox_inches = 'tight')