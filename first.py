import random;
f = open("input.txt", "r");
s = f.readline();
a = [];
for i in range(3):
    a.append(f.readline());
ok = 0;
g = open("output.txt", "w");
for i in range(3):
    for j in range(3):
        if (not ok and a[i][j] == '.'):
            f.write(i, j);
            ok = 1;