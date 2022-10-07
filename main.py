from classes.level import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('Flappy_bird')


def run_neat(config_path: Path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultSpeciesSet,
                                neat.DefaultStagnation, neat.DefaultReproduction,
                                config_path)
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(main, 50)
    return winner


def main(genomes: list[tuple], config):
    level = Level(genomes, config)
    clock = pygame.time.Clock()

    while True:

        level.draw(display)

        level.game_cycle()
        pygame.display.update()

        clock.tick(60)


if __name__ == '__main__':
    winner = run_neat(config_path)
    winner_stor = Path('winner.pickle')
    if not winner_stor.exists():
        winner_stor.touch()
    with open(winner_stor, 'wb') as out:
        pickle.dump(winner, winner_stor)
