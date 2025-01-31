def parse_disk_map(disk_map):
    lengths = [int(char) for char in disk_map]
    return lengths

def build_initial_representation(lengths):
    representation = []
    file_id = 0
    
    for length in lengths:
        # Add file blocks
        representation.extend([str(file_id)] * length)
        file_id += 1
        
        # Add free space (if there's another length)
        if lengths:
            representation.append('.')
    
    # Remove the last added free space (not needed)
    if representation and representation[-1] == '.':
        representation.pop()
    
    return ''.join(representation)

def compact_files(representation):
    # Create a list to hold the compacted representation
    new_representation = list(representation.replace('.', ''))
    
    # Add back the free spaces
    free_space_count = representation.count('.')
    new_representation.extend(['.'] * free_space_count)
    
    return ''.join(new_representation)

def calculate_checksum(representation):
    checksum = 0
    for index, char in enumerate(representation):
        if char != '.':
            file_id = int(char)
            checksum += index * file_id
    return checksum

def main(disk_map):
    lengths = parse_disk_map(disk_map)
    initial_representation = build_initial_representation(lengths)
    compacted_representation = compact_files(initial_representation)
    checksum = calculate_checksum(compacted_representation)
    return checksum

# Example disk map
disk_map = "2333133121414131402"
resulting_checksum = main(disk_map)
print(f"The resulting filesystem checksum is: {resulting_checksum}")