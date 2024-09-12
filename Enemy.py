class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, enemy_type):
        super().__init__()
        self.image = pygame.image.load(f"{enemy_type}.png").convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.health = 100
        
    def move_towards_player(self, player):
        if self.rect.x < player.rect.x:
            self.rect.x += 2
        else:
            self.rect.x -= 2
        
        if self.rect.y < player.rect.y:
            self.rect.y += 2
        else:
            self.rect.y -= 2
