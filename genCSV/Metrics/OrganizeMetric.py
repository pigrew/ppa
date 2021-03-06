__author__ = 'tjstickx'


class OrganizeMetric:
    def __init__(self, metrics, test_case, tool):
        self.metrics = metrics
        self.new_metrics = []
        self.test_case = test_case
        self.tool = tool
        self.metric_name = 0

    @staticmethod
    def get_default_metrics():
        import json
        import FindFile
        config_file = FindFile.return_config_name()
        # Open the JSON file and get the default list of metrics
        with open(config_file, 'r') as f:
            json_data = json.load(f)
            # gets the line_keywords from the JSON file
            default_metric_names = json_data['default_list_of_metrics']
        return default_metric_names

    def create_list_of_metric_names(self):
        import re
        metric_names = []
        # Add each metric name that was captured from parsing the files to the list metric_names
        for metric_pair in self.metrics:
            # Because metric_pair is a list that might have different lengths we use range(len(metric_pair))
            # in the following for loop
            if metric_pair[self.metric_name] not in metric_names:
                time_in_metric = re.search(r'time', metric_pair[self.metric_name], re.I)
                if time_in_metric:
                    self.new_metrics.append((re.sub('Time|time', 'TIME', metric_pair[self.metric_name]), metric_pair[1]))
                    metric_names.append((re.sub('Time|time', 'TIME', metric_pair[self.metric_name])))
                else:
                    self.new_metrics.append(metric_pair)
                    metric_names.append(metric_pair[self.metric_name])
            else:
                print("DUPLICATE METRIC FOUND %s \n" %(metric_pair,))
        return metric_names

    # This method is used to add the metrics that don't appear after parsing the required files
    def add_missing_metrics_old(self):
        new_metrics_collections = []
        default_metric_names = self.get_default_metrics()
        metric_names = self.create_list_of_metric_names()
        self.metrics = self.new_metrics

        for default_metric_name in default_metric_names:
            if default_metric_name not in metric_names:
                # "" is the default value for blank metrics
                new_metric = (default_metric_name, "")
                new_metrics_collections.append(new_metric)

        self.metrics.extend(new_metrics_collections)
        temp_metric_collections = self.sort_metrics()
        return temp_metric_collections

    def sort_metrics(self):
        from operator import itemgetter
        temp_metric_collections, syn, apr, calibre, drc, pv_max, pv_min, pv_power, pv_noise, sta, kit = [], [], [], [], [], [], [], [], [], [], []
        metrics = filter(None, self.metrics)

        # This loop is to arrange the files in the correct order
        for metric_pair in metrics:

            if "syn" in metric_pair[self.metric_name]:
                syn.append(metric_pair)
            elif "apr" in metric_pair[self.metric_name]:
                apr.append(metric_pair)
            elif "calibre" in metric_pair[self.metric_name]:
                calibre.append(metric_pair)
            elif "drc" in metric_pair[self.metric_name]:
                drc.append(metric_pair)
            elif "pv_max" in metric_pair[self.metric_name]:
                pv_max.append(metric_pair)
            elif "pv_min" in metric_pair[self.metric_name]:
                pv_min.append(metric_pair)
            elif "pv_power" in metric_pair[self.metric_name]:
                pv_power.append(metric_pair)
            elif "pv_noise" in metric_pair[self.metric_name]:
                pv_noise.append(metric_pair)
            elif "sta" in metric_pair[self.metric_name]:
                sta.append(metric_pair)
            elif "Kit" in metric_pair[self.metric_name] and len(kit) == 0:
                kit.append(metric_pair)

        temp_metric_collections.extend(self.add_testcase_defaults() + kit + sorted(syn, key=itemgetter(0)) +
                                   sorted(apr, key=itemgetter(0)) + sorted(drc, key=itemgetter(0)) +
                                   sorted(calibre, key=itemgetter(0)) + sorted(pv_max, key=itemgetter(0)) +
                                   sorted(pv_min, key=itemgetter(0)) + sorted(pv_power, key=itemgetter(0)) +
                                   sorted(pv_noise, key=itemgetter(0)) + sorted(sta, key=itemgetter(0)))

        return temp_metric_collections

    def add_testcase_defaults(self):
        import os
        from datetime import datetime

        # If the file name given ends with a '/' or a '\' then os.path.basename() would return "" therefore we do the
        # following "if" statements when gathering the test case name
        if os.path.basename(self.test_case) != "":
            test_case_name = os.path.basename(self.test_case)
        else:
            test_case_name = os.path.basename(os.path.dirname(self.test_case))

        testcase_defaults = [("Test_case_name", test_case_name), ("Test_case_path", self.test_case),
                             ("Test_case_creation_date", self.add_directory_date()), ("DateTIME", str(datetime.now())),
                             ("Tool", self.tool), ("Dot", self.add_dot_metric())]

        return testcase_defaults

    def add_directory_date(self):
        import os
        import datetime
        datetime.datetime.fromtimestamp(os.path.getctime(self.test_case))
        creation_time = os.path.getctime(self.test_case)
        return str(datetime.datetime.fromtimestamp(creation_time))

    def add_dot_metric(self):
        import re
        dot_metric = re.search(r'/(dot[\d]+)/', self.test_case)
        if dot_metric:
            return str(dot_metric.group(1))
        return ""

    @staticmethod
    def get_test_case_number(test_case_number=[0]):
        test_case_number[0] += 1
        return test_case_number[0]
