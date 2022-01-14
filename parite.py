# Calculation of parite within a set of MPs

#! /usr/bin/env python3
# coding: utf-8

import argparse
import re
import logging as lg
import analysis.csv as c_an
import analysis.xml as x_an

# Function to collect arguments
def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--datafile",help="""CSV file containing pieces of
                        information about the members of parliament""")
    parser.add_argument("-s","--searchname",help="""Informations relative to a
                        named MP""")
    parser.add_argument("-g","--groupfirst",help="""Classement des n plus
                        grands partis""")
    parser.add_argument("-i","--info", action='store_true', help="""information
                        about the file""")
    parser.add_argument("-p","--byparty", action='store_true', help="""displays
                        a graph for each political party""")
    return parser.parse_args()

# Main function
def main():
    args = parse_arguments()
    try:
        datafile = args.datafile
        if datafile is None:
            raise Warning('You must indicate a valid datafile!')
        regext = re.search(r'^.+\.(\D{3})$', args.datafile)
        extension = regext.group(1)
        if extension == 'xml':
            x_an.launch_analysis(datafile)
        elif extension == 'csv':
            c_an.launch_analysis(datafile, args.info, args.byparty,
                                    args.searchname, args.groupfirst)
        else:
            raise Warning('You must indicate a valid datafile!')
    except Warning as er_file:
        lg.warning(er_file)
    finally:
        print('#################### Analysis is over ######################')

if __name__ == '__main__':
    main()
    