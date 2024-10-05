import pygame
import player_shots as shots_mod
import floors as floor_mod
import player_behavior as player_mod
import life as life_mod
import math
import random
import screen as screen_mod
import wave_controller as wave_controller_mod

screen = screen_mod.screen
pwrups_shuffled = False
pwrups_picked = False

power_up_collectible_size = 100
display_text_1 = ''
display_text_2 = ''

plus_sprite = pygame.image.load('assets/power_up_sprites/+.jpg')


def powerup_damageup():
    # +20% damage, additively
    # size up slightly
    # shot flight speed down slightly
    shots_mod.damage_value += 20
    if shots_mod.size_value * 1.1 <= floor_mod.floor_size_y * 0.8:
        shots_mod.size_value *= 1.1
    shots_mod.speed_value *= 0.9


def powerup_firerateup():
    # -25% shot cooldown, multiplicative
    shots_mod.cooldown_value *= 0.75
    round(shots_mod.cooldown_value)


def powerup_multishot():
    # +1 or +33% projectiles per shot, at the cost of -33% damage, multiplicative
    if shots_mod.multishot_value >= 3:
        shots_mod.multishot_value += round(shots_mod.multishot_value * 0.34)
    else:
        shots_mod.multishot_value += 1

    shots_mod.size_value *= 0.90
    shots_mod.damage_modifier *= 0.67
    shots_mod.inaccuracy_value += 1


def powerup_pierceup():
    # increases how many times each shot can go through an enemy/floor without beind destroyed
    shots_mod.pierce_value += 1


def powerup_move_speed():
    # +25% player sideways movement speed, additively
    player_mod.player_move_speed += player_mod.PLAYER_BASE_SPEED * 1.25
    round(player_mod.player_move_speed)


def powerup_climb_speed():
    # -20% up/down between floors movement cooldown, additively, down to a minimum of 5 frames
    player_mod.player_updown_cd -= player_mod.BASE_UPDOWN_CD * 0.2
    if player_mod.player_updown_cd < 5:
        player_mod.player_updown_cd = 5


def powerup_instaheal():
    #heal 30% of maximum health, rounded up
    life_mod.life += life_mod.max_life * 0.3
    life_mod.life = math.ceil(life_mod.life)
    if life_mod.life > life_mod.max_life:
        life_mod.life = life_mod.max_life


def powerup_full_heal():
    #heal back to maximum health
    life_mod.life = life_mod.max_life


def powerup_health_boost():
    #increase maximum health by 25, also heals by 25
    life_mod.max_life += 25
    life_mod.life += 25


offense_powerups = [powerup_damageup, powerup_firerateup, powerup_pierceup, powerup_multishot]
support_powerups = [powerup_move_speed, powerup_climb_speed, powerup_instaheal, powerup_full_heal, powerup_health_boost]

pwrup_bundle_1 = []
pwrup_bundle_2 = []
pwrup_bundle_3 = []

bundle_list = [pwrup_bundle_1, pwrup_bundle_2, pwrup_bundle_3]


class powerup:
    def __init__(self, pwrup_func, rect):
        self.effect = pwrup_func
        self.rect = rect

        if self.effect == powerup_damageup:
            self.sprite = pygame.image.load('assets/power_up_sprites/damage_up_placeholder.jpg')
            self.text = "+20% damage!"
        elif self.effect == powerup_firerateup:
            self.sprite = pygame.image.load('assets/power_up_sprites/fire_rate_up_placeholder.jpg')
            self.text = "Shoot 25% faster!"
        elif self.effect == powerup_pierceup:
            self.sprite = pygame.image.load('assets/power_up_sprites/pierce_up_placeholder.png')
            self.text = "Shots pass through one floor!"
        elif self.effect == powerup_multishot:
            self.sprite = pygame.image.load('assets/power_up_sprites/multishot_placeholder.jpg')
            self.text = "More bullets per shot"
        elif self.effect == powerup_move_speed:
            self.sprite = pygame.image.load('assets/power_up_sprites/speed_up_leftright_placeholder.jpg')
            self.text = "Speed +25%!"
        elif self.effect == powerup_climb_speed:
            self.sprite = pygame.image.load('assets/power_up_sprites/speed_up_updown_placeholder.jpg')
            self.text = "Climbing speed +20%!"
        elif self.effect == powerup_instaheal:
            self.sprite = pygame.image.load('assets/power_up_sprites/small_heal_placeholder.jpg')
            self.text = "Recover 30% of health!"
        elif self.effect == powerup_full_heal:
            self.sprite = pygame.image.load('assets/power_up_sprites/full_heal_placeholder.jpg')
            self.text = "Recover 100% of health!"
        elif self.effect == powerup_health_boost:
            self.sprite = pygame.image.load('assets/power_up_sprites/max_health_up_placeholder.jpg')
            self.text = "Increase maximum health by 25!"

        self.sprite = pygame.transform.scale(self.sprite, (power_up_collectible_size, power_up_collectible_size))

    def render(self):
        screen.blit(self.sprite, self.rect)


# shuffle available upgrades before showcasing them to the player
def randomize_bundles():
    global bundle_list
    global pwrup_bundle_1
    global pwrup_bundle_2
    global pwrup_bundle_3
    global pwrups_shuffled

    bundle_list = []
    support_copy = support_powerups.copy()
    offense_copy = offense_powerups.copy()
    print(offense_copy)


    for bundle in range(2):
        bundle = []

        support = random.choice(support_copy)
        support_copy.remove(support)

        offensive = random.choice(offense_copy)
        offense_copy.remove(offensive)

        bundle.append(offensive)
        bundle.append(support)

        bundle_list.append(bundle)

        print(offense_copy)

    pwrups_shuffled = True


def do_selection(is_selecting):
    global pwrups_picked
    global display_text_1
    global display_text_2

    floors_bottom_y_list = floor_mod.floors_bottom_y_list
    for n in range(1, 4):
        ground_y = floors_bottom_y_list[n]
        rect_1 = pygame.Rect(0, 0, power_up_collectible_size, power_up_collectible_size)
        rect_1.bottom = ground_y
        rect_1.centerx = (floor_mod.floor_size_x / 2) - 100

        rect_2 = pygame.Rect(0, 0, power_up_collectible_size, power_up_collectible_size)
        rect_2.bottom = ground_y
        rect_2.centerx = (floor_mod.floor_size_x / 2) + 100

        pwrup_1 = powerup(bundle_list[n - 2][0], rect_1)
        pwrup_2 = powerup(bundle_list[n - 2][1], rect_2)

        pwrup_1.render()
        pwrup_2.render()
        plus_rect = pygame.Rect(0, 0, 66, 66)
        plus_rect.centerx = floor_mod.floor_size_x / 2
        plus_rect.bottom = ground_y
        screen.blit(plus_sprite, plus_rect)

        local_pwrup_bundle = [pwrup_1.effect, pwrup_2.effect]
        rect_list = [rect_1, rect_2]

        # check if player is coming in contact with the upgrade
        is_touching_list = False
        for x in rect_list:
            if player_mod.player_pos.colliderect(x):
                is_touching_list = True
                display_text_1 = pwrup_1.text
                display_text_2 = pwrup_2.text

        # check if player is trying to pick up upgrade
        if is_selecting == True and pwrups_picked == False:
            if is_touching_list:
                for effect in local_pwrup_bundle:
                    effect()
                    print(effect)
                pwrups_picked = True
                #commands to continue next wave here
                wave_controller_mod.is_power_picked = True
