from livewires import games, color
import random

games.init(screen_width=640, screen_height=480, fps=50)

class Shoot(games.Sprite):
    image1 = games.load_image('img/shoot.gif')


    def __init__(self, police_x, police_y, police):
        super(Shoot, self).__init__(image=Shoot.image1, x=police_x, y=police_y + 55, dy=5)
        self.police = police


    def update(self):
        if self.overlapping_sprites:
            for sprite in self.overlapping_sprites:
                sprite.destroy()
            self.destroy()
            self.police.score.value += 1


class Police(games.Sprite):
    image1 = games.load_image('img/police.gif')
    SHOOT_DELAY = 30


    def __init__(self, game, x, y):
        super(Police, self).__init__(image=Police.image1, x=x, y=y)
        self.game = game
        self.shoot_wait = 0
        self.time_till_drop = 70
        self.score = games.Text(value=0,
                                size=100,
                                color=color.black,
                                top=30,
                                right=70)
        games.screen.add(self.score)


    def update(self):
        if self.shoot_wait > 0:
            self.shoot_wait -= 1

        if games.keyboard.is_pressed(games.K_LEFT):
            self.x -= 2
        if games.keyboard.is_pressed(games.K_RIGHT):
            self.x += 2

        if self.right > games.screen.width:
            self.right = games.screen.width
        if self.left < 0:
            self.left = 0

        if games.keyboard.is_pressed(games.K_SPACE) and self.shoot_wait==0:
            new_shoot = Shoot(self.x, self.y, self)
            games.screen.add(new_shoot)
            self.shoot_wait = Police.SHOOT_DELAY
        self.check_drop()


    def check_drop(self):
        if self.time_till_drop > 0:
            self.time_till_drop -= 1
        else:
            y = games.screen.width + 50
            x = random.randint(0, 600)
            new_terrorist = Terrorist1(x=x, y=y)
            games.screen.add(new_terrorist)

            self.time_till_drop = random.randint(100, 150)


class Terrorist1(games.Sprite):
    image = games.load_image('img/terrorist1.gif')
    SPEED = 2


    def __init__(self, x, y):
        super(Terrorist1, self).__init__(
            image=Terrorist1.image,
            x=x, y=y,
            dy=-random.choice([0.5,0.4,0.7,0.3,0.8,0.6]) * Terrorist1.SPEED,
        )


    def update(self):
        if self.top == 0:
            self.destroy()
            end_sms = games.Message(value='GAME OVER', size=110,
                                    color=color.black,
                                    x=games.screen.width/2,
                                    y=games.screen.height/2,
                                    lifetime=2 * games.screen.fps,
                                    after_death=games.screen.quit
                                    )
            games.screen.add(end_sms)


class Game():
    def __init__(self):
        self.police = Police(game=self,
                         x=games.screen.width/2,
                         y=games.screen.height - 420)
        games.screen.add(self.police)


    def play(self):
        back_image = games.load_image('img/back2.jpg',transparent=False)
        games.screen.background = back_image

        begin_sms = games.Message(value='СПАСИТЕ МИР ОТ ВРАГОВ', size=50,
                                color=color.black,
                                x=games.screen.width / 2,
                                y=games.screen.height / 2,
                                lifetime=2 * games.screen.fps,
                                )
        games.screen.add(begin_sms)

        for i in range(4):
            y = games.screen.width + 50
            x = 100 + i*150
            new_terrorist = Terrorist1(x=x, y=y)
            games.screen.add(new_terrorist)

        games.screen.mainloop()

def main():
    go = Game()
    go.play()


if __name__ == '__main__':
    main()
