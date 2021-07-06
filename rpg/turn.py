import math


class Turn(object):
    def __init__(self, battle_manager):
        self.battle_manager = battle_manager

    def start_turn(self, abilities, player_party, enemy_party):
        self.handle_effects(player_party[0])
        for player in battle_manager.player_party:
            abilities[player](self.battle_manager.room.ctx, enemy_party, self.battle_manager.ability_effects)

        for enemy in battle_manager.enemy_party:
            abilities[enemy](self.battle_manager.room.ctx, player_party, self.battle_manager.ability_effects)

    async def handle_effects(self, player_token):
        for effect in self.battle_manager.battles[player_token]["ability_effects"]:
            ctx = self.battle_manager.room.ctx
            effect["turns"] -= 1
            affects = effect["affects"]

            for entity in affects:
                health = effect["effects"]["health"]
                p_dmg = effect["effects"]["physcial damage"]
                m_dmg = effect["effects"]["magic damage"]
                p_dmg_buff = effect["effects"]["physcial buff"]
                m_dmg_buff = effect["effects"]["magic buff"]
                p_def = effect["effects"]["physical defense"]
                m_def = effect["effects"]["magic defense"]
                ag = effect["effects"]["agility"]

                if health:
                    await ctx,send(f"{entity} healed for {health} health due to {effect["name"]}.")
                    entity.gain_hp(health)
                if p_dmg:
                    await ctx.send(f"{entity} took {p_dmg} physical damage (pre-mitigation) due to {effect["name"]}.")
                    entity.deal_physical(p_dmg)
                if m_dmg:
                    await ctx.send(f"{entity} took {m_dmg} magical damage (pre-mitigation) due to {effect["name"]}.")
                    entity.deal_magical(m_dmg)
                if p_dmg_buff:
                    if p_dmg_buff > 0:
                        await ctx.send(f"{entity} gained {p_dmg_buff} physical damage due to {effect["name"]}.")
                        entity.buff_physcial(p_dmg_buff)
                    else:
                        await ctx.send(f"{entity} lost {math.abs(p_dmg_buff)} physical damage due to {effect["name"]}.")
                        entity.debuff_physcial(math.abs(p_dmg_buff))
                if m_dmg_buff:
                    if m_dmg_buff > 0:
                        await ctx.send(f"{entity} gained {m_dmg_buff} magical damage due to {effect["name"]}.")
                        entity.buff_magical(p_dmg_buff)
                    else:
                        await ctx.send(f"{entity} lost {math.abs(m_dmg_buff)} magical damage due to {effect["name"]}.")
                        entity.debuff_magical(math.abs(m_dmg_buff))
                if p_def:
                    if p_def > 0:
                        await ctx.send(f"{entity} gained {p_def} physcial armor due to {effect["name"]}.")
                        entity.buff_armor(p_def)
                    else:
                        await ctx.send(f"{entity} lost {math.abs(p_def)} physcial armor due to {effect["name"]}.")
                        entity.debuff_armor(math.abs(p_def))
                if m_def:
                    if m_def > 0:
                        await ctx.send(f"{entity} gained {m_def} magic resist due to {effect["name"]}.")
                        entity.buff_mr(m_def)
                    else:
                        await ctx.send(f"{entity} lost {math.abs(m_def)} magic resist due to {effect["name"]}.")
                        entity.buff_mr(math.abs(m_def))
                if ag:
                    if ag > 0:
                        await ctx.send(f"{entity} gained {ag} agility due to {effect["name"]}.")
                        entity.buff_agility(ag)
                    else:
                        await ctx.send(f"{entity} lost {math.abs(ag)} agility due to {effect["name"]}.")
                        entity.debuff_agility(math.abs(ag)

        await ctx.send("The program is supposed to break now")
