import os
from glob import glob

###############################################
# Functions
###############################################
def read_csv(file_path):
    with open(file_path, 'r') as file:
        # get all columns in file
        headers = file.readline().strip().split(',')

        # get row values
        data = []
        for line in file:
            row_values = line.strip().split(',')
            row = dict(zip(headers, row_values))
            data.append(row)

        return headers, data


def write_csv(file_path, headers, data):
    with open(file_path, 'a') as file:
        
        # check column exist
        with open(file_path, 'r') as file_reader:
            headers_origin = file_reader.readline().strip().split(',')
        if headers_origin != headers:
            # column not exist --> write headers of file csv
            file.write(','.join(headers) + '\n')
        else:
            # column exist --> pass
            pass

        # write row values
        for row in data:
            file.write(','.join(row.get(header, '') for header in headers) + '\n')


def transform_data(row_values):
    """
        fill in:
            'UTC+0000' if {timezone} column is null
            0 if {created_at} column is null
            'unknown' if {os_name}, {device_type}, {store} and {platform} columns are null
    """
    row_values['{timezone}'] = row_values.get('{timezone}', '') or 'UTC+0000'
    row_values['{created_at}'] = row_values.get('{created_at}', '') or 0

    dict_store = {
        'android': 'google',
        'ios': 'itunes',
        'macos': 'google'
    }
    os_name = row_values.get('{os_name}', '')
    row_values['{store}'] = dict_store.get(os_name, 'unknown')

    if not os_name:
        row_values.update({
            '{os_name}': 'unknown',
            '{device_type}': 'unknown',
            '{store}': 'unknown',
            '{platform}': 'unknown',
        })
    else:
        row_values['{device_type}'] = row_values.get('{device_type}', '') or 'unknown'
        row_values['{platform}'] = row_values.get('{platform}', '') or 'unknown'

    return row_values
###############################################


###############################################
# Main
###############################################
def main():
    merged_path = 'result_merged/merged_data.csv'

    all_columns = ['{created_at}', '{country}', '{os_name}', 
                   '{device_type}', '{random_user_id}', '{store}', 
                   '{timezone}', '{network_type}', '{platform}', 
                   '{region}', '{time_to_reinstall}', '{time_to_uninstall}', 
                   '{is_organic}', '{hardware_name}', '{referral_time}', 
                   '{app_version}', '{time_spent}', '{label}', 
                   '{environment}']

    # loop all file csv in data folder
    all_files = glob(os.path.join('data', "*.csv"))
    for csv_file in all_files:
        print(f"Merging {csv_file.split('/')[-1]}")
        # --------------------------- #
        headers, data = read_csv(csv_file)

        merged_data = []
        for row in data:
            row_values = {col: row.get(col, '') for col in all_columns}
            row_values = transform_data(row_values)
            merged_data.append(row_values)

        write_csv(merged_path, all_columns, merged_data)
        # --------------------------- #
        print('='*100)


###############################################
if __name__ == "__main__":
    main()