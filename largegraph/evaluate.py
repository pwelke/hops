import os
import matplotlib.pyplot as plt
import math
import pickle
import tikzplotlib
import numpy as np
import json




class Evaluation:

    def __init__(self, path, data_name="YEAST", pattern_size=15, use_extended_file=False, use_extended_eval=False):

        # name of the database
        self.data = data_name
        self.tree_pattern_size = pattern_size

        self.extended_file = use_extended_file
        self.extended_eval = use_extended_eval

        self.pattern_set = set()

        # Paths
        self.results_path = path + '/Results/'
        self.save_name = self.data + self.results_path.split("/")[-1] + "_"

        self.file_data = ()
        self.results = []

        # Results
        self.pattern_timeout = {}
        self.pattern_timeout_by_size = {}
        self.pattern_timeout_by_size = {'4': 0, '6': 0, '7': 0, '10': 0, '13': 0, '15': 0}
        self.num_of_patterns = 0
        self.results = {}
        self.extended_results = {}
        self.pattern_number = {}
        self.exact_results = {}

        # plot settings
        self.plot_algo = {"fk_TREE_results": "hoPS", "fk_OBD_results": "OBD", "fk_AD_results": "AD",
                          "random_results": "Random", "exhaustive_results": "Exact"}
        self.plot_color = {"fk_TREE_results": (166 / 255, 97 / 255, 26 / 255),
                           "fk_OBD_results": (223 / 255, 194 / 255, 125 / 255),
                           "fk_AD_results": (128 / 255, 205 / 255, 193 / 255),
                           "random_results": (1 / 255, 133 / 255, 113 / 255), "exhaustive_results": "g"}
        self.plot_marker = {"fk_TREE_results": "^", "fk_OBD_results": "s", "fk_AD_results": "o", "random_results": "D"}

        # reads the data generated from the experiments

    def read_results(self):
        # walk trough all folders in the results path
        for subdir, dirs, files in os.walk(self.results_path + self.data + '/'):
            for file in files:  # consider all patterns
                file_ending = file.split(".")[1]

                # there was a timeout by the exact algorithm
                if file == "timeout.info":
                    p_size = subdir.split("/")[-2].split("size")[-1]

                    if str(p_size) not in self.pattern_timeout_by_size:
                        self.pattern_timeout_by_size[str(p_size)] = 1
                    else:
                        self.pattern_timeout_by_size[str(p_size)] += 1
                    self.pattern_timeout[subdir.split("/")[-1]] = 1

                self.file_data = (
                    file, file.split(".")[0], subdir.split(self.results_path + self.data + "/")[1].split("/"),
                    subdir + "/" + file)

                # get results of the TREE, OBD, AD and random algorithm
                if "/monitoring" in subdir and file_ending == "info":
                    self.algos_results()

                # get results of the exhaustive algorithm
                elif file_ending == "res":
                    self.exhaustive_results()

                # get extended results such as every estimation of the algorithms for some pattern set
                if "results.out" in file and self.extended_eval:
                    print(subdir)
                    self.extended_algos_results(pattern_set=self.pattern_set)

        # Number of considered patterns without timeout pattern
        print(self.pattern_number, self.pattern_timeout_by_size)
        self.num_of_patterns = self.pattern_number[str(self.tree_pattern_size)] - self.pattern_timeout_by_size[
            str(self.tree_pattern_size)]

        # write the extended results to a file
        if self.extended_file:
            for k, v in self.extended_results.items():
                if '_'.join(k.split("_")[:2]) in self.pattern_timeout:
                    self.extended_results[k]["exact_result"] = -1
                else:
                    self.extended_results[k]["exact_result"] = self.exact_results['_'.join(k.split("_")[:2])]

            pickout = gzip.open(os.path.join(self.results_path, 'results_' + self.data + "_size" + str(
                self.tree_pattern_size) + '.pickle'), 'wb')
            pickle.dump(self.extended_results, pickout)
            pickout.close()

    def extended_eval(self):
        # do some extended evaluation
        if self.extended_eval:
            print(self.pattern_timeout)
            """
            path = self.results_path  + 'results_' + self.data + "_size" + str(self.tree_pattern_size) + '.txt'
            result_by_algo = {}
            num_by_algo = {}
            with open (path, 'r') as f_open:
                print(path)
                f_open = cPickle.load(f_open)
                print(path)
            """
            counter = 0
            for key, value in self.extended_results.items():
                if value["name"] in self.pattern_timeout and value["size"] == str(self.tree_pattern_size) and value[
                    "algo"] != "random_results":
                    print(value["name"], value["algo"], value["find_number"] / float(len(value["embedding_data"])))
                    if value["algo"] in result_by_algo:
                        result_by_algo[value["algo"]] += value["find_number"] / float(len(value["embedding_data"]))
                        num_by_algo[value["algo"]] += 1
                    else:
                        result_by_algo[value["algo"]] = value["find_number"] / float(len(value["embedding_data"]))
                        num_by_algo[value["algo"]] = 1
                    counter += 1
            print(counter)
            for key, value in result_by_algo.items():
                result_by_algo[key] = result_by_algo[key] / (counter / 3)
            print(result_by_algo)
            print(num_by_algo)

            # if "dblppattern_4a0e90d880ee4ff59ba24ff0cbfbea63" + "_" + "fk_AD_results" in f_open:
            # print(f_open["dblppattern_4a0e90d880ee4ff59ba24ff0cbfbea63" + "_" + "fk_AD_results"]["embedding_data"][0:1000])

    def algos_results(self):

        file, file_name, file_infos, file_path = self.file_data

        pattern_size = file_infos[0].split("_size")[-1]
        pattern_name = file_infos[1]
        algo = file_infos[2]
        res_time = file_name.split("_")[-1]

        sampling_iterations = 0
        std_deviation = 0
        observations = 0
        embeddings = 0

        with open(file_path, 'r') as f_open:
            file_text = f_open.readlines()
            if algo != "exhaustive_results":
                # print(file_text)
                sampling_iterations = int(file_text[16].split(":")[-1])
                embeddings = float(file_text[17].split(":")[-1])
                std_deviation = float(file_text[18].split(":")[-1])

                result_dict = {"size": pattern_size, "observations": observations, "embeddings": embeddings,
                               "sampling_iterations": sampling_iterations, "std_deviation": std_deviation}

                if algo in self.results:
                    if pattern_name in self.results[algo]:
                        self.results[algo][pattern_name][res_time] = result_dict
                    else:
                        self.results[algo][pattern_name] = {}
                        self.results[algo][pattern_name][res_time] = result_dict
                else:
                    self.results[algo] = {}
                    self.results[algo][pattern_name] = {}
                    self.results[algo][pattern_name][res_time] = result_dict

    def extended_algos_results(self, pattern_set=""):

        file, file_name, file_infos, file_path = self.file_data

        pattern_size = file_infos[0].split("_size")[-1]
        pattern_name = file_infos[1]
        algo = "_".join(file.split("_")[:2])
        res_time = file_name.split("_")[-1]

        sampling_iterations = 0
        std_deviation = 0
        observations = 0
        embeddings = 0

        if pattern_set == "" or pattern_name in pattern_set:
            with open(file_path, 'rb') as f_open:
                estimator_data = json.loads(f_open.read())
                embedding_data = []
                find_number = 0
                result_dict = {"db": self.data, "name": pattern_name, "size": pattern_size, "algo": algo, "path": file_path,
                               "embedding_data": embedding_data, "find_number": find_number}
                for x in range(1, len(estimator_data) + 1):
                    result_dict["embedding_data"].append(int(estimator_data[str(x)][0]))
                    if int(estimator_data[str(x)][0]) > 0:
                        result_dict["find_number"] += 1
                print(result_dict["algo"], len(result_dict["embedding_data"]), result_dict["find_number"])
                self.extended_results[str(pattern_name + "_" + algo)] = result_dict

    def exhaustive_results(self):

        file, file_name, file_infos, file_path = self.file_data

        pattern_size = file_infos[0].split("_size")[-1]
        pattern_name = file_infos[1]
        algo = file_infos[2]

        res_time = file_name.split("_")[-1]

        sampling_iterations = 0
        std_deviation = 0
        observations = 0
        embeddings = 0

        """
        The algorithm is the exhaustive
        """
        with open(file_path, 'r') as f_open:
            file_text = f_open.readlines()

            if algo == "exhaustive_results":
                time = int(file_text[0].split(" ")[-2])
                observations = int(file_text[1].split(":")[-1])
                embeddings = int(file_text[4].split(":")[-1])

                self.exact_results[pattern_name] = {"time": time, "embeddings": int(embeddings), "size": pattern_size}

                if str(pattern_size) in self.pattern_number:
                    self.pattern_number[str(pattern_size)] += 1
                else:
                    self.pattern_number[str(pattern_size)] = 1

    def plot_results_by_size(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title("Graph: " + self.data + ", Pattern size: " + str(self.tree_pattern_size))

        for algo, pattern_data in self.results.items():
            data = {}
            std_data = {}
            max_data = {}
            min_data = {}
            boxplot_data = {}
            for pattern, time_data in pattern_data.items():
                if pattern not in self.pattern_timeout.keys():
                    exact_number = self.exact_results[pattern]["embeddings"]
                    for time, value in time_data.items():
                        if value["size"] == str(self.tree_pattern_size):
                            if int(time) not in data:
                                rel_error = abs(value["embeddings"] - exact_number) / exact_number
                                data[int(time)] = (1 / float(self.num_of_patterns)) * rel_error
                                std_data[int(time)] = (1 / float(self.num_of_patterns)) * rel_error ** 2
                                max_data[int(time)] = rel_error
                                min_data[int(time)] = rel_error
                                boxplot_data[int(time)] = [rel_error]
                            else:
                                rel_error = abs(value["embeddings"] - exact_number) / exact_number
                                data[int(time)] += (1 / float(self.num_of_patterns)) * rel_error
                                std_data[int(time)] += (1 / float(self.num_of_patterns)) * rel_error ** 2
                                if rel_error > max_data[int(time)]:
                                    max_data[int(time)] = rel_error
                                if rel_error < min_data[int(time)]:
                                    min_data[int(time)] = rel_error
                                boxplot_data[int(time)].append(rel_error)

            for key, value in std_data.items():
                std_data[key] = math.sqrt(value)

            plot_keys = list(data.keys())
            plot_values = list(data.values())
            max_values = list(max_data.values())
            min_values = list(min_data.values())

            std_values = list(std_data.values())

            # plot average
            plt.plot([x for x, _ in sorted(zip(plot_keys, plot_values))],
                     [y for _, y in sorted(zip(plot_keys, plot_values))], label=self.plot_algo[algo], ls='-',
                     c=self.plot_color[algo], marker=self.plot_marker[algo], markersize=3)
            print([(x, y) for x, y in sorted(zip(plot_keys, plot_values))])
            #plt.boxplot(boxplot_data[2], sym='', positions=[2])
            # plot max
            # plt.plot([x for x,_ in sorted(zip(plot_keys, plot_values))], [y for _,y in sorted(zip(plot_keys, max_values))], label = self.plot_algo[algo], ls = '--', c = self.plot_color[algo], marker = self.plot_marker[algo], markersize = 3)
            # plot min
            # plt.plot([x for x,_ in sorted(zip(plot_keys, plot_values))], [y for _,y in sorted(zip(plot_keys, min_values))], label = self.plot_algo[algo], ls = '--', c = self.plot_color[algo], marker = self.plot_marker[algo], markersize = 3)
            # plot std
            y_std = []
            for x, y, z in zip(plot_keys, plot_values, std_values):
                #plt.plot([int(x), int(x)], [y, z], c=self.plot_color[algo], ls=':')
                #plt.plot([int(x)], [z], c=self.plot_color[algo], marker=self.plot_marker[algo], markersize=3)
                y_std.append((x, z))


            ax.fill_between([x for x, _ in sorted(zip(plot_keys, plot_values))],
                     [y for _, y in sorted(zip(plot_keys, plot_values))], [z for _, z in sorted(y_std, key=lambda tup: tup[0])], color=self.plot_color[algo], alpha = 0.3, zorder = 20, linewidth = 2)
                # plt.plot([int(x), int(x)], [y, max(2*y-z, 0)], c = self.plot_color[algo], ls = ':')
                # if 2*y-z > 0:
                # plt.plot([int(x)], [max(2*y-z, 0)], c = self.plot_color[algo], marker = self.plot_marker[algo])

            # plt.plot([x for x,_ in sorted(zip(plot_keys, plot_values))], [y for _,y in sorted(zip(plot_keys, std_values))], label = self.plot_algo[algo], ls = '-.', c = self.plot_color[algo], marker = self.plot_marker[algo], markersize = 3)
        ax.legend(ncol=4, bbox_to_anchor=(0.5, 0.85),
                  loc='lower center', fontsize='small')

        plt.xlabel("Runtime [s]")
        # plt.xticks([12, 24, 36, 48, 60], ["2%", "4%", "6%", "8%", "10%"])

        plt.ylabel("Relative Error")

        print(self.save_name)
        plt.savefig(self.save_name + 'size' + str(self.tree_pattern_size) + '.png', bbox_inches='tight')
        tikzplotlib.save(self.save_name + 'size' + str(self.tree_pattern_size) + ".tex", table_row_sep='\\\\')
        plt.show()

    def plot_results_by_algo(self, algo):
        algo = algo + "_results"

        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(
            "Graph: " + self.data + ", Pattern size: " + str(self.tree_pattern_size) + ", Algo: " + self.plot_algo[
                algo])

        for alg, pattern_data in self.results.items():
            if alg == algo:
                for pattern, time_data in pattern_data.items():
                    data = {}
                    if pattern not in self.pattern_timeout.keys():
                        exact_number = self.exact_results[pattern]["embeddings"]
                        for time, value in time_data.items():
                            if value["size"] == str(self.tree_pattern_size):
                                if int(time) not in data:
                                    data[int(time)] = abs(value["embeddings"] - exact_number) / exact_number

                        plt.plot(sorted(data.keys()), [y for _, y in sorted(zip(data.keys(), data.values()))],
                                 c=self.plot_color[algo], ls="-")
                        # plt.plot(sorted(data.keys()), data.values(), [y for _,y in sorted(zip(data.keys(), data.values()))], "b-")

        plt.xlabel("Runtime [s]")
        # plt.xticks([12, 24, 36, 48, 60], ["2%", "4%", "6%", "8%", "10%"])

        plt.ylabel("Relative Error")

        plt.savefig(self.save_name + 'size' + str(self.tree_pattern_size) + "_" + algo + '.png')
        tikzplotlib.save(self.save_name + 'size' + str(self.tree_pattern_size) + "_" + algo + '.tex',
                         table_row_sep='\\\\')
        plt.show()

    def plot_embedding_num_by_algo(self, algo):
        algo = algo + "_results"
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(
            "Graph: " + self.data + ", Pattern size: " + str(self.tree_pattern_size) + " Algo: " + self.plot_algo[algo])

        if algo == "exhaustive_results":
            for pattern, value in self.exact_results.items():
                if pattern not in self.pattern_timeout.keys():
                    color = self.plot_color[algo]
                else:
                    color = "r"
                plt.plot([0, 60], [value["embeddings"], value["embeddings"]], color)

        for alg, pattern_data in self.results.items():
            if alg == algo:
                for pattern, time_data in pattern_data.items():
                    data = {}
                    if pattern not in self.pattern_timeout.keys():
                        color = self.plot_color[algo]
                    else:
                        color = "r"
                    for time, value in time_data.items():
                        if value["size"] == str(self.tree_pattern_size):
                            if int(time) not in data:
                                data[int(time)] = value["embeddings"]

                    plt.plot(sorted(data.keys()), [y for _, y in sorted(zip(data.keys(), data.values()))], c=color)

            plt.xlabel("Runtime [s]")
            # plt.xticks([12, 24, 36, 48, 60], ["2%", "4%", "6%", "8%", "10%"])

            plt.ylabel("Number of Embeddings")

        plt.savefig(self.save_name + 'size' + str(self.tree_pattern_size) + "_" + algo + "_embeddingNum" + '.png')
        tikzplotlib.save(self.save_name + 'size' + str(self.tree_pattern_size) + "_" + algo + "_embeddingNum" + '.tex',
                         table_row_sep='\\\\')
        plt.show()

    def plot_by_param_dict(self, param="sampling_iterations"):
        fig, axs = plt.subplots(1, 4, sharey=True, tight_layout=True)
        fig.suptitle("Average of " + param, y=1.02)

        i = 0
        for algo, pattern_data in self.results.items():
            data = {}
            for pattern, time_data in pattern_data.items():
                if pattern not in self.pattern_timeout.keys():
                    exact_number = self.exact_results[pattern]["embeddings"]
                    for time, value in time_data.items():
                        if int(time) == 60:
                            if int(value["size"]) not in data:
                                data[int(value["size"])] = (1 / float((self.pattern_number[str(value["size"])] -
                                                                       self.pattern_timeout_by_size[
                                                                           str(value["size"])]))) * value[param]
                                data[int(value["size"])] += (1 / float((self.pattern_number[str(value["size"])] -
                                                                        self.pattern_timeout_by_size[
                                                                            str(value["size"])]))) * value[param]

            axs[i].plot(list(data.keys()), list(data.values()), self.plot_marker[algo], label=self.plot_algo[algo],
                        c=self.plot_color[algo])
            axs[i].set_title(self.plot_algo[algo], fontsize='small')
            axs[i].set_xlabel("pattern_size", fontsize='smaller')
            axs[i].set_xticks([4, 7, 10, 13, 15])
            i += 1
        plt.savefig(self.save_name + param + '.png', bbox_inches="tight")
        tikzplotlib.save(self.save_name + param + '.tex', table_row_sep='\\\\')
        plt.show()

    def plot_std_by_param_dict(self, param="std_deviation"):
        fig, axs = plt.subplots(1, 4, sharey=True, tight_layout=True)
        fig.suptitle("Average of " + param, y=1.02)

        i = 0
        for algo, pattern_data in self.results.items():
            data = {}
            for pattern, time_data in pattern_data.items():
                if pattern not in self.pattern_timeout.keys():
                    exact_number = self.exact_results[pattern]["embeddings"]
                    for time, value in time_data.items():
                        if int(time) == 60:
                            if int(value["size"]) not in data:
                                data[int(value["size"])] = (1 / float((self.pattern_number[str(value["size"])] -
                                                                       self.pattern_timeout_by_size[
                                                                           str(value["size"])]))) * abs(
                                    exact_number - value[param]) / float(exact_number)
                                data[int(value["size"])] += (1 / float((self.pattern_number[str(value["size"])] -
                                                                        self.pattern_timeout_by_size[
                                                                            str(value["size"])]))) * abs(
                                    exact_number - value[param]) / float(exact_number)

            axs[i].plot(list(data.keys()), list(data.values()), self.plot_marker[algo], label=self.plot_algo[algo],
                        c=self.plot_color[algo])
            axs[i].set_title(self.plot_algo[algo], fontsize='small')
            axs[i].set_xlabel("pattern_size", fontsize='smaller')
            axs[i].set_xticks([4, 7, 10, 13, 15])
            i += 1
        plt.savefig(self.save_name + "_" + param + '.png', bbox_inches="tight")
        tikzplotlib.save(self.save_name + param + '.tex', table_row_sep='\\\\')
        plt.show()

    def plot_histogramm(self, algos, with_zeros=False, pattern=""):
        x_histo = {}
        for algo in algos:
            x_histo[algo + "_results"] = []
        for k, v in self.extended_results.items():
            pattern_key = '_'.join(k.split("_")[:2])
            algo_key = '_'.join(k.split("_")[2:-1])
            if algo_key in algos:
                if (pattern == "" or pattern == pattern_key):
                    embedding_data = v["embedding_data"]
                    for x in embedding_data:
                        if not with_zeros:
                            if x != 0:
                                x_histo[v["algo"]].append(x)
                        else:
                            x_histo[v["algo"]].append(x)

        n_bins = 1000
        fig, axs = plt.subplots(1, len(algos), sharey=True, tight_layout=True)
        for i, algo in enumerate(algos, 0):
            axs[i].hist(x_histo[algo + "_results"], bins=n_bins)
            axs[i].set_xlabel(algo)
        plt.show()

    def avg_time_exhaustive(self, pattern_size):
        result = 0
        std_var = 0
        num = self.pattern_number[str(pattern_size)] - self.pattern_timeout_by_size[str(pattern_size)]
        for key, value in self.exact_results.items():
            if key not in self.pattern_timeout and value["size"] == str(pattern_size):
                result += 1 / float(num) * value["time"]

        for key, value in self.exact_results.items():
            if key not in self.pattern_timeout and value["size"] == str(pattern_size):
                std_var += 1 / (float(num)) * (value["time"] - result) ** 2
        return result, np.sqrt(std_var)

    def avg_stddev_exhaustive(self, value_key, pattern_size):
        result = 0
        std_var = 0
        num = self.pattern_number[str(pattern_size)] - self.pattern_timeout_by_size[str(pattern_size)]
        for key, value in self.exact_results.items():
            if key not in self.pattern_timeout and value["size"] == str(pattern_size):
                print(key, value[value_key])
                result += 1 / float(num) * value[value_key]

        for key, value in self.exact_results.items():
            if key not in self.pattern_timeout and value["size"] == str(pattern_size):
                std_var += 1 / (float(num)) * (value[value_key] - result) ** 2
                # print(value[value_key], result)
        return str(result) + "(+-" + str(np.sqrt(std_var)) + ")"

    def pattern_set_of_size(self, size):
        pattern_set = set()
        for subdir, dirs, files in os.walk(self.results_path + self.data + '/'):
            if "pattern_size" + str(size) in subdir:
                pattern_name = subdir.split("/")[-1]
                if "pattern" in pattern_name:
                    pattern_set.add(pattern_name)

        return pattern_set

    def Table2(self):
        print("Table2 pat. size", self.tree_pattern_size)
        print("Table2 finished(total)",
              str(self.num_of_patterns) + "(" + str(self.pattern_number[str(self.tree_pattern_size)]) + ")")
        print("Table2 Time", self.avg_stddev_exhaustive("time", self.tree_pattern_size))
        print("Table2 Embeddings", self.avg_stddev_exhaustive("embeddings", self.tree_pattern_size))

    def Table3(self):
        # do some extended evaluation
        if self.extended_eval:
            print(self.pattern_timeout)
            result_by_algo = {}
            num_by_algo = {}
            """
            path = self.results_path  + 'results_' + self.data + "_size" + str(self.tree_pattern_size) + '.txt'

            with open (path, 'r') as f_open:
                print(path)
                f_open = cPickle.load(f_open)
                print(path)
            """

            ###iterations
            counter = 0
            for key, value in self.extended_results.items():
                print(key)
                print(value["algo"], len(value["embedding_data"]), value["find_number"])
                if value["name"] not in self.pattern_timeout and value["size"] == str(self.tree_pattern_size):
                    exact = self.exact_results[value["name"]]["embeddings"]
                    factor = (1 / float(self.num_of_patterns))
                    average = sum([x for x in value["embedding_data"]]) / len(value["embedding_data"])
                    if value["algo"] + "_not_null" in result_by_algo:
                        result_by_algo[value["algo"] + "_not_null"] += factor * value["find_number"]
                        result_by_algo[value["algo"] + "_iterations"] += factor * len(value["embedding_data"])
                        result_by_algo[value["algo"] + "_success_rate"] += factor* result_by_algo[value["algo"] + "_not_null"] / \
                                                                          result_by_algo[value["algo"] + "_iterations"]
                        result_by_algo[value["algo"] + "_error"] += factor * abs(average - exact) / float(exact)
                        #result_by_algo[value["algo"] + "_rel_std_dev"] += factor * math.sqrt(
                        #    1. / len(value["embedding_data"]) * sum(
                        #        [((x - exact) / float(exact)) ** 2 for x in value["embedding_data"]]))
                        result_by_algo[value["algo"] + "_counter"] += 1
                        result_by_algo[value["algo"] + "_std_dev"] += factor * (abs(average - exact) / float(exact))**2
                    else:
                        result_by_algo[value["algo"] + "_not_null"] = factor * value["find_number"]
                        result_by_algo[value["algo"] + "_iterations"] = factor * len(value["embedding_data"])
                        result_by_algo[value["algo"] + "_success_rate"] = factor* result_by_algo[value["algo"] + "_not_null"] / \
                                                                          result_by_algo[value["algo"] + "_iterations"]
                        result_by_algo[value["algo"] + "_error"] = factor * abs(average - exact) / float(exact)
                        #result_by_algo[value["algo"] + "_rel_std_dev"] = factor * math.sqrt(
                        #    1. / len(value["embedding_data"]) * sum(
                        #        [((x - exact) / float(exact)) ** 2 for x in value["embedding_data"]]))
                        result_by_algo[value["algo"] + "_counter"] = 1
                        result_by_algo[value["algo"] + "_std_dev"] = factor * (abs(average - exact) / float(exact))**2
            for algo in ["fk_TREE", "fk_AD", "fk_OBD"]:
                result_by_algo[algo + "_std_dev"] = math.sqrt(result_by_algo[algo + "_std_dev"])
            print(result_by_algo)
            """                     

                    print()
                    print(value["name"], value["algo"], value["find_number"]/float(len(value["embedding_data"])))
                    if value["algo"] in result_by_algo:
                        result_by_algo[value["algo"]] += value["find_number"]/float(len(value["embedding_data"]))
                        num_by_algo[value["algo"]] += 1
                    else:
                        result_by_algo[value["algo"]] = value["find_number"]/float(len(value["embedding_data"]))
                        num_by_algo[value["algo"]] = 1
                    counter += 1
            print(counter)
            for key, value in result_by_algo.items():
                result_by_algo[key] = result_by_algo[key]/(counter/3)
            print(result_by_algo)
            print(num_by_algo)
            """

    def PaperEvaluation(self):
        # Define some pattern set for extended evaluations
        self.pattern_set = self.pattern_set_of_size(self.tree_pattern_size)
        # Read experimental results
        self.read_results()

        self.Table2()

        self.Table3()

        # Plot average over all patterns (compare the algorithms)
        self.plot_results_by_size()


        
        # Plot for one algorithm, pattern-wise evaluation of correctness
        for algorithm in ["fk_TREE", "fk_OBD", "fk_AD", "random"]:
            self.plot_results_by_algo(algorithm)

        # Plot for one algorithm, pattern-wise evaluation of estimated embedding number
        for algorithm in ["exhaustive", "fk_TREE", "fk_OBD", "fk_AD", "random"]:
            self.plot_embedding_num_by_algo(algorithm)

        # Plot of average of some parameter of all patterns of some size for some algorithm
        #Get the average over param for std and sampling iterations
        self.plot_std_by_param_dict()

        self.plot_by_param_dict()

        #Get the histogramm over all estimated embeddings
        # self.plot_histogramm(["fk_TREE", "fk_OBD", "fk_AD"])
        

def main():
    """
    Evaluate the experiments of the hoPS paper
    path: path of the output of the experiments
    data_name: data to run the evaluation from the output of the experiments [YEAST, DBLP, IMDB, WEBKB, FACEBOOK, AMAZON]
    pattern_size: size of the evaluated patterns
    use_extended_eval: extended evaluations (needs extended run of experiments and generates extended data, see paper)
    """

    
    #Settings used for paper evaluation
    path = "/home/.../largegraph/HopsExperiments/Experiments" #TODO set your path
    ext = "10h"
    for val in [("YEAST", 15), ("WEBKB",  10), ("DBLP",  10), ("FACEBOOK",  10)]:
        evaluate = Evaluation(path=path + val[0] + ext, data_name=val[0], pattern_size=val[1], use_extended_eval=False)
        evaluate.PaperEvaluation()

if __name__ == "__main__":
    main()
