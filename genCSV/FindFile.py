def search_dir(test_case, tool):
    import fnmatch
    import os

    file_endings = return_file_endings(tool)
    found_files = []
    included_path_names = [test_case, 'syn', 'apr', 'drc_lvs', 'sta', 'pv', 'runs', 'reports', 'logs',
                           'reports_max', 'reports_min', 'denall_reuse', 'drcc', 'gden', 'HV', 'drc_IPall', 'lvs',
                           'max', 'min', 'power', 'noise', 'drcd', 'trclvs']

    for root, dir_names, file_names in os.walk(test_case, topdown=True):
        # This statement makes sure that we only search for paths that includes the names in the list, included_path_names
        dir_names[:] = [d for d in dir_names if d in included_path_names]

        # Because the files we are searching for in the drc_lvs directory does not follow the patterns that the rest of the files do we have to do the following
        if "drcd" in root or "denall_reuse" in root or "drc_IPall" in root or "trclvs" in root:
            for root_name, directory_names, files in os.walk(root):
                for file_ending in file_endings:
                    # found_files = add_matching_files(files, file_ending, root_name, found_files)
                    for drcd_file in fnmatch.filter(files, file_ending):
                        found_files.append(os.path.join(root_name, drcd_file))

        else:
            for file in file_endings:
                if 'drc.sum' in file:
                    if 'drc_lvs' in root:
                        found_files = add_matching_files(file_names, file, root, found_files)
                elif '*.link.rpt' in file:
                    if 'pv' in root or 'sta' in root:
                        found_files = add_matching_files(file_names, file, root, found_files)
                else:
                    found_files = add_matching_files(file_names, file, root, found_files)

    return found_files


def add_matching_files(file_names, file, root, found_files):
    import os
    import fnmatch
    for filename in fnmatch.filter(file_names, file):
        found_files.append(os.path.join(root, filename))
    return found_files


def return_csv_name():
    import json

    config_file = return_config_name()
    with open(config_file, 'r') as f:
        json_data = json.load(f)
        # finds the default value for the order number to search files in the json file
        csv_location = json_data['Csv_location']

    return csv_location


def return_config_name():
    import sys
    import os
    import genCSV

    # If a config.json file is passed in then the program will use that as the configuration file otherwise we
    # use the one located at the script location
    if genCSV.args.c:
        return genCSV.args.c
    else:
        return os.path.join(sys.path[0], 'config.json')


def return_file_endings(tool):
    import json

    config_file = return_config_name()

    # Finds the file name endings
    with open(config_file, 'r') as f:
        json_data = json.load(f)
        file_endings = json_data['file_endings'][tool]

    # This line gets rid of empty strings just in case one is accidently passed
    file_endings = list(filter(None, file_endings))

    return file_endings
