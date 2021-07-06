import random
import os


class Assassin(object):
    @staticmethod
    def smokescreen(self, enemies):
        # Throws a smoke bomb on the battlefield. If your party consists of more than 2 members, you go into stealth, becoming untargetable until the enemy uses a revealing or AOE ability. Cannot be used if has more than 0 stealth. (Sets player up for other skills and gains 20 shadow stacks)
        pass

    @staticmethod
    def blind_spot(self, enemies):
        # Can only be used if below 60 stealth. Gains 20 stealth.
        pass

    @staticmethod
    def patience(self, enemies):
        # Patience. Can only be used when stealth is equal to or above 60. Gains 40 stealth.
        pass

    @staticmethod
    def poison_blade(self, enemies):
        # Uses 30 stealth. Throws a poison blade towards a targeted enemy, which deals a good amount of physical decaying over the next 2 turns.
        pass

    @staticmethod
    def spawn_of_the_devil(self, enemies):
        # Uses 30 stealth. Sends in clones made out of darkness to the battlefield, making them waste their next ability on the clones.
        pass

    @staticmethod
    def ensnaring_trap(self, enemies):
        # Uses 10 stealth. Lays down a trap on the battlefield. If someone steps on the trap (10% chance), they're snared and cannot do anything on the next turn. (uses the trap and gains back 20 stealth)
        pass

    @staticmethod
    def harbringer_of_death_a_thousand_blades(self, enemies):
        # Everything goes silent. You come out of the darkness, unleashing 1 thousand attacks in a matter of seconds. Does en enormous amount of mixed damage. Utilizes all your stealth. Does more damage depending upon the missing health of the target. (Targeted ability)
        pass

class Woman(object):
    @staticmethod
    def seduction(ctx, enemies):
        # seduces everyone in the room. Increases str and magic for allies and decreases def and mr for enemies.
        pass

    @staticmethod
    def shout_for_no_reason(ctx, enemies):
        # shouts for literally no reason, confusing the enemies, reducing their agility and changing their state to "NORMAL"
        pass

    @staticmethod
    def dont_touch_me(ctx, enemies):
        # damage dealing abilities won't affect your party for the next turn.
        pass

    @staticmethod
    def slap(ctx, enemies):
        # slaps the enemies, dealing (str) physcial damage
        pass

    @staticmethod
    def cry_for_help(ctx, enemies):
        # starts crying loudly for help. Summons cops who beat up the enemies (does magic damage cuz i said so)
        pass

    @staticmethod
    def pepper_spray(ctx, enemies):
        # pepper sprays the enemies, blinding them. (decreses agility to 0 for 1 turn and does some mixed damage)
        pass

    @staticmethod
    def women_should_be_treated_equally(ctx, enemies):
        # ULTIMATE - steals her enemies' stats. They last with her for the next 2 turns before reverting back to normal.
        pass


class Fighter(object):
    @staticmethod
    def mantis_style(ctx, enemies):
        # Northern Praying Mantis is a style of Chinese martial arts, sometimes called Shandong Praying Mantis after its province of origin. Increases armor and magic resist by a large amount.
        pass

    @staticmethod
    def monkey_style(ctx, enemies):
        # Monkey Kung Fu or Hóu Quán is a Chinese martial art which utilizes ape or monkey-like movements as part of its technique. Increases agility by a large amount.
        pass

    @staticmethod
    def viper_style(ctx, enemies):
        # The green bamboo viper is the snake style taught in the United States by Grandmaster Wing Loc Johnson Ng. Deals physcial damage as poison for the next 2 turns (including current turn).
        pass

    @staticmethod
    def tiger_style(ctx, enemies):
        # Deals physcial damage to the enemies, scaling with player's stats.
        pass

    @staticmethod
    def take_it_all(ctx, enemies):
        # Suppresses the feeling of pain, reducing the damage taken by 30%. Also restores 20 fury.
        pass

    @staticmethod
    def furiosity(ctx, enemies):
        # Sacrifices 20% of own maxhp to gain 40 fury.
        pass

    @staticmethod
    def dragon_style(ctx, enemies):
        # Takes 60% reduced damage for the next 2 turns. After that, unleases all the damage taken (increased based on fury) to the enemies as magic damage.
        pass


class Mage(object):
    @staticmethod
    def polymorph(ctx, enemies):
        # Requires 50 energy stacks. Polymorphs the enemies for 1 turn. They cannot do anything in their next turn and take increases damage from all sources.
        pass

    @staticmethod
    def demon_summon(ctx, enemies):
        # Summons demons directly from hell (1 demon per 10 energy stack) each doing magic damage which scales with the player's stats.
        pass

    @staticmethod
    def magic_missiles(ctx, enemies):
        # Throws a bunch of magic missiles towards enemies, dealing magic damage which scales with the player's stats.
        pass

    @staticmethod
    def gods_grace(ctx, enemies):
        # Channels for the next turn, restoring 20 energy stacks gaining a magical shield for the duration which absorbs all kinds of damage. Amount of damage absorbed scales with the player's magic damage.
        pass

    @staticmethod
    def blizzard(ctx, enemies):
        # Requires 30 stacks. Stuns the enemies for 1 turn.
        pass

    @staticmethod
    def judgement(ctx, enemies):
        # Requires 80 energy stacks. You send your enemies for judgement. There is a 50% chance they come out unharmed. If not, they take 40% max health magic damage and you restore 40 energy stacks
        pass

    @staticmethod
    def dark_vortex(ctx, enemies):
        # Sacrifice 95% of your remaining HP. Summons a whirling mass of dark energy, ripping through all resistances and doing crazy amounts of magical damage, scaling with energy stacks, the amount of hp sacrificed and player's stats (uses all energy stacks).
        pass


class Tank(object):
    @staticmethod
    def massacre(ctx, enemies):
        # Slams the enemies on the ground and pounds them, dealing physcial damage scaling with the player's stats.
        pass

    @staticmethod
    def rage(ctx, enemies):
        # Channels for 1 ability. Ups armor and magic resist and builds 20 resolve.
        pass

    @staticmethod
    def land_slide(ctx, enemies):
        # Causes a land slide, reducing their agility. Also makes them prone to more damage by reducing their armor.
        pass

    @staticmethod
    def taunt(ctx, enemies):
        # Requires 30 resolve. Taunts the enemies, making them focus the player. Enemy abilities in the next turn only affect you but they do twice the damage.
        pass

    @staticmethod
    def intimidate(ctx, enemies):
        # Requires 20 resolve. Intimidates the enemies, fearing them. 20% chance of stunning the enemies for 1 turn and lowers their damage permanently. If enemies are stunned, restores 40 resolve
        pass

    @staticmethod
    def confrontation(ctx, enemies):
        # Temporarily disable your resistances and take all your opponent's damage head on. In the next turn, do 140% of the damage taken as physcial damage. (requires 50 stacks)
        pass

    @staticmethod
    def war_cry(ctx, enemies):
        # uses 100 resolve stacks. Starts an inspirational speech, motivating everybody in the party and giving them attack buffs, while gaining a lot of armor and mr himself. The power of the speech and buffs scale with the player's % missing health.
        pass
