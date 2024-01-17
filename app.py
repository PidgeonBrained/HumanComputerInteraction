# Fitt's Law Project

# Variables for generated circles
# Distance - Size - Direction
challenges = [[0,0,0] for i in range(0,32)]
for i in range(0, 32):
    if i < 8:
        challenges[i][0] = 100
    elif i < 16:
        challenges[i][0] = 200
    elif i < 24:
        challenges[i][0] = 300
    elif i < 32:
        challenges[i][0] = 400

sizes = [16, 32, 64, 128]
for i in range(0, 32):
    challenges[i][1] = sizes[i % len(sizes)]

count = 0
flipped = False
for i in range(0, 32):
    if count >= 4:
        flipped = not flipped
        count = 0

    challenges[i][2] = int(flipped)
    count += 1

print(challenges)