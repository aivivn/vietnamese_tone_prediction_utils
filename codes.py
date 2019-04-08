CODE_DICT = {
    'xe0': ['af', 'a2'],
    'xe1': ['as', 'a1'],
    'u1ea3': ['ar', 'a3'],
    'xe3': ['ax', 'a4'],
    'u1ea1': ['aj', 'a5'],
    'u0103': ['aw', 'a8'],
    'u1eb1': ['awf', 'a82'],
    'u1eaf': ['aws', 'a81'],
    'u1eb3': ['awr', 'a83'],
    'u1eb5': ['awx', 'a84'],
    'u1eb7': ['awj', 'a85'],
    'xe2': ['aa', 'a6'],
    'u1ea7': ['aaf', 'a62'],
    'u1ea5': ['aas', 'a61'],
    'u1ea9': ['aar', 'a63'],
    'u1eab': ['aax', 'a64'],
    'u1ead': ['aaj', 'a65'],
    'u0111': ['dd', 'd9'],
    'xe8': ['ef', 'e2'],
    'xe9': ['es', 'e1'],
    'u1ebb': ['er', 'e3'],
    'u1ebd': ['ex', 'e4'],
    'u1eb9': ['ej', 'e5'],
    'xea': ['ee', 'e6'],
    'u1ec1': ['eef', 'e62'],
    'u1ebf': ['ees', 'e61'],
    'u1ec3': ['eer', 'e63'],
    'u1ec5': ['eex', 'e64'],
    'u1ec7': ['eej', 'e65'],
    'xec': ['if', 'i2'],
    'xed': ['is', 'i1'],
    'u1ec9': ['ir', 'i3'],
    'u0129': ['ix', 'i4'],
    'u1ecb': ['ij', 'i5'],
    'xf2': ['of', 'o2'],
    'xf3': ['os', 'o1'],
    'u1ecf': ['or', 'o3'],
    'xf5': ['ox', 'o4'],
    'u1ecd': ['oj', 'o5'],
    'xf4': ['oo', 'o6'],
    'u1ed3': ['oof', 'o62'],
    'u1ed1': ['oos', 'o61'],
    'u1ed5': ['oor', 'o63'],
    'u1ed7': ['oox', 'o64'],
    'u1ed9': ['ooj', 'o65'],
    'u01a1': ['ow', 'o7'],
    'u1edd': ['owf', 'o72'],
    'u1edb': ['ows', 'o71'],
    'u1edf': ['owr', 'o73'],
    'u1ee1': ['owx', 'o74'],
    'u1ee3': ['owj', 'o75'],
    'xf9': ['uf', 'u2'],
    'xfa': ['us', 'u1'],
    'u1ee7': ['ur', 'u3'],
    'u0169': ['ux', 'u4'],
    'u1ee5': ['uj', 'u5'],
    'u01b0': ['uw', 'u7'],
    'u1eeb': ['uwf', 'u72'],
    'u1ee9': ['uws', 'u71'],
    'u1eed': ['uwr', 'u73'],
    'u1eef': ['uwx', 'u74'],
    'u1ef1': ['uwj', 'u75'],
    'u1ef3': ['yf', 'y2'],
    'xfd': ['ys', 'y1'],
    'u1ef7': ['yr', 'y3'],
    'u1ef9': ['yx', 'y4'],
    'u1ef5': ['yj', 'y5'],
    'xc0': ['AF', 'A2'],
    'xc1': ['AS', 'A1'],
    'u1ea2': ['AR', 'A3'],
    'xc3': ['AX', 'A4'],
    'u1ea0': ['AJ', 'A5'],
    'u0102': ['AW', 'A8'],
    'u1eb0': ['AWF', 'A82'],
    'u1eae': ['AWS', 'A81'],
    'u1eb2': ['AWR', 'A83'],
    'u1eb4': ['AWX', 'A84'],
    'u1eb6': ['AWJ', 'A85'],
    'xc2': ['AA', 'A6'],
    'u1ea6': ['AAF', 'A62'],
    'u1ea4': ['AAS', 'A61'],
    'u1ea8': ['AAR', 'A63'],
    'u1eaa': ['AAX', 'A64'],
    'u1eac': ['AAJ', 'A65'],
    'u0110': ['DD', 'D9'],
    'xc8': ['EF', 'E2'],
    'xc9': ['ES', 'E1'],
    'u1eba': ['ER', 'E3'],
    'u1ebc': ['EX', 'E4'],
    'u1eb8': ['EJ', 'E5'],
    'xca': ['EE', 'E6'],
    'u1ec0': ['EEF', 'E62'],
    'u1ebe': ['EES', 'E61'],
    'u1ec2': ['EER', 'E63'],
    'u1ec4': ['EEX', 'E64'],
    'u1ec6': ['EEJ', 'E65'],
    'xcc': ['IF', 'I2'],
    'xcd': ['IS', 'I1'],
    'u1ec8': ['IR', 'I3'],
    'u0128': ['IX', 'I4'],
    'u1eca': ['IJ', 'I5'],
    'xd2': ['OF', 'O2'],
    'xd3': ['OS', 'O1'],
    'u1ece': ['OR', 'O3'],
    'xd5': ['OX', 'O4'],
    'u1ecc': ['OJ', 'O5'],
    'xd4': ['OO', 'O6'],
    'u1ed2': ['OOF', 'O62'],
    'u1ed0': ['OOS', 'O61'],
    'u1ed4': ['OOR', 'O63'],
    'u1ed6': ['OOX', 'O64'],
    'u1ed8': ['OOJ', 'O65'],
    'u01a0': ['OW', 'O7'],
    'u1edc': ['OWF', 'O72'],
    'u1eda': ['OWS', 'O71'],
    'u1ede': ['OWR', 'O73'],
    'u1ee0': ['OWX', 'O74'],
    'u1ee2': ['OWJ', 'O75'],
    'xd9': ['UF', 'U2'],
    'xda': ['US', 'U1'],
    'u1ee6': ['UR', 'U3'],
    'u0168': ['UX', 'U4'],
    'u1ee4': ['UJ', 'U5'],
    'u01af': ['UW', 'U7'],
    'u1eea': ['UWF', 'U72'],
    'u1ee8': ['UWS', 'U71'],
    'u1eec': ['UWR', 'U73'],
    'u1eee': ['UWX', 'U74'],
    'u1ef0': ['UWJ', 'U75'],
    'u1ef2': ['YF', 'Y2'],
    'xdd': ['YS', 'Y1'],
    'u1ef6': ['YR', 'Y3'],
    'u1ef8': ['YX', 'Y4'],
    'u1ef4': ['YJ', 'Y5'],
    }