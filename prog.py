import argparse, os, collections, math

parser = argparse.ArgumentParser(description='Utility that will detect encrypted/compressed files in a specified directory.',
                                formatter_class = argparse.ArgumentDefaultsHelpFormatter, prefix_chars='-+',
                                allow_abbrev=False)

parser.add_argument('-d', '--dir', default='./',
                    help='specifies the path to directory where to look for encrypted/compressed files.')
parser.add_argument('-c', '--confidence', default=80, type=int,
                    help='specifies the threshold level of confidence to treat a certain file as encryped/compressed.')
parser.add_argument('-p', '--print-confidence', action='store_true',
                    help='print the confidence level along with the file name.')
parser.add_argument('-s', dest='descending', action='store_true',
                    help='all files in the program output should be sorted by confidence level descending.')
parser.add_argument('+s', dest='ascending', action='store_true',
                    help='all files in the program output should be sorted by confidence level ascending.')

args = parser.parse_args()
dir = args.dir
more_then_confidence = args.confidence
dic = {}

for file in os.listdir(dir):
    if os.path.isfile(file):
        f = open(dir+file, 'rb')
        read_f = f.read()
        m = len(read_f)
        bases = collections.Counter([tmp_base for tmp_base in read_f])
        ent = 0
        for base in bases:
            n_i = bases[base]
            p_i = n_i / float(m)
            entropy_i = p_i * (math.log(p_i, 2))
            ent += -(entropy_i)
        print(ent)
        confidence = round(ent/8*100)
        if args.confidence:
            if confidence >= more_then_confidence:
                dic[file]= confidence

def sort():
    new_dic = {x: y for x, y in sorted(dic.items(), key=lambda item: item[1])}
    return new_dic

def reverse_sort():
    new_dic = {x: y for x, y in sorted(dic.items(), key=lambda item: item[1], reverse=True)}
    return new_dic

def output(dictation):
    for key in dictation.keys():
        print('\n{0}'.format(key, dictation[key]), end = ' ')

def output_with_conf(dictation):
    for key in dictation.keys():
        print('\n{1}% {0}'.format(key, dictation[key]), end = ' ')

if args.print_confidence and args.descending:
    sort_dic = reverse_sort()
    output_with_conf(sort_dic)
elif args.print_confidence and args.ascending:
    sort_dic = sort()
    output_with_conf(sort_dic)
elif args.descending:
    sort_dic = reverse_sort()
elif args.ascending:
    sort_dic = sort()
    output()
elif args.print_confidence == True:
    output_with_conf(dic)
else:
    output(dic)


