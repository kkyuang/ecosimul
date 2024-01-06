import pygame
import sys
import math
import random

# 초기화
pygame.init()

# 화면 설정
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Predator-Prey Simulation")

# 색깔
RED = (255, 0, 0)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

# 개체 클래스 정의
class Entity:
    def __init__(self, color, speed, szheight, szwidth, breed_time, death_time):
        self.color = color
        
        #변이 확률
        if random.uniform(0, 1) < 0.1:
            self.height = szheight + szheight * random.uniform(-0.2, 0.2)
        else:
            self.height = szheight
            
        #변이 확률
        if random.uniform(0, 1) < 0.1:
            self.width = szwidth + szwidth * random.uniform(-0.2, 0.2)
        else:
            self.width = szwidth
            
        self.rect = pygame.Rect(random.uniform(0, width - szwidth), random.uniform(0, height - szheight), szwidth, szheight)
        self.direction = random.uniform(0, 2 * 3.1415926535)
        
        #변이 확률
        if random.uniform(0, 1) < 0.1:
            self.speed = speed + speed * random.uniform(-0.2, 0.2)
        else:
            self.speed = speed
            
        self.time_since_breed = 0
        self.eaten = 0
        self.breed_time = random.uniform(breed_time, breed_time*2)
        self.death_time = random.uniform(death_time, death_time*2)

    def move(self):
        self.rect.x += self.speed * round(math.cos(self.direction))
        self.rect.y += self.speed * round(math.sin(self.direction))

        # 화면 경계에서 반대 방향으로 튕기기
        if not (0 <= self.rect.x <= width - self.width):
            self.direction = random.uniform(0, 2 * 3.1415926535)
            self.rect.x = max(0, min(width - self.width, self.rect.x))

        if not (0 <= self.rect.y <= height - self.height):
            self.direction = random.uniform(0, 2 * 3.1415926535)
            self.rect.y = max(0, min(height - self.height, self.rect.y))

    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)


neo_predator_count = 3
predator_count = 10
prey_count = 100
food_count = 500

# 포식자, 피식자, 먹이 객체 생성
neo_predators = [Entity((0, 0, 255), 2, 20, 20, 30, 40) for _ in range(neo_predator_count)]
predators = [Entity(RED, 2, 20, 20, 10, 20) for _ in range(predator_count)]
preys = [Entity(BLACK, 2, 20, 20, 2, 10) for _ in range(prey_count)]
foods = [Entity(YELLOW, 2, 10, 10, 5, 10) for _ in range(food_count)]


# 게임 루프
clock = pygame.time.Clock()
time_elapsed = 0
neo_predator_counts = []
predator_counts = []
prey_counts = []
food_counts = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # 이동
    for neo_predator in neo_predators:
        neo_predator.move()
    for predator in predators:
        predator.move()
    for prey in preys:
        prey.move()

    # 포식
    for prey in preys:
        for predator in predators:
            if prey.rect.colliderect(predator.rect):
                #사냥 실패 확률 존재
                if random.uniform(0, 1) < 0.5:
                    if prey in preys:
                        preys.remove(prey)
                    predator.eaten += 1
                    
    #최상위 포식
    for predator in predators:
        for neo_predator in neo_predators:
            if predator.rect.colliderect(neo_predator.rect):
                #사냥 실패 확률 존재
                if random.uniform(0, 1) < 0.5:
                    if predator in predators:
                        predators.remove(predator)
                    neo_predator.eaten += 1


    # 먹이 생성
    if time_elapsed % 1 == 0:
        foods.append(Entity(YELLOW, 2, 10, 10, 10, 10))

    # 먹이 먹기
    for prey in preys:
        for food in foods:
            if prey.rect.colliderect(food.rect):
                if food in foods:
                    foods.remove(food)
                prey.eaten += 1
                
    #번식
    for neo_predator in neo_predators:
        neo_predator.time_since_breed += 1/30
        if neo_predator.time_since_breed >= neo_predator.breed_time:
            if neo_predator.eaten >= neo_predator.breed_time / 4:
                neo_predators.append(Entity((0, 0, 255), neo_predator.speed, neo_predator.height, neo_predator.width, 30, 40))
                neo_predator.time_since_breed = 0
                neo_predator.eaten = 0
                
    # 번식
    for predator in predators:
        predator.time_since_breed += 1/30
        if predator.time_since_breed >= predator.breed_time:
            if predator.eaten >= predator.breed_time / 2.5:
                predators.append(Entity(RED, predator.speed, predator.height, predator.width, 10, 20))
                predator.time_since_breed = 0
                predator.eaten = 0
    # 번식
    for prey in preys:
        prey.time_since_breed += 1/30
        if prey.time_since_breed >= prey.breed_time:
            if prey.eaten >= prey.breed_time / 4:
                preys.append(Entity(BLACK, prey.speed, prey.height, prey.width, 2, 10))
                prey.time_since_breed = 0
                prey.eaten = 0

    # 시간 경과
    time_elapsed += 1
    if time_elapsed % 10 == 0:
        neo_predator_counts.append(len(neo_predators))
        predator_counts.append(len(predators))
        prey_counts.append(len(preys))
        food_counts.append(len(foods))

    # 개체 제거
    for neo_predator in neo_predators:
        if neo_predator.time_since_breed >= neo_predator.death_time:
            if neo_predator.eaten <= neo_predator.time_since_breed:
                neo_predators.remove(neo_predator)
    for predator in predators:
        if predator.time_since_breed >= predator.death_time:
            if predator.eaten <= predator.time_since_breed:
                predators.remove(predator)
    for prey in preys:
        if prey.time_since_breed >= prey.death_time:
            if prey.eaten <= prey.time_since_breed:
                preys.remove(prey)

    # 그리기
    screen.fill((255, 255, 255))
    for neo_predator in neo_predators:
        neo_predator.draw()
    for predator in predators:
        predator.draw()
    for prey in preys:
        prey.draw()
    for food in foods:
        food.draw()

    pygame.display.flip()
    clock.tick(30)

    # 종료 조건
    isbreak = False
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                print("Q Pressed")
                isbreak = True                
    if isbreak:
        break
    if len(predators) == 0 or len(preys) == 0:
        break

# 개체 수 그래프 그리기
import matplotlib.pyplot as plt

plt.plot(range(len(neo_predator_counts)), neo_predator_counts, label='Neo_Predators', color='blue')
plt.plot(range(len(predator_counts)), predator_counts, label='Predators', color='red')
plt.plot(range(len(food_counts)), food_counts, label='Foods', color='yellow')
plt.plot(range(len(prey_counts)), prey_counts, label='Preys', color='black')
plt.xlabel('Time')
plt.ylabel('Number of Entities')
plt.legend()
plt.show()