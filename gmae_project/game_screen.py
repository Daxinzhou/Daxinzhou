import pygame
from random import randint
from utils import load_image  # 确保这个函数定义正确

class GameScreen:
    def __init__(self, game):
        self.game = game
        self.grid_size = 4
        self.cell_size = 150  # 每个方块的大小
        self.grid = [[randint(1, 4) for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.selected_tile = None
        self.eliminating = []  # 用于记录正在消除的方块位置
        self.score = 0  # 新增的积分变量
        self.time_remaining = 300  # 初始时间为五分钟

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            grid_x, grid_y = self.get_grid_position(x, y)
            print(f"Clicked at: ({x}, {y}), Grid Position: ({grid_x}, {grid_y})")
            if 0 <= grid_x < self.grid_size and 0 <= grid_y < self.grid_size:
                if self.selected_tile is None:
                    self.selected_tile = (grid_x, grid_y)
                else:
                    if self.is_adjacent(grid_x, grid_y, self.selected_tile):
                        self.swap_tiles(self.selected_tile[0], self.selected_tile[1], grid_x, grid_y)
                        self.check_for_matches_and_eliminate()
                    else:
                        self.selected_tile = (grid_x, grid_y)
                        
    def get_grid_position(self, x, y):
        board_x = (self.game.screen.get_width() - self.grid_size * self.cell_size) // 2
        board_y = (self.game.screen.get_height() - self.grid_size * self.cell_size) // 2
        grid_x = (x - board_x) // self.cell_size
        grid_y = (y - board_y) // self.cell_size
        return grid_x, grid_y

    def is_adjacent(self, x, y, selected):
        sx, sy = selected
        return abs(sx - x) + abs(sy - y) == 1

    def swap_tiles(self, x1, y1, x2, y2):
        """交换两个指定位置的方块"""
        print(f"Swapping tiles: ({x1}, {y1}) <-> ({x2}, {y2})")
        temp = self.grid[x1][y1]
        self.grid[x1][y1] = self.grid[x2][y2]
        self.grid[x2][y2] = temp

    def check_for_matches_and_eliminate(self):
        """检查是否有匹配的方块可以消除"""
        matches = []

        # 检查每一行
        for row in range(self.grid_size):
            current_value = None
            match_count = 0
            for col in range(self.grid_size):
                if self.grid[row][col] == current_value and self.grid[row][col] is not None:
                    match_count += 1
                    if match_count >= 3:
                        matches.extend([(row, col - match_count + i) for i in range(match_count)])
                        match_count = 0
                elif self.grid[row][col] is not None:
                    current_value = self.grid[row][col]
                    match_count = 1
            if match_count >= 3:
                matches.extend([(row, col - match_count + i) for i in range(match_count)])

        # 检查每一列
        for col in range(self.grid_size):
            current_value = None
            match_count = 0
            for row in range(self.grid_size):
                if self.grid[row][col] == current_value and self.grid[row][col] is not None:
                    match_count += 1
                    if match_count >= 3:
                        matches.extend([(row - match_count + i, col) for i in range(match_count)])
                        match_count = 0
                elif self.grid[row][col] is not None:
                    current_value = self.grid[row][col]
                    match_count = 1
            if match_count >= 3:
                matches.extend([(row - match_count + i, col) for i in range(match_count)])

        for row, col in set(matches):  # 使用set去重
            self.eliminating.append((row, col))
            self.grid[row][col] = None
            self.score += 1  # 每消除一个方块，增加一分

    def refill_empty(self):
        """用随机方块填补空位"""
        for row in self.grid:
            for i, cell in enumerate(row):
                if cell is None:
                    row[i] = randint(1, 4)

    def update(self):
        # 如果有方块正在消除，则更新状态
        if self.eliminating:
            for pos in list(self.eliminating):
                if self.is_tile_fade_out(pos):
                    self.eliminating.remove(pos)
            if not self.eliminating:
                self.refill_empty()

        # 减少剩余时间
        self.time_remaining -= self.game.clock.tick(60) / 1000.0  # 每秒60帧
        if self.time_remaining <= 0:
            # 时间结束，跳转到游戏结束画面
            self.game.change_screen('end_screen')

    def is_tile_fade_out(self, pos):
        """模拟方块消失的过程，这里简单实现为一帧后消失"""
        return True  # 实际使用时可能需要更复杂的逻辑

    def draw(self):
        self.game.screen.fill((255, 255, 255))  # 填充白色背景
    
        left_side_image = load_image('left_side.jpg')
        right_side_image = load_image('right_side.jpg')
        screen_width, screen_height = self.game.screen.get_size()

        offset = 50
        # 计算每张图片的垂直居中位置
        vertical_center = screen_height // 2 - left_side_image.get_height() // 2
        # 左侧图片的位置
        left_side_rect = left_side_image.get_rect()
        left_side_rect.midtop = (left_side_image.get_width() // 2 + offset, vertical_center)

        # 右侧图片的位置
        right_side_rect = right_side_image.get_rect()
        right_side_rect.midbottom = (screen_width - right_side_image.get_width() // 2 - offset, vertical_center + right_side_image.get_height())

        # 绘制左右两侧的图片
        self.game.screen.blit(left_side_image, left_side_rect)
        self.game.screen.blit(right_side_image, right_side_rect)

        # 计算棋盘左上角的位置
        board_x = (self.game.screen.get_width() - self.grid_size * self.cell_size) // 2
        board_y = (self.game.screen.get_height() - self.grid_size * self.cell_size) // 2
    
        # 遍历棋盘上的每一个方块
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                value = self.grid[i][j]
                if value is not None:
                    # 加载相应的方块图片
                    image = load_image(f'tile_{value}.png')
                    # 计算该方块的左上角位置
                    rect = image.get_rect()
                    rect.topleft = (board_x + j * self.cell_size, board_y + i * self.cell_size)
                    # 绘制方块
                    self.game.screen.blit(image, rect)
                elif (i, j) in self.eliminating:
                    # 如果方块正在消除，则绘制白色方块
                    pygame.draw.rect(self.game.screen, (255, 255, 255), (board_x + j * self.cell_size, board_y + i * self.cell_size, self.cell_size, self.cell_size))


        # 显示积分
        font = pygame.font.Font(None, 75)
        score_text = font.render(f"Score: {self.score}", True, (255, 0, 0))
        self.game.screen.blit(score_text, (60, 50))

        font = pygame.font.Font(None, 48)
        time_text = font.render(f"Time Left: {int(self.time_remaining)}s", True, (0, 0, 0))
        screen_width, screen_height = self.game.screen.get_size()
        self.game.screen.blit(time_text, (screen_width - 250, screen_height - 60))
