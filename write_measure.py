import sys
import numpy as np
import math
import re


def read_c_others(atom_file):
  try:
    with open(atom_file, 'r') as fin:
      raw_input = fin.read().splitlines()
  except FileNotFoundError:
    print('file not found')
  center_number = int(raw_input[0].split(':')[1])
  others = []
  block_pair = {}
  for block in raw_input[1:]:
    block_name = block.split(':')[0]
    block_atoms = list(map(int,block.split(':')[1].split(',')))
    block_pair.setdefault(block_name, list(zip([center_number]*len(block_atoms), block_atoms)))
  return block_pair


def read_atoms(filename):
  '''
  rtype = list[str]
  '''
  with open(filename, 'r') as fin:
    atom_list = []
    atom_num = 1
    for line in fin:
      if line.strip() == '':
        continue
      if line.startswith("  "):
        arr = re.split(" +", line.strip())
        if len(arr) == 4:
          atom = arr[0]
          atom_list.append(atom + str(atom_num))
          atom_num += 1
    return atom_list


def get_name_number(num, atom_list):
  return atom_list[num-1]


def get_pair_names(block_pair,atom_list):
  '''
  rtype = dict
  '''
  pair_dict = {}
  for key, pairs in block_pair.items():
    name_corr_pairs ={tuple(map(lambda x : get_name_number(x, atom_list), pair)): pair for pair in pairs}
    pair_dict.setdefault(key, name_corr_pairs)
  return pair_dict

def write_yaml_label(pair_dict):
  with open('measure.yaml','w') as yaml:
    yaml.write("job: measure\n")
    yaml.write("geometry: trajectory_anneal.xyz\n\n") 
    yaml.write("measurements:\n")
    with open('labels_by_block.txt', 'w') as label:
      for block, vs in pair_dict.items():
        label.write(block + ':')
        label_list = []
        for pair,num in pair_dict[block].items():
          name = '-'.join(pair)
          num_to_write = '; '.join(tuple(map(str, num))) 
          yaml_line = '    {}: distance({})\n'.format(name,num_to_write)
          yaml.write(yaml_line)
          label_list.append(name)
        label.write(','.join(label_list)+ '\n')
        

if __name__ == '__main__' :
  if len(sys.argv) < 3:
    print('usage: python write_measure.py atom_file example_input(gjf style file)')
    sys.exit()
  atom_file = sys.argv[1]
  standard_input = sys.argv[2]
  block_pair= read_c_others(atom_file)
  atom_tp_num = read_atoms(standard_input)
  pair_dict=get_pair_names(block_pair, atom_tp_num)
  write_yaml_label(pair_dict)
  
