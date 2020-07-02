from pathlib import Path
import re

'''
replace tile size (or other parameter) in Geoserver xml files
'''


def change_pattern_in_file(filename, key, pattern, new_value):
    # I could use proper read/write xml, but it seems like an overkill
    print(filename)
    filename = Path(filename).resolve()
    if not filename.exists():
        raise Exception('filename {} does not exist'.format(filename))
    my_file = open(str(filename), "r")
    lines_of_file = my_file.readlines()
    my_line_i = None
    for i, line in enumerate(lines_of_file):
        stripped = line.strip()
        if stripped == key:
            my_line_i = i+1
            break
    if my_line_i:
        my_line = lines_of_file[my_line_i]
        new_line = pattern.sub(new_value, my_line)
        lines_of_file[my_line_i] = new_line
        if new_line == new_line:
            print('pattern was not replaced!')
            return False
    else:
        print('key not found')
        return False
    my_file = open(str(filename), "w")
    my_file.writelines(lines_of_file)
    return True


def change_pattern_glob(root: Path, file_pattern: str, **kwargs):
    for filename in root.glob(file_pattern):
        change_pattern_in_file(filename=filename, **kwargs)


# <coverage>
# ...
#   <parameters>
# ...
#     <entry>
#       <string>SUGGESTED_TILE_SIZE</string>
#       <string>512,512</string>
#     </entry>
# ...
#   </parameters>
# ...
# </coverage>


def geoserver_tilesize_change(data_dir, workspace):
    key = '<string>SUGGESTED_TILE_SIZE</string>'
    pattern = r'<string>{}</string>'
    p = re.compile(pattern.format('.*'))
    # new_value = r'<string>256,256</string>'
    new_value = pattern.format('256,256')
    root = Path(data_dir) / 'workspaces' / workspace
    file_pattern = '**/**/coverage.xml'

    change_pattern_glob(root=root, file_pattern=file_pattern, key=key, pattern=p, new_value=new_value)


if __name__ == '__main__':
    geoserver_tilesize_change(data_dir=r'd:\geoserver-2.17.1-bin\data_dir', workspace='omni')



