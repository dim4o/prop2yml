# .properties to .yml converter

Converting files by hand is boring. This tool helps to to migrate from `.properties` to `.yml` files and and vice versa.

## Table of Contents

1. [Python guide](#python-guide)
2. [Java guide (COMING SOON)](#java-guide)


## Python guide
1. `.properties` to `.yml`:

    To convert `.properties` file to `.yml` file run:

    `python prop2yml.py <source_file_path.properties> <destination_path.yml>`

    If the destination path is not specified the converted file will be saved in the current working directory with name: `<source_file_name>.yml`. 
2. `.yml` to `.prop`: (COMING SOON)  
    To convert `.yml` file to `.properties` file run:

    `python yml2prop.py <source_file_path.yml> <destination_path.properties>`

    If the destination path is not specified the converted file will be saved in the current working directory with name: `<source_file_name>.properties`. 
## Java guide