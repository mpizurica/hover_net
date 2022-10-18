# Running hovernet model and analyzing cell types in tiles

Steps to run this code:
    1. gather tiles for which you want a HoverNet analysis in a folder ``input_dir``
    2. run ``run_tile.sbatch``, and make sure to set ``--input_dir`` and ``--output_dir``
    3. the code will generate the output in ``output_dir``, specifically a folder will be created for every tile in ``--input_dir`` which contains subfolders ``json`` (containing detected cells and their class) and ``overlay`` (an image where the detected cells are encircled in a color corresponding to their class, where the color is defined based on the json in the ``--type_info_path``)
        ! if you do not want the ``overlay`` images to be written (takes up a lot of space, and if you won't use it it's better not to create it), then comment the line ``cv2.imwrite(save_path, cv2.cvtColor(overlaid_img, cv2.COLOR_RGB2BGR))`` in ``infer.tile.py``

Steps to analyze the fraction of cell types in every tile (i.e. processing the generated ``.json`` files)
    - ``get_counts.py`` will generate a ``.txt`` file that contains the detected cell types per tile (columns: tile_name, no_label, tumor, lymphocytes, connective, dead, normal)
    - if you want to create boxplots/violinplots that contain statistics across several tiles, see code in ``get_boxplot.py`` and ``get_violinplot.py``

    