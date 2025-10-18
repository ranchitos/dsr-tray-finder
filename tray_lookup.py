import csv
import re # regular expressions

def load_tray_data(filename):
    """
    Load tray data from CSV file and return as a list of dictionaries
    """
    data = []
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            data.append(row)
    return data

def parse_room(room):
    """
    Splits room into (prefix letters, number, suffix).
    Examples:
    'E206A' -> ('E', 206, 'A')
    '203' -> ('', 203, '')
    'A101-1' -> ('A', 101, '-1')
    """
    match = re.match(r'([A-Za-z]*)(\d+)([A-Za-z0-9-]*)', room)
    if match:
        prefix, number, suffix = match.groups()
        prefix = prefix.upper()
        suffix = suffix.upper()

        # case where suffix has hyphen followed by digit
        if suffix.startswith('-') and suffix[1:].isdigit():
            suffix = int(suffix[1:]) # remove the hyphen

        return prefix, int(number), suffix
    return '', 0, ''  # default if no match

def room_in_range(room, start, end):
    """
    Check if a room is within the range defined by start and end rooms.
    """
    room_prefix, room_number, room_suffix = parse_room(room)
    start_prefix, start_number, start_suffix = parse_room(start)
    end_prefix, end_number, end_suffix = parse_room(end)

    # compare tuples: (prefix, number, suffix)
    if (room_prefix, room_number, room_suffix) < (start_prefix, start_number, start_suffix):
        return False
    if (room_prefix, room_number, room_suffix) > (end_prefix, end_number, end_suffix):
        return False
    return True


def get_tray(hall, room, data):
    """
    Given a hall and room, return the corresponding tray from the data
    """
    for entry in data:
        # check hall first
        if entry['hall'].lower() == hall.lower():
            
            # check if room is within range
            if room_in_range(room, entry['room_start'], entry['room_end']):
                return entry['tray']
    return None

def main():
    data = load_tray_data('tray_data.csv')

    hall = input('Enter hall name (e.g. Cedar) or enter "quit" to quit the program: ')
    while hall.lower() != 'quit':
        room = input('Enter room (e.g. E410, 205, A110-1): ')

        tray = get_tray(hall, room, data)

        if tray:
            print(f'Room {room} in {hall} belongs to Tray {tray}')
        else:
            print('No matching tray found')
        
        hall = input('Enter hall name or enter "quit" to quit the program: ')

if __name__ == '__main__':
    main()