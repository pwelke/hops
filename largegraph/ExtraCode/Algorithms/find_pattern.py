import os
import glob

def main():
    pathA = '/home/PathA'
    pathB = '/home/PathB'
    pat_list = []
    path_list =[]
    for y in glob.glob(pathB + '/*.gml'):
        print(y)
        path_list.append(y)
        z = y.split("/")[-1].split(".")[0]
        pat_list.append(z)
    for x, y, z in os.walk(pathA):
        if("fk_TREE_resultsresults.out" in z):
            print(x + ".gml")
            z = x.split("/")[-1]
            path_list.remove("/home/.../" + z + ".gml")
            pat_list.remove(z)

    print(pat_list)
    print(path_list)



if __name__ == "__main__":
    main()
