import random
import os


class Assassin(object):
    @staticmethod
    async def smokescreen(player, ctx, players, enemies, effects, client):
        if player.state == "HIDDEN":
            raise Exception("how")
        
        player.stacks += 20
        await ctx.send(f"{player.name} throws a smokebomb on the battlefield, immediately going hidden, gaining 20 stealth.")
        player.change_state("HIDDEN")

    @staticmethod
    async def blind_spot(player, ctx, players, enemies, effects, client):
        # Can only be used if below 60 stealth. Gains 20 stealth.
        if player.stacks > 60:
            raise Exception("how")

        player.stacks += 20
        await ctx.send(f"{player.name} moves into the enemy's blind spot, avoiding detection further, gaining 20 stealth")

    @staticmethod
    async def patience(player, ctx, players, enemies, effects, client):
        # Patience. Can only be used when stealth is equal to or above 60. Gains 40 stealth.
        if player.stacks < 60:
            raise Exception("how")

        player.stacks += 40
        await ctx.send(f"{player.name} waits patiently in the dark. Gains 40 stealth.")

    @staticmethod
    async def poison_blade(player, ctx, players, enemies, effects, client):
        # Uses 30 stealth. Throws a poison blade towards a targeted enemy, which deals a good amount of physical decaying over the next 2 turns.

        if player.stacks < 30:
            raise Exception("how")

        enemyinfo = ""
        for enemy in enemies:
            enemyinfo.append(f"{enemies.index(enemy) + 1}. {enemy.get_monster_info()}:\n{enemy.get_info()}\n")
        
        while True:
            await ctx.send(f"{client.get_user(player.user_id).mention} choose an enemy to use the ability on\n{enemyinfo}(You need to respond with number in front of the enemy you want to choose.)")

            def check(msg):
                return msg.author == client.get_user(player.user_id) and msg.channel == ctx.channel

            msg = client.wait_for("message", check=check)

            try:
                choice = int(msg.content)
            except:
                await ctx.send("You need to type a number dumbass")
                continue

            if choice < 1:
                await ctx.send("You need to type a valid number dumbass")
                continue

            try:
                enemy = enemies[choice-1]
                break
            except:
                await ctx.send(await ctx.send("You need to type a valid number dumbass"))
                continue

        player.stacks -= 30
        enemy.deal_physical(player.physical)
        effects.append({
                "name": "poison",
                "turns": 2,
                "affects": [enemy],
                "effects": {
                    "health": 0,
                    "physical damage": player.physical,
                    "magic damage": 0,
                    "physical buff": 0,
                    "magic buff": 0,
                    "physical defense": 0,
                    "magic defense": 0,
                    "agility": 0
                }
            })
        await ctx.send(f"{player.name} threw a poison blade at {enemy.get_monster_info()} dealing {player.physical} damage (pre-mitigation), poisoning them for 2 turns. Used 30 stacks.")

    @staticmethod
    async def spawn_of_the_devil(player, ctx, players, enemies, effects, client):
        # Uses 30 stealth. Sends in clones made out of darkness to the battlefield, making them waste their next ability on the clones.
        pass

    @staticmethod
    async def ensnaring_trap(player, ctx, players, enemies, effects, client):
        # Uses 10 stealth. Lays down a trap on the battlefield. If someone steps on the trap (10% chance), they're snared and cannot do anything on the next turn. (uses the trap and gains back 20 stealth)
        pass

    @staticmethod
    async def harbringer_of_death_a_thousand_blades(player, ctx, players, enemies, effects, client):
        # Everything goes silent. You come out of the darkness, unleashing 1 thousand attacks in a matter of seconds. Does en enormous amount of mixed damage. Utilizes all your stealth. Does more damage depending upon the missing health of the target. (Targeted ability)
        pass

class Woman(object):
    @staticmethod
    async def seduction(player, ctx, players, enemies, effects, client):
        # seduces everyone in the room. Increases str and magic for allies and decreases async def and mr for enemies, effects, client.
        pass

    @staticmethod
    async def shout_for_no_reason(player, ctx, players, enemies, effects, client):
        # shouts for literally no reason, confusing the enemies, effects, client, reducing their agility and changing their state to "NORMAL"
        pass

    @staticmethod
    async def dont_touch_me(player, ctx, players, enemies, effects, client):
        # damage dealing abilities won't affect your party for the next turn.
        pass

    @staticmethod
    async def slap(player, ctx, players, enemies, effects, client):
        # slaps the enemies, effects, client, dealing (str) physical damage
        pass

    @staticmethod
    async def cry_for_help(player, ctx, players, enemies, effects, client):
        # starts crying loudly for help. Summons cops who beat up the enemies, effects, client (does magic damage cuz i said so)
        pass

    @staticmethod
    async def pepper_spray(player, ctx, players, enemies, effects, client):
        # pepper sprays the enemies, effects, client, blinding them. (decreses agility to 0 for 1 turn and does some mixed damage)
        pass

    @staticmethod
    async def women_should_be_treated_equally(player, ctx, players, enemies, effects, client):
        # ULTIMATE - steals her enemies, effects, client' stats. They last with her for the next 2 turns before reverting back to normal.
        pass


