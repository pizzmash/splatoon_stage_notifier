import datetime
from abc import ABCMeta, abstractmethod


class TextBuilder(metaclass=ABCMeta):
    def __init__(self, schedules):
        self.schedules = schedules

    @abstractmethod
    def build(self, **kwargs):
        pass

    def extract_gachi_match(self, idx):
        return self.schedules["gachi"][idx]

    def extract_match_info(self, match):
        return match["rule"]["name"], match["stage_a"]["name"], match["stage_b"]["name"]

    def extract_start_hour(self, match):
        return datetime.datetime.fromtimestamp(match["start_time"]).hour


class CurrentRuleTB(TextBuilder):
    def build(self, **kwargs):
        match = self.extract_gachi_match(0)
        rule, stage_a, stage_b = self.extract_match_info(match)

        return "現在のガチマッチのルールは" + rule + "、ステージは" + stage_a + "と" + stage_b + "です。"


class NextRuleTB(TextBuilder):
    def build(self, **kwargs):
        match = self.extract_gachi_match(1)
        start_hour = self.extract_start_hour(match)
        rule, stage_a, stage_b = self.extract_match_info(match)

        return str(start_hour) + "時からのガチマッチのルールは" + rule + "、ステージは" + stage_a + "と" + stage_b + "です。"


class SearchedRuleTB(TextBuilder):
    RULE_NAMES = {
        "area": "ガチエリア",
        "yagura": "ガチヤグラ",
        "hoko": "ガチホコバトル",
        "asari": "ガチアサリ"
    }

    def build(self, **kwargs):
        rule_key = kwargs["rule"]
        idx = 1
        while True:
            match = self.extract_gachi_match(idx)
            rule, stage_a, stage_b = self.extract_match_info(match)
            if rule == self.RULE_NAMES[rule_key]:
                break
            else:
                idx += 1
        start_hour = self.extract_start_hour(match)
        return "次の" + rule + "は" + str(start_hour) + "時から、ステージは" + stage_a + "と" + stage_b + "です。"
