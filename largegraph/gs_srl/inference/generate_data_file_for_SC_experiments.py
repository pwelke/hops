import os,argparse

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run exhaustive approach')
    parser.add_argument('-train', help='path to train gpickle')
    parser.add_argument('-test', help='path to test gpickle')
    parser.add_argument('-o', help='output')
    parser.add_argument('-p', help='pattern path')
    parser.add_argument('-e', help='experiment: exact or furer')
    parser.add_argument('-const', help='constant for the target predicate. e.g., protein')
    parser.add_argument('-attr', help='attribute for the target predicate. e.g., function')
    parser.add_argument('-rT', help='root node target, e.g., function')
    parser.add_argument('-sT', help='start node target, e.g., 2')
    parser.add_argument('-max_time', default=600, type=int, help='start node target, e.g., 2')
    parser.add_argument('-output', help='output file')
    args = parser.parse_args()

    patterns_path= args.p
    results_path=args.o
    train=args.train
    test=args.test
    e=args.e
    const=args.const
    attr=args.attr
    rT=args.rT
    sT=args.sT
    max_time=args.max_time


    with open(args.output,'w') as f:
        f.write("train,test,o,e,p,const,attr,rT,sT,max_time\n")
        for dir in os.listdir(patterns_path):
            if not "pattern" in dir:
                continue
            p=os.path.join(patterns_path,dir)
            o=os.path.join(results_path,dir)
            f.write(train+","+test+","+o+","+e+","+p+","+const+","+attr+","+rT+","+str(sT)+","+str(max_time)+"\n")


