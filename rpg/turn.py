import math


class Turn(object):
    def __init__(self, battle_manager):
        self.battle_manager = battle_manager

    async def start_turn(self, abilities, player_party, enemy_party):
        await self.handle_effects(player_party[0])
        for player in player_party:
            if type(abilities[player]) == str:
                await self.battle_manager.room.ctx.send(abilities[player])
            else:
                abilities[player](self.battle_manager.room.ctx, enemy_party, self.battle_manager.battles[player_party[0]]["ability_effects"])
        
        for enemy in enemy_party:
            if type(abilities[enemy]) == str:
                await self.battle_manager.room.ctx.send(abilities[enemy])
            else:
                abilities[enemy](self.battle_manager.room.ctx, player_party, self.battle_manager.battles[player_party[0]]["ability_effects"])

    async def handle_effects(self, player_token):
        ctx = self.battle_manager.room.ctx
        narration = ""
        for effect in self.battle_manager.battles[player_token]["ability_effects"]:
            effect["turns"] -= 1
            affects = effect["affects"]

            for entity in affects:
                health = effect["effects"]["health"]
                p_dmg = effect["effects"]["physical damage"]
                m_dmg = effect["effects"]["magic damage"]
                p_dmg_buff = effect["effects"]["physical buff"]
                m_dmg_buff = effect["effects"]["magic buff"]
                p_def = effect["effects"]["physical defense"]
                m_def = effect["effects"]["magic defense"]
                ag = effect["effects"]["agility"]

                if health:
                    narration += f"{entity} healed for {health} health due to {effect['name']}.\n"
                    entity.gain_hp(health)
                if p_dmg:
                    narration += f"{entity} took {p_dmg} physical damage (pre-mitigation) due to {effect['name']}.\n"
                    entity.deal_physical(p_dmg)
                if m_dmg:
                    narration += f"{entity} took {m_dmg} magical damage (pre-mitigation) due to {effect['name']}.\n"
                    entity.deal_magical(m_dmg)
                if p_dmg_buff:
                    if p_dmg_buff > 0:
                        narration += f"{entity} gained {p_dmg_buff} physical damage due to {effect['name']}.\n"
                        entity.buff_physical(p_dmg_buff)
                    else:
                        narration += f"{entity} lost {abs(p_dmg_buff)} physical damage due to {effect['name']}.\n"
                        entity.debuff_physical(abs(p_dmg_buff))
                if m_dmg_buff:
                    if m_dmg_buff > 0:
                        narration += f"{entity} gained {m_dmg_buff} magical damage due to {effect['name']}.\n"
                        entity.buff_magical(p_dmg_buff)
                    else:
                        narration += f"{entity} lost {abs(m_dmg_buff)} magical damage due to {effect['name']}.\n"
                        entity.debuff_magical(abs(m_dmg_buff))
                if p_def:
                    if p_def > 0:
                        narration += f"{entity} gained {p_def} physical armor due to {effect['name']}.\n"
                        entity.buff_armor(p_def)
                    else:
                        narration += f"{entity} lost {abs(p_def)} physical armor due to {effect['name']}.\n"
                        entity.debuff_armor(abs(p_def))
                if m_def:
                    if m_def > 0:
                        narration += f"{entity} gained {m_def} magic resist due to {effect['name']}.\n"
                        entity.buff_mr(m_def)
                    else:
                        narration += f"{entity} lost {abs(m_def)} magic resist due to {effect['name']}.\n"
                        entity.buff_mr(abs(m_def))
                if ag:
                    if ag > 0:
                        narration += f"{entity} gained {ag} agility due to {effect['name']}.\n"
                        entity.buff_agility(ag)
                    else:
                        narration += f"{entity} lost {abs(ag)} agility due to {effect['name']}.\n"
                        entity.debuff_agility(abs(ag))

        if narration:
            await ctx.send(narration)
