import json

from apex.util import GET, ReplaceAll

statsURL = "https://r5-pc.stryder.respawn.com/user.php?qt=user-getinfo&getinfo=1&hardware={}&uid={}&language=english&timezoneOffset=1&ugc=1&rep=1&searching=0&change=7&loadidx=1"
allowedPlatforms = {
    "pc": "pc",
    "origin": "pc",
    "ps4": "ps4",
    "ps": "ps4",
    "playstation": "ps4",
    "playstation4": "ps4",
    "xb1": "x1",
    "xbox": "x1",
    "xboxone": "x1",
}


class Apex:
    """ToDo"""

    def GetStats(self, userId: str, platform: str):
        """
        ToDo

        Valid platforms: `PC`, `PS4`, `XB1`
        """

        platform = allowedPlatforms[platform.lower()]
        url = statsURL.format(platform.upper(), userId)
        headers = {"User-Agent": "Respawn HTTPS/1.0"}
        res = GET(url, headers=headers)

        # HTTP 200 (OK).
        if res.status_code == 200:
            data = self.ParseStats(res.text)

            return data


    def ParseStats(self, data: str):
        """ToDo"""

        # Remove first line of API response to create valid JSON.
        data = data.split("\n", 1)[1]
        data = json.loads(data)

        # Discard unused values.
        removeKeys = [
            "charVer",
            "charIdx",
            "endpoint",
            "communities",
            "cdata0",
            "cdata1",
            "cdata19",
            "cdata20",
            "cdata21",
            "cdata22",
            "cdata25",
            "cdata26",
            "cdata27",
            "cdata28",
            "cdata29",
            "cdata30",
        ]

        for key in removeKeys:
            try:
                del data[key]
            except KeyError:
                pass

        # Rename and reorder keys.
        keys = {
            "uid": "userId",
            "name": "username",
            "hardware": "platform",
            "privacy": "partyPrivacy",
            "cdata31": "inMatch",
            "online": "isOnline",
            "joinable": "isJoinable",
            "partyFull": "isPartyFull",
            "kills": "kills",
            "matches": "gamesPlayed",
            "wins": "wins",
            "cdata23": "accountLevel",
            "cdata24": "accountProgress",
            "cdata2": "activeLegend",
            "cdata3": "legendSkin",
            "cdata18": "legendIntro",
            "cdata4": "bannerFrame",
            "cdata5": "bannerStance",
            "cdata6": "bannerBadge1",
            "cdata7": "bannerBadge1Tier",
            "cdata8": "bannerBadge2",
            "cdata9": "bannerBadge2Tier",
            "cdata10": "bannerBadge3",
            "cdata11": "bannerBadge3Tier",
            "cdata12": "bannerTracker1",
            "cdata13": "bannerTracker1Value",
            "cdata14": "bannerTracker2",
            "cdata15": "bannerTracker2Value",
            "cdata16": "bannerTracker3",
            "cdata17": "bannerTracker3Value",
        }

        for key in keys:
            try:
                data[keys[key]] = data.pop(key)
            except KeyError:
                pass

        # Set bool types.
        boolValues = [
            "inMatch",
            "isOnline",
            "isJoinable",
            "partyFull",
        ]

        for key in boolValues:
            try:
                data[key] = bool(data[key])
            except KeyError:
                pass

        # Restructure JSON.
        try:
            data["legend"] = {
                "name": data["activeLegend"],
                "skin": data["legendSkin"],
                "intro": data["legendIntro"],
            }

            del data["activeLegend"]
            del data["legendSkin"]
            del data["legendIntro"]

            data["banner"] = {
                "frame": data["bannerFrame"],
                "stance": data["bannerStance"],
                "badges": [
                    {
                        "badge": data["bannerBadge1"],
                        "tier": data["bannerBadge1Tier"]
                    },
                    {
                        "badge": data["bannerBadge2"],
                        "tier": data["bannerBadge2Tier"]
                    },
                    {
                        "badge": data["bannerBadge3"],
                        "tier": data["bannerBadge3Tier"]
                    },
                ],
                "trackers": [
                    {
                        "tracker": data["bannerTracker1"],
                        "value": data["bannerTracker1Value"]
                    },
                    {
                        "tracker": data["bannerTracker2"],
                        "value": data["bannerTracker2Value"]
                    },
                    {
                        "tracker": data["bannerTracker3"],
                        "value": data["bannerTracker3Value"]
                    },
                ],
            }

            del data["bannerFrame"]
            del data["bannerStance"]
            del data["bannerBadge1"]
            del data["bannerBadge1Tier"]
            del data["bannerBadge2"]
            del data["bannerBadge2Tier"]
            del data["bannerBadge3"]
            del data["bannerBadge3Tier"]
            del data["bannerTracker1"]
            del data["bannerTracker1Value"]
            del data["bannerTracker2"]
            del data["bannerTracker2Value"]
            del data["bannerTracker3"]
            del data["bannerTracker3Value"]
        except KeyError:
            pass

        # Replace cdata values.
        data = json.dumps(data)

        cdata = {
            "1111853120": "Caustic",
            "1409694078": "Lifeline",
            "1464849662": "Pathfinder",
            "182221730": "Gibraltar",
            "2045656322": "Mirage",
            "725342087": "Bangalore",
            "827049897": "Wraith",
            "898565421": "Bloodhound",
            "1031439873": "wins_with_full_squad",
            "1062566391": "double_time_distance",
            "1218507142": "smoke_grenade_enemies_hit",
            "1404343849": "sniper_kills",
            "1454765265": "headshots",
            "1561856843": "kills_as_kill_leader",
            "156609670": "creeping_barrage_damage",
            "159674464": "executions",
            "1712819508": "revives",
            "1814522143": "kills",
            "1913031309": "ar_kills",
            "2019682590": "winning_kills",
            "278004241": "games_played",
            "386848081": "pistol_kills",
            "445985781": "care_package_kills",
            "486927953": "top_3",
            "713918432": "lmg_kills",
            "833459246": "damage",
            "997037285": "shotgun_kills",
            "1049917798": "kills",
            "1469728535": "damage",
            "888240106": "wins_with_full_squad",
            "15753331": "kills",
            "79320088": "games_played",
            "345008354": "kills",
            "1000524603": "care_package_kills",
            "1010955107": "executions",
            "1013667227": "doc_drone_healing",
            "1049919818": "pistol_kills",
            "1436290069": "lmg_kills",
            "1447295346": "damage",
            "1503453708": "games_played",
            "1509839340": "kills",
            "1676898271": "winning_kills",
            "172943936": "kills_as_kill_leader",
            "1758696453": "ar_kills",
            "1768041931": "dropped_items_for_squadmates",
            "1807836495": "smg_kills",
            "2091825336": "shotgun_kills",
            "31935871": "wins_with_full_squad",
            "3941687": "revive_shield_damage_blocked",
            "53059952": "revives",
            "692891435": "top_3",
            "704985961": "sniper_kills",
            "927222661": "headshots",
            "1730527550": "kills",
            "196161681": "kills",
            "1029543241": "wins_with_full_squad",
            "1081609860": "damage",
            "1460730151": "lmg_kills",
            "1618935778": "kills",
            "1790559237": "pistol_kills",
            "1932917010": "games_played",
            "1955189012": "executions",
            "218650152": "kills_as_kill_leader",
            "219040158": "winning_kills",
            "252848455": "headshots",
            "553648221": "smg_kills",
        }

        data = ReplaceAll(str(data), cdata)

        return data
