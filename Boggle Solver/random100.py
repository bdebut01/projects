data = open('data.txt', 'a')
import random
for i in range(100):
    word = ""
    for j in range(100):
        word = word + chr(97 + random.randrange(0, 25))
    data.write(word + '\n')


data.close()
exit()