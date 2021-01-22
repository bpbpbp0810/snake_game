import pygame
import time 
import random 
 
pygame.init() 
#파이게임 초기화 설정

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 700
# 게임 창 크기 변수로 저장
# 800 X 600: 뱀이 움직이는 부분
# 800 X 100: 점수 및 목숨이 표시되는 부분

GRID_SIZE = 20 
GRID_WIDTH = WINDOW_WIDTH / GRID_SIZE 
GRID_HEIGHT = 600 / GRID_SIZE
# 한 칸의 크기를 20 X 20 픽셀로 지정

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
# 방향 튜플

bigfont = pygame.font.SysFont('malgungothic', 72)
smallfont = pygame.font.SysFont('malgungothic', 36)
#글꼴설정

RED = 255, 0, 0        
BLACK = 0, 0, 0        
WHITE = 255, 255, 255  
ORANGE = 255, 180, 0   
BROWN = 150, 75, 0
# RGB 조합

FPS = 10
# 초당 프레임

def draw_background(window): 
# 게임 배경 그리기
    grass = pygame.image.load('grass.jpg') 
    #400 x 400 크기의 배경 이미지 로드
    for i in range(WINDOW_WIDTH // grass.get_width() + 1):
        for j in range(600 // grass.get_height() + 1):
            window.blit(grass, (i * 400, j * 400)) 
            # 이미지로 배경 채우기

def draw_object(window, color, position): 
# 뱀, 먹이, 장애물 등 물체 그리기
    obj = pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE)) 
    pygame.draw.rect(window, color, obj)

class Snake:
    def __init__(self):
        self.color = BROWN
        # 뱀 색깔은 갈색
        self.alive = True 
        # 목숨 상태
        self.lives = 0
        # 목숨 개수
        self.create()

    def create(self): 
    # 게임 시작 시 뱀의 특성
        self.positions = [(int(WINDOW_WIDTH / 2), int(600 / 2))] 
        # 첫 생성 위치는 화면의 정중앙
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT]) 
        # 첫 진행 방향 위, 아래, 좌, 우 중 하나 랜덤으로 선택
        self.length = 2 
        # 시작 길이 2

    def control(self, xy): 
    # 방향 조작
        if (xy[0] * -1, xy[1] * -1) == self.direction:
            return
            # 진행방향의 정반대 방향으로 움직이려고 하면 무시
        else:
            self.direction = xy
            # 아니면 입력한 방향으로 진행방향 바꾸기

    def move(self):
        head = self.positions[0] 
        # 뱀 머리는 몸통의 첫번째 칸
        x, y = self.direction
        toward = ((head[0] + (x * GRID_SIZE), head[1] + (y * GRID_SIZE)))
        # 입력받은 방향으로 칸이 추가로 생성되면서 나아감 

        if head in self.positions[2:]:
            self.alive = False 
            # 자신을 먹으면 죽음
        elif head[0] >= WINDOW_WIDTH or head[0] < 0 or head[1] >= 600 or head[1] < 0:
            self.alive = False 
            # 벽에 부딪히면 죽음
        else:
            self.positions.insert(0, toward) 
            while len(self.positions) != self.length:
                self.positions.pop() 
                # 몸길이 유지하면서 몸통 전체 전진

    def eat(self):
        self.length += 1 
        # 먹이 먹으면 몸통 길이 한 칸 증가

    def draw(self, window): 
    # 뱀 화면에 그리기
        for p in self.positions: 
            draw_object(window, self.color, p)
            # 뱀 몸통 포지션을 for문으로 한 칸씩 화면에 그림

class Feed:
    def __init__(self):
        self.position = (0, 0)
        self.color = ORANGE

    def random_pos(self, snake_positions):
        self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
        # 먹이의 좌표값을 랜덤으로 지정
        for p in snake_positions:
            if p == self.position:
                self.position = (random.randint(0, GRID_WIDTH - 1) * GRID_SIZE, random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE)
                # 먹이 좌표가 뱀 몸통이랑 겹치면 좌표 재지정

    def draw(self, window):
        draw_object(window, self.color, self.position)
        # 좌표에 먹이 표시

def check_eat(snake, feed):
    if snake.positions[0] == feed.position:
        snake.eat()
        feed.random_pos(snake.positions)
        feed.draw(window)
        return True
        # 뱀이 먹이를 먹으면 뱀은 몸이 한 칸 증가하고 먹이는 다른 칸에 랜덤으로 표시

pygame.display.set_caption('Snake Game') #창 이름 설정
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT)) # 게임 창 크기를 튜플로 설정 후 게임 창 객체를 변수에 저장