class Fighter(object):
    @staticmethod
    async def mantis_style(player, ctx, players, enemies, effects, client):
        # Northern Praying Mantis is a style of Chinese martial arts, sometimes called Shandong Praying Mantis after its province of origin. Increases armor and magic resist by a large amount.
        pass

    @staticmethod
    async def monkey_style(player, ctx, players, enemies, effects, client):
        # Monkey Kung Fu or Hóu Quán is a Chinese martial art which utilizes ape or monkey-like movements as part of its technique. Increases agility by a large amount.
        pass

    @staticmethod
    async def viper_style(player, ctx, players, enemies, effects, client):
        # The green bamboo viper is the snake style taught in the United States by Grandmaster Wing Loc Johnson Ng. Deals physcial damage as poison for the next 2 turns (including current turn).
        pass

    @staticmethod
    async def tiger_style(player, ctx, players, enemies, effects, client):
        # Deals physical damage to the enemies, effects, client, scaling with player's stats.
        pass

    @staticmethod
    async def take_it_all(player, ctx, players, enemies, effects, client):
        # Suppresses the feeling of pain, reducing the damage taken by 30%. Also restores 20 fury.
        pass

    @staticmethod
    async def furiosity(player, ctx, players, enemies, effects, client):
        # Sacrifices 20% of own maxhp to gain 40 fury.
        pass

    @staticmethod
    async def dragon_style(player, ctx, players, enemies, effects, client):
        # Takes 60% reduced damage for the next 2 turns. After that, unleases all the damage taken (increased based on fury) to the enemies, effects, client as magic damage.
        pass


class Mage(object):
    @staticmethod
    async def polymorph(player, ctx, players, enemies, effects, client):
        # Requires 50 energy stacks. Polymorphs the enemies, effects, client for 1 turn. They cannot do anything in their next turn and take increases damage from all sources.
        pass

    @staticmethod
    async def demon_summon(player, ctx, players, enemies, effects, client):
        # Summons demons directly from hell (1 demon per 10 energy stack) each doing magic damage which scales with the player's stats.
        pass

    @staticmethod
    async def magic_missiles(player, ctx, players, enemies, effects, client):
        # Throws a bunch of magic missiles towards enemies, effects, client, dealing magic damage which scales with the player's stats.
        pass

    @staticmethod
    async def gods_grace(player, ctx, players, enemies, effects, client):
        # Channels for the next turn, restoring 20 energy stacks gaining a magical shield for the duration which absorbs all kinds of damage. Amount of damage absorbed scales with the player's magic damage.
        pass

    @staticmethod
    async def blizzard(player, ctx, players, enemies, effects, client):
        # Requires 30 stacks. Stuns the enemies, effects, client for 1 turn.
        pass

    @staticmethod
    async def judgement(player, ctx, players, enemies, effects, client):
        # Requires 80 energy stacks. You send your enemies, effects, client for judgement. There is a 50% chance they come out unharmed. If not, they take 40% max health magic damage and you restore 40 energy stacks
        pass

    @staticmethod
    async def dark_vortex(player, ctx, players, enemies, effects, client):
        # Sacrifice 95% of your remaining HP. Summons a whirling mass of dark energy, ripping through all resistances and doing crazy amounts of magical damage, scaling with energy stacks, the amount of hp sacrificed and player's stats (uses all energy stacks).
        pass


class Tank(object):
    @staticmethod
    async def massacre(player, ctx, players, enemies, effects, client):
        # Slams the enemies, effects, client on the ground and pounds them, dealing physcial damage scaling with the player's stats.
        pass

    @staticmethod
    async def rage(player, ctx, players, enemies, effects, client):
        # Channels for 1 ability. Ups armor and magic resist and builds 20 resolve.
        pass

    @staticmethod
    async def land_slide(player, ctx, players, enemies, effects, client):
        # Causes a land slide, reducing their agility. Also makes them prone to more damage by reducing their armor.
        pass

    @staticmethod
    async def taunt(player, ctx, players, enemies, effects, client):
        # Requires 30 resolve. Taunts the enemies, effects, client, making them focus the player. Enemy abilities in the next turn only affect you but they do twice the damage.
        pass

    @staticmethod
    async def intimidate(player, ctx, players, enemies, effects, client):
        # Requires 20 resolve. Intimidates the enemies, effects, client, fearing them. 20% chance of stunning the enemies, effects, client for 1 turn and lowers their damage permanently. If enemies, effects, client are stunned, restores 40 resolve
        pass

    @staticmethod
    async def confrontation(player, ctx, players, enemies, effects, client):
        # Temporarily disable your resistances and take all your opponent's damage head on. In the next turn, do 140% of the damage taken as physcial damage. (requires 50 stacks)
        pass

    @staticmethod
    async def war_cry(player, ctx, players, enemies, effects, client):
        # uses 100 resolve stacks. Starts an inspirational speech, motivating everybody in the party and giving them attack buffs, while gaining a lot of armor and mr himself. The power of the speech and buffs scale with the player's % missing health.
        pass
