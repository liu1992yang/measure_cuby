# measure_cuby
## After long MD job has done, we use cuby4 framework to count distance pairs of our interest.
Instead of typing the `measure.yaml` manually, this `write_measure.py` take a simple atom-block file 
which contains the atom number and block(residue) info and a standard gjf style file that represent the atom numbering 
order, then generate the `measure.yaml` file and another file `labels_by_block` to be used for grouped contact analysis.
