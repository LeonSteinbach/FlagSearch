import os
from PIL import Image


colors = {'red':    (255,0,0),
          'green':  (0,255,0),
          'blue':   (0,0,255),
          'yellow': (255,255,0),
          'white':  (305,305,305),
          'black':  (-50,-50,-50)}

def distance(left, right):
    return sum((l - r) ** 2 for l, r in zip(left, right)) ** 0.5

class NearestColorKey(object):
    def __init__(self, goal):
        self.goal = goal
    
    def __call__(self, item):
        return distance(self.goal, item[1])


img_dir = os.getcwd() + '\images'
data_file = open('data.txt', 'w')

for file in os.listdir(img_dir):
    if file.endswith('.png'):
        color_data = [list(i) for i in Image.open(img_dir + '\\' + file).convert('RGB').resize((25, int(25 / 3 * 2)), Image.ANTIALIAS).getcolors()]

        # Get total amount of colors for calculating the percentage
        count = 0
        for t in color_data:
            count += t[0]

        # Calculate Percentage
        for t in color_data:
            t[0] = t[0] / count * 100.0

        # Write data to file
        country = ''
        for letter in file:
            if letter == '.':
                break
            country += letter
        data_file.write(country + ': ')
        
        data = {'red': 0, 'green': 0, 'blue': 0, 'yellow': 0, 'white': 0, 'black': 0}

        for i, t in enumerate(color_data):
            c = str(min(colors.items(), key=NearestColorKey(t[1])))
            col = ''
            for letter in c:
                if letter.isalpha():
                    col += letter
            data[col] += t[0]

        for i in data:
            data[i] = round(data[i], 2)

        data_file.write(str(data) + '\n')

data_file.close()

