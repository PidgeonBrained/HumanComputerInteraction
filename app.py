import pygame, random, time, csv

"""
Fitt's Law Project - CS 470 Spring 2024
Team Woo Factor 2.0
Pidge Witiak, Ahmed Tamer, Sam Baeyen, Cole Schoenbauer
"""

# ------ Name this file differently for every subject tested!! ------
csv_file = "subject1.csv"

#  --------- Variables for generated circles ---------
# Distance - Size - Direction - ID

challenges = [[0,0,0,0] for i in range(0,32)]
for i in range(0, 32):
    challenges[i][3] = i
    if i < 8:
        challenges[i][0] = 100
    elif i < 16:
        challenges[i][0] = 200
    elif i < 24:
        challenges[i][0] = 300
    elif i < 32:
        challenges[i][0] = 400

sizes = [32, 64, 128, 256]
for i in range(0, 32):
    challenges[i][1] = sizes[i % len(sizes)]

count = 0
flipped = False
for i in range(0, 32):
    if count >= 4:
        flipped = not flipped
        count = 0

    if flipped:
        challenges[i][2] = -1
    else:
        challenges[i][2] = 1
    
    count += 1

print(challenges)
 
# --------- Counting times for each task trial for this user ---------

challenges_counter = {}
for challenge in challenges:
    challenges_counter[challenge[3]] = []

# --------- Starting game ---------

# TODO: Add timer, disclaimer before game starts, practice round, visual indicators for hits and misses

pygame.init()

pygame.display.set_caption('Test')
window_surface = pygame.display.set_mode((1920, 1080))
screen_center = [960,540]

background = pygame.Surface((1920, 1080))
background.fill(pygame.Color('black'))

permutation = challenges[random.randint(0, 31)]
print((screen_center[0] + (permutation[0] * permutation[2]), (screen_center[1] - (permutation[1] // 2))), (permutation[1], permutation[1]))
target = pygame.Rect((screen_center[0] + (permutation[0] * permutation[2]), (screen_center[1] - (permutation[1] // 2))), (permutation[1], permutation[1]))

is_running = True
start_time, start_pos, misses = time.time(), pygame.mouse.get_pos(), 0

while is_running:

    clicked = False

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True

        if event.type == pygame.QUIT:
            is_running = False

    window_surface.fill("black")
    pygame.draw.rect(window_surface, 'white', target)

    # flip() the display to put your work on screen
    pygame.display.flip()

    if clicked and target.collidepoint(pygame.mouse.get_pos()):
        print("Target hit!")

        # Log info
        # Time (milliseconds) - Distance (in pixels (x,y)) - Error (number of misses)
        challenges_counter[permutation[3]].append((((time.time() - start_time) * 1000), (pygame.mouse.get_pos()[0] - start_pos[0], pygame.mouse.get_pos()[1] - start_pos[1]), misses))

        # Set up next square
        permutation = challenges[random.randint(0, 31)]
        print((screen_center[0] + (permutation[0] * permutation[2]), (screen_center[1] - (permutation[1] // 2))), (permutation[1], permutation[1]))
        target = pygame.Rect((screen_center[0] + (permutation[0] * permutation[2]), (screen_center[1] - (permutation[1] // 2))), (permutation[1], permutation[1]))

        # Resetting variables
        start_time, start_pos, misses = time.time(), pygame.mouse.get_pos(), 0
    
    elif clicked and not target.collidepoint(pygame.mouse.get_pos()):
        print("Missed!")
        misses += 1

    pygame.display.update()

pygame.quit()

#  --------- Display times ---------
for challenge in challenges_counter:
    print(f"Permutation: {challenge}, Stats: {challenges_counter[challenge]}")

#  --------- Record Data ---------

with open(csv_file, "w", newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Permuatation", "Time to Complete", "Distance Moved", "Error"])
    for challenge in challenges_counter:
        for result in challenges_counter[challenge]:
            writer.writerow([challenge, result[0], result[1], result[2]])