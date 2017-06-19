import csv
import re

with open("all_liste_js.csv", "rb") as f:
    content = f.readlines()
    with open('all_liste_js_corrected.csv', 'a') as the_file:
        for line in content:
            new_line = re.sub("\s*\n", ",0.1\n",line)
            the_file.write(new_line)
    print("all done")