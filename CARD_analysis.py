import pandas as pd
import argparse


class ARG(object):
    def __init__(self):
        self.count = 1
        self.drug_class = []
        self.AMR = []


class CARD(object):
    def __init__(self, args):
        """
        This will become the .txt file that CARD outputs
        """
        self.input_file = args.inp
        self.output_file = args.outp
        self.df = CARD.extract_args(self.input_file)

        self.create_output()

    def create_output(self):
        """
        Create the output - all the antibiotic resitance genes, their instances, and the
        unique drug mechanisms
        """
        col = ["AMR Gene Family", "Count", "Resistance Mechanisms", "Drug Class(es)"]
        rows = []
        for keys in self.df:
            rest_mech = keys
            count = self.df[rest_mech].count
            drug_class = self.df[rest_mech].drug_class
            AMR_GF = self.df[rest_mech].AMR
            # print("{}, {}, {}, {}".format(, count, drug_class, rest_mech))

            input_row = [AMR_GF, count, rest_mech, drug_class]
            rows.append(input_row)

        df_out = pd.DataFrame(rows, columns=col)
        df_out.to_csv(self.output_file, sep="\t")

    @staticmethod
    def extract_args(input_file):
        df = pd.read_csv(input_file, sep="\t", usecols=[14, 15, 16])
        instances = len(df.index)
        df_dic = {}
        i = 0

        while i < instances:
            d_class = str(df.iloc[i, 0])
            AMR_GF = str(df.iloc[i, 1])
            rest_mech = str(df.iloc[i, 2])

            if rest_mech in df_dic:
                df_dic[rest_mech].count += 1
                if d_class not in df_dic[rest_mech].drug_class:
                    # print(df_dic[AMR_GF].drug_class, d_class)
                    df_dic[rest_mech].drug_class.append(d_class)
                if AMR_GF not in df_dic[rest_mech].AMR:
                    # print(df_dic[AMR_GF].resistance_mechanism, rest_mech)
                    df_dic[rest_mech].AMR.append(AMR_GF)
            else:
                df_dic[rest_mech] = ARG()
                df_dic[rest_mech].drug_class = [d_class]
                df_dic[rest_mech].AMR = [AMR_GF]

            i += 1

        return df_dic


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Money can be used for goods and services. Similarly, data can be used for analysis and inspire frustration.")
    parser.add_argument("-in", help="RGI output", required=True, dest="inp")
    parser.add_argument("-out", help="Your output file, directory does need to exist", required=True, dest="outp")
    args = parser.parse_args()
    CARD(args)