def main(lives, score): # 메인 함수 정의

    draw_background(window) # 배경 생성
    gulp_sound = pygame.mixer.Sound('gulp.wav')
    urgh_sound = pygame.mixer.Sound('urgh.wav')
    ah_sound = pygame.mixer.Sound('ah.wav') # 효과음 파일 불러오기
    clock = pygame.time.Clock() # 화면 업데이트 시계
    snake = Snake() # 뱀 객체 생성
    feed = Feed() # 먹이 객체 생성
    feed.random_pos(snake.positions) # 화면 상에 랜덤으로 먹이 위치 지정
    snake.lives = lives
    game_score = score

    while True:
        draw_background(window) # 업데이트 후 배경 다시 생성
        
        for event in pygame.event.get():
        # pygame.event.get()으로 발생한 이벤트 목록이 담긴 시퀀스 객체 불러오기
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                # 윈도우의 닫기버튼(QUIT)이 눌리면 파이게임 종료 후 프로그램 종료
            elif event.type == pygame.KEYDOWN:
                # 키보드의 키가 눌리면
                if event.key == pygame.K_UP:
                    snake.control(UP)          
                elif event.key == pygame.K_DOWN:
                    snake.control(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.control(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.control(RIGHT)
                # 각각의 입력된 방향에 따라 뱀이 움직이는 방향 컨드롤

        snake.move()
        speed = (FPS + snake.length) / 3 # 뱀이 길어질수록 빨라지게 설정
        snake.draw(window)
        feed.draw(window)

        if check_eat(snake, feed) == True:
            pygame.mixer.Sound.play(gulp_sound)
            game_score += 1
            # 먹이를 먹으면 꿀꺽 효과음 재생 및 점수 1점 증가
        
        bottom_image = pygame.Rect((0, 600), (800, 100))
        pygame.draw.rect(window, BLACK, bottom_image)
        # 뱀이 움직이는 화면 (800 X 600) 밑에 점수랑 목숨 표시하는 공간 (800 X 100) 생성

        score_image = smallfont.render('점수: {}'.format(game_score), True, WHITE)
        window.blit(score_image, (10, 620))
        # 점수 표시

        live_image = smallfont.render('목숨: {}'.format(snake.lives), True, WHITE)
        window.blit(live_image, (400, 620))
        # 목숨 표시

        if snake.alive == False:
            snake.lives -= 1
            if snake.lives != 0:
                pygame.mixer.Sound.play(urgh_sound)
            break
            # 죽으면 윽! 효과음 재생 및 화면 업데이트 안하고 루프 탈출

        pygame.display.flip()
        pygame.display.update() # 안죽었을 때만 화면 업데이트
        clock.tick(speed) # 업데이트 주기 설정

    if snake.lives != 0:
    # 남은 목숨이 0이 아니면
        main(snake.lives, game_score)
        # 목숨 하나 줄어들고 다시 시작

    elif snake.lives == 0:
    # 목숨을 다 썼다면
        pygame.mixer.Sound.play(ah_sound)
        # Aㅏ...
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and not snake.alive:
                        main(3, 0)
                    # 죽었을 때 r 누르면 목숨 3개 점수 0점부터 다시 시작

            bottom_image = pygame.Rect((0, 600), (800, 100))
            pygame.draw.rect(window, BLACK, bottom_image)
            # 뱀이 움직이는 화면 (800 X 600) 밑에 점수랑 목숨 표시하는 공간 (800 X 100) 생성

            score_image = smallfont.render('점수: {}'.format(game_score), True, WHITE)
            window.blit(score_image, (10, 620))
            # 점수 표시

            live_image = smallfont.render('목숨: {}'.format(snake.lives), True, WHITE)
            window.blit(live_image, (400, 620))
            # 목숨 표시

            ah_image = bigfont.render('Aㅏ....', True, RED)
            game_over_image = smallfont.render('게임종료', True, RED)
            restart_image = smallfont.render('Press R to restart', True, RED)
            window.blit(ah_image, ah_image.get_rect(centerx = WINDOW_WIDTH // 2, centery = (WINDOW_HEIGHT // 2) - 80))
            window.blit(game_over_image, game_over_image.get_rect(centerx = WINDOW_WIDTH // 2, centery = (WINDOW_HEIGHT // 2) - 10))
            window.blit(restart_image, restart_image.get_rect(centerx = WINDOW_WIDTH // 2, centery = (WINDOW_HEIGHT // 2) + 55))
            # 뱀이 죽으면 게임 종료 및 다시 시작 표시

            pygame.display.flip()
            pygame.display.update()

# 시작화면
while True:
        draw_background(window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                main(3, 0) 
                # 아무키나 누르면 게임 시작
        
        title_image = bigfont.render('Snake Game', True, RED)
        game_start_image = smallfont.render('Press any key to start...', True, RED)

        window.blit(title_image, title_image.get_rect(centerx = WINDOW_WIDTH // 2, centery = (WINDOW_HEIGHT // 2) - 70))
        window.blit(game_start_image, game_start_image.get_rect(centerx = WINDOW_WIDTH // 2, centery = WINDOW_HEIGHT // 2))
        pygame.display.flip()
        pygame.display.update()