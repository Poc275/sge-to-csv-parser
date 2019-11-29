import os
import csv

folder = "C:\\Users\\peter\\Documents\\Coding\\Amygda\\Smartavia Data\\fwdcfm56data"
delimiter = '#'

def split_headers(headers: list):
    final_headers = []
    headers_str = ''.join(headers)
    headers_split = headers_str.split(delimiter)
    # remove data type (?) headers
    for header in headers_split:
        if(len(header) == 1):
            continue
        else:
            final_headers.append(header)

    return final_headers


def split_values(values: list):
    values_str = ''.join(values)
    # remove the trailing hash if present as this will 
    # add an extra empty element when we split
    if(values_str.endswith('#')):
        values_str = values_str[:-1]

    return values_str.split(delimiter)


def output_csv(headers: list, values: list, path: str):
    output = False
    if(len(headers) == len(values)):
        with open(path, 'w', newline='') as output_csv_file:
            wr = csv.writer(output_csv_file, quoting=csv.QUOTE_ALL)
            wr.writerow(headers)
            wr.writerow(values)
            output = True
    else:
        print("{0} column/value mis-match, not parsed".format(path))

    return output


for file_path in os.listdir(folder):
    headers = []
    values = []
    parse_headers = False
    parse_values = False

    if(file_path.endswith('.sge')):
        with open(os.path.join(folder, file_path)) as f:
            for line in f:
                if(line == '\n'):
                    continue
                else:
                    if(line.startswith('*FORMAT')):
                        # beginning of headers
                        parse_headers = True

                    elif(line.startswith('*VALUES')):
                        # beginning of values
                        parse_values = True
                        parse_headers = False

                    else:
                        if(parse_headers):
                            headers.append(line.replace('\n', ''))

                        if(parse_values):
                            values.append(line.replace('\n', ''))

        col_headers = split_headers(headers)
        values = split_values(values)
        output = output_csv(col_headers, values, os.path.join(folder, file_path).replace('.sge', '.csv'))
        if(output):
            print("Parsed {0} successfully".format(file_path))
        else:
            print("{0} failed to parse".format(file_path))
