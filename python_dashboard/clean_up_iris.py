
proper_lines = []
bad_lines = []

with open("../BIGBASE/iris.json") as f:
    index = 0
    for line in f:
        if "null" not in line :
            proper_lines.append(line)
        else :
            bad_lines.append(line)
            print(line)
            print(index)
        index = index+1

print(len(proper_lines))
print(len(bad_lines))
print("done")

with open("../BIGBASE/iris_clean.json", 'w') as fc:
    fc.writelines(proper_lines)
