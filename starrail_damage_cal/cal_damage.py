from typing import Dict

from msgspec import convert

from starrail_damage_cal.damage.Avatar import AvatarInstance
from starrail_damage_cal.exception import (
    CharNameError,
    MihomoRequestError,
    NotInCharacterShowcaseError,
)
from starrail_damage_cal.map.name_covert import alias_to_char_name, name_to_avatar_id
from starrail_damage_cal.mihomo.models import MihomoData
from starrail_damage_cal.mono.Character import Character
from starrail_damage_cal.to_data import api_to_dict


async def cal_char_info(char_data: Dict):
    char: Character = Character(char_data)
    await char.get_equipment_info()
    await char.get_char_attribute_bonus()
    await char.get_relic_info()
    return char


async def cal_info(char_data: Dict):
    char = await cal_char_info(char_data)
    avatar = AvatarInstance(char)
    return await avatar.get_damage_info()


class DamageCal:
    @classmethod
    async def cal_info(cls, char_data: Dict):
        char = Character(char_data)
        await char.get_equipment_info()
        await char.get_char_attribute_bonus()
        await char.get_relic_info()
        avatar = AvatarInstance(char)
        return await avatar.get_damage_info()

    @classmethod
    async def get_damage_data_by_uid(cls, uid: str, avatar_name: str):
        char_name = alias_to_char_name(avatar_name)
        char_id = name_to_avatar_id(char_name)

        if char_id == "":
            raise CharNameError(char_name)

        char_id_list, char_data_dict = await api_to_dict(uid)

        if isinstance(char_id_list, str):
            msg = "char_id_list is str"
            raise MihomoRequestError(msg)

        if char_data_dict is None:
            msg = "char_data_dict is None"
            raise MihomoRequestError(msg)

        if char_id not in char_id_list:
            raise NotInCharacterShowcaseError

        char_data = char_data_dict[char_id]
        return await cls.cal_info(char_data)

    @classmethod
    async def get_damage_data_by_mihomo_raw(cls, mihomo_raw: Dict, avatar_name: str):
        char_name = alias_to_char_name(avatar_name)
        char_id = name_to_avatar_id(char_name)

        if char_id == "":
            raise CharNameError(char_name)

        mihomo_data = convert(mihomo_raw, type=MihomoData)
        char_id_list, char_data_dict = await api_to_dict(mihomo_raw=mihomo_data)

        if isinstance(char_id_list, str):
            msg = "char_id_list is str"
            raise MihomoRequestError(msg)

        if char_data_dict is None:
            msg = "char_data_dict is None"
            raise MihomoRequestError(msg)

        if char_id not in char_id_list:
            raise NotInCharacterShowcaseError

        char_data = char_data_dict[char_id]
        return await cls.cal_info(char_data)

    @classmethod
    async def get_all_damage_data_by_mihomo_raw(cls, mihomo_raw: Dict):
        mihomo_data = convert(mihomo_raw, type=MihomoData)
        char_id_list, char_data_dict = await api_to_dict(mihomo_raw=mihomo_data)

        if isinstance(char_id_list, str):
            msg = "char_id_list is str"
            raise MihomoRequestError(msg)

        if char_data_dict is None:
            msg = "char_data_dict is None"
            raise MihomoRequestError(msg)

        damage_dict = {}

        for char_id in char_id_list:
            char_data = char_data_dict[char_id]
            damage_dict[char_id] = await cls.cal_info(char_data)

        return damage_dict

    @classmethod
    async def get_all_damage_data_by_uid(cls, uid: str):
        char_id_list, char_data_dict = await api_to_dict(uid=uid)

        if isinstance(char_id_list, str):
            msg = "char_id_list is str"
            raise MihomoRequestError(msg)

        if char_data_dict is None:
            msg = "char_data_dict is None"
            raise MihomoRequestError(msg)

        damage_dict = {}

        for char_id in char_id_list:
            char_data = char_data_dict[char_id]
            damage_dict[char_id] = await cls.cal_info(char_data)

        return damage_dict
