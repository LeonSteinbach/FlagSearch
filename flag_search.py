# Read and convert data from file
file = open('data.txt')

colors = ['red', 'green', 'blue', 'yellow', 'white', 'black']
data = {}
min_percentage = 5

for line in file:
    country_data = {}
    country_str = line[3:]
    new_country_str = ''
    color_i = 0
    for i, letter in enumerate(country_str):
        if letter.isdigit() or letter == '.':
            new_country_str += letter
            if not country_str[i+1].isdigit() and country_str[i+1] != '.':
                country_data[colors[color_i]] = float(new_country_str)
                new_country_str = ''
                color_i += 1
    data[line[:2]] = country_data


def get_value(key, search):
    val = 0
    for col in search:
        val += data[key][col]
        if data[key][col] < min_percentage:
            val = 0
            break
    return val


def get_flags(search):
    countries = list(data.keys())
    sorted_countries = []
    
    for key in data.keys():
        val = get_value(key, search)
        if len(sorted_countries) == 0:
            sorted_countries.append((key, round(val, 2)))
            continue
        for i, country in enumerate(sorted_countries):
            if val > country[1]:
                sorted_countries.insert(i, (key, round(val, 2)))
                break
        else:
            sorted_countries.append((key, round(val, 2)))
    return sorted_countries
