#imports
import pandas as pd
import matplotlib.pyplot as plt
train = pd.read_csv('charts/train.csv')

#Graph Top Published Authors
fig = plt.figure()
most_books_per_author = train.groupby(by = 'author').size().nlargest(15)
plt.xticks(rotation=90)
plt.ylabel('Number of Books')
plt.ticklabel_format(style = 'plain')
ax = plt.bar(most_books_per_author.index,most_books_per_author.values)
plt.title('Top Published Authors')
plt.savefig('graphs/Top_Published_Authors.png',bbox_inches = 'tight')
plt.show()

#Per Epoch scores
val_accuracy = [0.7580, 0.7487, 0.7446, 0.7549, 0.7611, 0.7621, 0.7405, 0.7693, 0.7662, 0.7652, 0.7621,  0.7621, 0.7714, 0.7477, 0.7631, 0.7621, 0.7611, 0.7683, 0.7446, 0.7662]
training_loss = [0.2458, 0.1392, 0.0944, 0.0662, 0.0590, 0.0465, 0.0287, 0.0319, 0.0242, 0.0346, 0.0378, 0.0417, 0.0147, 0.0160, 0.0202, 0.0207, 0.0237, 0.0089, 0.0153, 0.0181]
val_loss = [0.6095, 0.6884, 1.0347, 0.9148, 0.9752, 1.1152, 1.3549, 1.2024, 1.2577, 1.1695, 1.1316, 0.9850, 1.2032, 1.2496, 1.1746, 1.1113, 1.0719, 1.4005, 1.1661, 1.1311]
train_accuracy = [0.8990, 0.9511, 0.9717, 0.9779, 0.9840, 0.9871, 0.9912, 0.9920, 0.9959, 0.9887, 0.9897,0.9897, 0.9956, 0.9954, 0.9946, 0.9969, 0.9951, 0.9969, 0.9959, 0.9951]

#Accuracy and Loss as Epochs Increase Graphs
fig, ax = plt.subplots(2)
ax[0].set_xticks(list(range(0,22))[0:21])
ax[0].set_xticklabels(list(range(1,22))[0:21])
ax[0].set_title('Accuracy and Loss as Epochs Increase')
ax[0].set_ylabel('Accuracy')
ax[0].set_xlabel('Number of Epochs')

ax[1].set_xticks(list(range(0,22))[0:21])
ax[1].set_xticklabels(list(range(1,22))[0:21])
ax[1].set_ylabel('Loss')
ax[1].set_xlabel('Number of Epochs')

ax[0].plot(list(range(len(val_accuracy))),val_accuracy, label = 'val_accuracy', color = 'b', marker='.')
ax[0].plot(list(range(len(train_accuracy))),train_accuracy, label = 'train_accuracy', color = 'r', marker='.')

ax[1].plot(list(range(len(val_loss))),val_loss, label = 'val_loss', color = 'b', marker='.')
ax[1].plot(list(range(len(training_loss))),training_loss, label = 'train_loss', color = 'r', marker='.')
ax[1].legend()
ax[0].legend()
plt.show()
plt.savefig('graphs/epoch_scores.png', bbox_inches = 'tight')