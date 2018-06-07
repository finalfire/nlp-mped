import argparse
import sys

def parse(r, t1, t2, t3):
    return t1(r[0]), t2(r[1]), t3(r[2])

def create_vocabulary(file_path):
    with open(file_path) as infile:
        data = [parse(l.strip().split(' '), int, str, int) for l in infile]
    return {w_id : w for w_id, w, _ in data}

def parse_matching(v1, v2, path_m, t=0.0):
    with open(path_m) as infile:
        data = [parse(l.strip().split(' '), int, int, float) for l in infile]
    
    # l'ordine è importante per v1 e v2
    matchings = list()
    for en_id, it_id, m in data:
        if m >= t:
            e = list()
            e.append(v1[en_id] if en_id in v1.keys() else 'NULL')
            e.append(v2[it_id] if it_id in v2.keys() else 'NULL')
            e.append(m)
            matchings.append(e)
    
    return matchings


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parser for GIZA++ files.')
    parser.add_argument('-en', help="Path of the english vocabulary file.", required=True)
    parser.add_argument('-it', help="Path of the italian vocabulary file.", required=True)
    parser.add_argument('-m', help='Path of the matching resulting from GIZA++.', required=True)
    parser.add_argument('-t', type=float, default=0.0, help="Threshold (if not present, all values are returned).")
    args = parser.parse_args()

    path_voc_1 = args.en    # train.en.vcb
    path_voc_2 = args.it    # train.ita.vcb
    path_match = args.m     # t3.final

    voc_1 = create_vocabulary(path_voc_1)
    voc_2 = create_vocabulary(path_voc_2)
    result = parse_matching(voc_1, voc_2, path_match, args.t)

    for r in result:
        print(' '.join(map(str, r)))