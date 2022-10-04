from classes.level import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('Flappy_bird')


def setup_neat(config_path: Path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, neat.DefaultReproduction,
                                config_path)
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(main, 50)

def main():
    level = Level()
    clock = pygame.time.Clock()

    while True:

        level.draw(display)

        level.game_cycle()
        pygame.display.update()

        clock.tick(60)


if __name__ == '__main__':
    main()