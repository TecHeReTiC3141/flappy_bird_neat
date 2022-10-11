from classes.level import *

display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('Flappy_bird')
CUR_GEN = 0


def run_neat(config_path: Path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    population = neat.Population(config)

    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    winner = population.run(main, 25)
    return winner


def eval_genome():
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    with open('best_bot.pickle', 'rb') as we:
        weights = pickle.load(we)
    main(weights, config, is_eval=True)


def main(genomes: list[tuple], config, is_eval=False):
    global CUR_GEN
    level = Level(genomes, config, CUR_GEN, is_eval)
    clock = pygame.time.Clock()

    while True:

        level.draw(display)

        gen_alive = level.game_cycle()
        if not gen_alive:
            break
        pygame.display.update()

        clock.tick(60)
    CUR_GEN += 1


if __name__ == '__main__': # uncomment to see learning of bots
    # winner = run_neat(config_path)
    # winner_stor = Path('best_bot.pickle')
    # if not winner_stor.exists():
    #     winner_stor.touch()
    # with open(winner_stor, 'wb') as out:
    #     pickle.dump(winner, out)
    eval_genome()
