class clockTreeRptData:
    def outdata(self, metric_list):
        for metrics in metric_list:
            print(metrics)
class clockTreeRpt:
    def searchfile(file):
        import re
        from Configurations import Configurations
        DataItems = []
        base_path = Configurations().parser_final()
        # Open the file with read only permit
        f = open(file, "r")
        # The variable "lines" is a list containing all lines
        lines = f.readlines()
        f.close()
        rptData = clockTreeRptData()

        for line in lines:
            found_max_globe_skew = re.search(r'(Max[\s]*global[\s]*skew)[\s]*:+[\s]*([\d]+[\.]*[\d]*)+.*', line, re.I)

            if found_max_globe_skew:
                rptData.foundMaxGlobeSkew = "apr_cts_max_global_skew", found_max_globe_skew.group(2)
                DataItems.append(rptData.foundMaxGlobeSkew)

        return ["%s" % i[0] for i in DataItems], ["%s" % i[1] for i in DataItems]
