import pandas as pd
import json
import os

RULES_PATH = "config/rules.json"

class Transformer:
    def __init__(self):
        self.rules = self.load_rules()

    def load_rules(self):
        with open(RULES_PATH, "r") as f:
            return json.load(f)

    def apply_transformations(self, input_df, ref_df):
        merged_df = input_df.merge(ref_df, on=["refkey1", "refkey2"], how="left")
        merged_df["outfield1"] = merged_df["field1"] + merged_df["field2"]
        merged_df["outfield2"] = merged_df["refdata1"]
        merged_df["outfield3"] = merged_df["refdata2"] + merged_df["refdata3"]
        merged_df["outfield5"] = merged_df[["field5", "refdata4"]].max(axis=1)
        merged_df["outfield4"] = merged_df["field3"] * merged_df["outfield5"]
        return merged_df[["outfield1", "outfield2", "outfield3", "outfield4", "outfield5"]]
