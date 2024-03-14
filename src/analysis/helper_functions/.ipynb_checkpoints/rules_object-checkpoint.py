"""
Associative rule mining on a list of itemsets (groups)
"""
from collections import defaultdict
from itertools import combinations
from operator import itemgetter
from typing import Any, Iterable

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from scipy.stats import chi2


class AssociativeRules:
    def __init__(
        self,
        groups: Iterable[Any],
        order=False,
        threshold=None,
        min_count=None,
        rule_filter="chi_squared",
    ):
        self.groups = groups
        self.order = order
        self.threshold = threshold
        self.min_count = min_count
        self.rule_filter = rule_filter
        self.nsets = len(groups)
        self.rules = {}
        self.pair_counts = defaultdict(int)
        self.item_counts = defaultdict(int)
        self.mean_item_count = None
        self.list_of_rules = []

    def update_pair_counts(self, itemset):
        """
        Updates the dictionary of pair counts for
        all pairs of items in a given itemset.
        """
        assert type(self.pair_counts) is defaultdict

        # check each combination of 2 items from the itemset
        for a, b in combinations(itemset, 2):
            self.pair_counts[(a, b)] += 1
            if self.order is False:
                self.pair_counts[(b, a)] += 1  # if order DOES NOT matter

    def update_item_counts(self, itemset):
        """
        Updates the dictionary of item counts for
        all items in a given itemset.
        """
        for i in itemset:
            self.item_counts[i] += 1

    def filter_rules_by_conf(self):
        """
        For a given combination of 2 items from an itemset, (item_a, item_b),
        calculates conf, the confidence that (item_a => item_b).
        If conf > threshold and a occurs more than min_count times,
        add rule to the dictionary
        """

        for (a, b) in self.pair_counts.keys():
            assert a in self.item_counts
            conf = self.pair_counts[(a, b)] / self.item_counts[a]
            has_reached_threshold = conf >= self.threshold
            has_minimum_count = self.item_counts[a] >= self.min_count
            if has_reached_threshold and has_minimum_count:
                self.rules[(a, b)] = conf

    def filter_rules_by_chi2(self, level):
        """
        For a given combination of 2 items from an itemset, (item_a, item_b),
        Calculates the X^2  test statistic for each pair of items.
        If larger than the cutoff X^2 for 1dof and 99% default
        significance level, reject independence assumption and add to rule list
        Reference---- ICDM 2006: Advances in Data Mining. Applications in
        Medicine, Web Mining, Marketing, Image and Signal Mining pp 202-216
        """
        assert 1 >= level > 0

        dof = 1  # 1 degree of freedom
        for (a, b) in self.pair_counts.keys():
            assert a in self.item_counts
            assert b in self.item_counts
            # calculate supports
            s_a = self.item_counts[a] / self.nsets
            s_b = self.item_counts[b] / self.nsets
            s_ab = self.pair_counts[(a, b)] / self.nsets
            # calculate chi^2
            try:
                tstat = self.nsets * (s_ab - s_a * s_b) ** 2 / (s_a * s_b * (1 - s_a) * (1 - s_b))
                cdf = chi2.cdf(tstat, dof)
                if cdf >= level and self.item_counts[a] >= self.min_count:
                    self.rules[(a, b)] = cdf

            except ZeroDivisionError:
                print("ZeroDivisionError", a, b, s_a, s_b, s_ab)

    def find_assoc_rules(self, level=0.99):
        """
        Using update_pair_counts, update_item_counts and desired rule filter
        (filter_rules_by_conf or filter_rules_by_chi2),
        Rules are extracted from the inputted groups
        If filtering by chi^2, can specify a confidence level
        in the range (0,1). The default is 0.99.
        """

        for itemset in self.groups:
            self.update_pair_counts(itemset)
            self.update_item_counts(itemset)

        if len(self.item_counts) > 0:
            self.mean_item_count = sum(self.item_counts.values()) / len(self.item_counts.values())
        else:
            raise ValueError(
                "No items in groups. Ensure you have processed data via the pipeline prior to running analysis."
            )

        # if a value is not given for min_count use mean_item_count
        if not self.min_count:
            self.min_count = self.mean_item_count

        if self.rule_filter == "conf":
            # print('filtering by conf')
            self.filter_rules_by_conf()
        else:
            # print('filtering by chi2 to significance level of ', level)
            self.filter_rules_by_chi2(level)

        ordered_rules = sorted(self.rules.items(), key=itemgetter(1), reverse=True)
        # print(ordered_rules)
        for (a, b), statistic_ab in ordered_rules:
            self.list_of_rules.append([a, b, statistic_ab])

    def gen_rule_str(self, a, b, val=None, val_fmt="{:.3f}", sep=" = "):
        text = "{} => {}".format(a, b)
        if val:
            text = self.rule_filter + "(" + text + ")"
            text += sep + val_fmt.format(val)
        return text

    def print_rules(self):
        if type(self.rules) is dict or type(self.rules) is defaultdict:

            ordered_rules = sorted(self.rules.items(), key=itemgetter(1), reverse=True)
        else:  # Assume rules is iterable
            ordered_rules = [((a, b), None) for a, b in self.rules]
        for (a, b), statistic_ab in ordered_rules:
            print(self.gen_rule_str(a, b, statistic_ab))

    def draw_graph(self, method="nx"):

        df = pd.DataFrame(self.list_of_rules, columns=["source", "target", "conf"])
        G = nx.from_pandas_edgelist(
            df,
            source="source",
            target="target",
            edge_attr="conf",
            create_using=nx.DiGraph,
        )
        if method == "nx":
            nx.draw_networkx(G)
            plt.axis("off")
            plt.savefig("rule_mining.png")
        if method == "ipycytoscape":  # for jupyter notebooks
            import ipycytoscape

            directed = ipycytoscape.CytoscapeWidget()
            directed.graph.add_graph_from_networkx(G, directed=True)

            directed.set_style(
                [
                    {
                        "selector": "node",
                        "css": {
                            "content": "data(id)",
                            "text-valign": "center",
                            "color": "white",
                            "text-outline-width": 2,
                            "text-outline-color": "blue",
                            "text-wrap": "wrap",
                            "text-max-width": "10px",
                            "text-overflow-wrap": "whitespace",
                            "background-color": "blue",
                        },
                    },
                    {
                        "selector": "edge",
                        "css": {
                            "mid-target-arrow-shape": "triangle",
                            "mid-target-arrow-fill": "filled",
                            "arrow-scale": 2,
                        },
                    },
                ]
            )

            directed.set_layout(name="cose", nodeOverlap=40, idealEdgeLength=60)
            return directed
