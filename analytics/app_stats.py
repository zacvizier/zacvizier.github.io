
# Create empty Stats array
# -- Stats includes details for every column in the BT Log
stats = [
    {
        "name": "env",
        "val": "Env",
        "checkedOptions": [{'dataVal': 'R', 'val': 'R'}, {'dataVal': 'T', 'val': 'T'}, {'dataVal': 'PB', 'val': 'PB'}],
        "plays": [2.1,2.2,3.1,3.6,4.8,5.8,7.2,7.3],
        "data": [
            {"checked": 'R', "w": 0, "l": 0},
            {"checked": 'T', "w": 0, "l": 0},
            {"checked": 'PB', "w": 0, "l": 0}]
    },
    {
        "name": "strmv",
        "val": "StrMv",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "plays": [2.1,2.2,3.1,3.6,4.8,5.8,7.2,7.3],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "imp sr",
        "val": "Imp SR",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "plays": [2.1,2.2,3.1,3.6,4.8,5.8,7.2,7.3],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "tr sr",
        "val": "Tr SR",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "plays": [2.1,2.2,3.1,3.6,4.8,5.8,7.2,7.3],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "mjr sr",
        "val": "Mjr SR",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "mnr sr",
        "val": "Minor SR",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "nmf",
        "val": "NMF",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "dp",
        "val": "DP",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "mdp",
        "val": "m DP",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "trpb1",
        "val": "Tr Pb 1",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "trpb2",
        "val": "Tr PB 2",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "imppb1",
        "val": "Imp PB 1",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "imppb2",
        "val": "Imp PB 2",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "50-100",
        "val": "50 - 100",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "100-200",
        "val": "100 - 200",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "1pb+",
        "val": "1PB+EMA",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "2pb+",
        "val": "2PB+EMA",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "hllh",
        "val": "HLLH",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "pbvall",
        "val": "PB Vall",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "vrev",
        "val": "V Rev",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "cons1",
        "val": "Cons Pk 1",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "cons2",
        "val": "Cons Pk 2",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "1pbwkr",
        "val": "1st PB Wkr",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "2pbwkr",
        "val": "2nd PB Wkr",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "deep",
        "val": "Deep",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "impls",
        "val": "Impls",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "val dp",
        "val": "Val DP",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "cons",
        "val": "Cons",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "long",
        "val": "Long",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "ins wk",
        "val": "Inside / Wk",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "alr bopb",
        "val": "Alr BOPB",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "50",
        "val": "50",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "100",
        "val": "100",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "200",
        "val": "200",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "impe",
        "val": "ImpE",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "norm",
        "val": "NoRm 2 HL",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "imrej",
        "val": "ImRej",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    # {
    #     "name": "exe",
    #     "val": "ExE",
    #     "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
    #     "data": [
    #         {"checked": 'y', "w": 0, "l": 0},
    #         {"checked": 'n', "w": 0, "l": 0}]
    # },
    # {
    #     "name": "better entry",
    #     "val": "Better Entry",
    #     "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
    #     "data": [
    #         {"checked": 'y', "w": 0, "l": 0},
    #         {"checked": 'n', "w": 0, "l": 0}]
    # },
    # {
    #     "name": "rec",
    #     "val": "Rec",
    #     "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
    #     "data": [
    #         {"checked": 'y', "w": 0, "l": 0},
    #         {"checked": 'n', "w": 0, "l": 0}]
    # },
    # {
    #     "name": "both",
    #     "val": "Both",
    #     "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
    #     "data": [
    #         {"checked": 'y', "w": 0, "l": 0},
    #         {"checked": 'n', "w": 0, "l": 0}]
    # },
    # {
    #     "name": "close ema",
    #     "val": "Close EMA",
    #     "checkedOptions": [{'dataVal': 'W', 'val': 'W'}, {'dataVal': 'L', 'val': 'L'}, {'dataVal': 'NA', 'val': 'NA'}, {'dataVal': '', 'val': 'L'}],
    #     "data": [
    #         {"checked": 'W', "w": 0, "l": 0},
    #         {"checked": 'L', "w": 0, "l": 0},
    #         {"checked": 'NA', "w": 0, "l": 0}]
    # },
    # {
    #     "name": "far ema",
    #     "val": "Far EMA",
    #     "checkedOptions": [{'dataVal': 'W', 'val': 'W'}, {'dataVal': 'L', 'val': 'L'}, {'dataVal': 'NA', 'val': 'NA'}, {'dataVal': '', 'val': 'L'}],
    #     "data": [
    #         {"checked": 'W', "w": 0, "l": 0},
    #         {"checked": 'L', "w": 0, "l": 0},
    #         {"checked": 'NA', "w": 0, "l": 0}]
    # },
    {
        "name": "ins",
        "val": "Ins",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "hl",
        "val": "HL",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "slight past",
        "val": "Slight Past HL",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
    {
        "name": "past hl",
        "val": "Past HL",
        "checkedOptions": [{'dataVal': True, 'val': 'y'}, {'dataVal': False, 'val': 'n'}],
        "data": [
            {"checked": 'y', "w": 0, "l": 0},
            {"checked": 'n', "w": 0, "l": 0}]
    },
]