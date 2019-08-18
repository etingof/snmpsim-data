#
# This file is part of snmpsim-data software.
#
# Copyright (c) 2019, Ilya Etingof <etingof@gmail.com>
# License: https://github.com/etingof/snmpsim-data/LICENSE.rst
#
import argparse
import sys
import os
import json
import logging
try:
    import urllib.request as urllib

except ImportError:
    import urllib2 as urllib

import snmpsim_data
from snmpsim_data import docs

import jinja2

LOG = logging.getLogger(sys.argv[0])


def render(rst_file, tmpl_dir, tmpl_file, **kwargs):
    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(tmpl_dir),
        trim_blocks=True, lstrip_blocks=True)

    tmpl = env.get_template('index.j2')

    text = tmpl.render(**kwargs)

    try:
        os.makedirs(os.path.dirname(rst_file))

    except FileExistsError:
        pass

    with open(rst_file, 'w') as fl:
        fl.write(text)


def prefixes(oid):
    oid = [int(x) for x in oid.split('.') if x != '']

    while oid:
        yield '.'.join(str(x) for x in oid)
        oid.pop(-1)


def main():

    ch = logging.StreamHandler()
    LOG.addHandler(ch)

    parser = argparse.ArgumentParser(
        description='Generate RsT docs out of snmpsim data files')

    parser.add_argument(
        '-v', '--version', action='version', version='%(prog)s ' + snmpsim_data.__version__
    )

    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debugging'
    )

    parser.add_argument(
        '--mib-source',
        metavar='<URI>',
        type=str,
        default='http://mibs.snmplabs.com/asn1',
        help='URI to ASN.1 MIBs collection'
    )

    parser.add_argument(
        '--json-mib-index',
        metavar='<URI>',
        type=str,
        default='http://mibs.snmplabs.com/json/index.json',
        help='URI to MIB index in form of pysmi JSON index'
    )

    parser.add_argument(
        '--data-dir',
        metavar='<PATH>',
        type=str,
        default=os.path.join(os.path.dirname(
            snmpsim_data.__file__), '..', 'data'),
        help='Path to SNMP simulator data dir to read .snmprec files from'
    )

    parser.add_argument(
        '--templates-dir',
        metavar='<PATH>',
        type=str,
        default=os.path.join(
            os.path.dirname(docs.__file__), 'templates'),
        help='Path to Jinja2 templates rendering Sphinx documents'
    )

    parser.add_argument(
        '--rst-dir',
        metavar='<PATH>',
        type=str,
        default=os.path.join(
            os.path.dirname(snmpsim_data.__file__),
            '..', 'docs', 'source', 'data'),
        help='Path to SNMP simulator documentation directory to render '
             'RsT files into'
    )

    args = parser.parse_args()

    if args.debug:
        LOG.setLevel(logging.DEBUG)
        ch.setLevel(logging.DEBUG)

    LOG.debug('fetching MIB index from %s', args.json_mib_index)

#    response = urllib.urlopen(args.json_mib_index)
    mib_index = {'oids': {}, 'identity': {}} #json.load(response)

    LOG.debug('got %d MIB objects from %d MIBs in index', len(mib_index['oids']), len(mib_index['identity']))

    args.data_dir = os.path.abspath(args.data_dir)
    args.rst_dir = os.path.abspath(args.rst_dir)
    args.templates_dir = os.path.abspath(args.templates_dir)

    LOG.debug('reading data files from %s', args.data_dir)

    for cur, _dirs, files in os.walk(args.data_dir):
        sub_dir = cur[len(args.data_dir) + 1:]
        rst_dir = os.path.join(args.rst_dir, sub_dir)

        tmpl_file = os.path.join(args.templates_dir, 'index.j2')

        rst_file = os.path.join(rst_dir, 'index.rst')

        LOG.debug('rendering template %s into %s', tmpl_file, rst_file)

        title = ' '.join(w[0].upper() + w[1:] for w in sub_dir.split(os.path.sep) if w)

        try:
            render(rst_file, args.templates_dir, tmpl_file, title=title)

        except jinja2.exceptions.TemplateError as exc:
            LOG.error('Jinja template %s rendering error: %s', tmpl_file, exc)
            continue

        for snmprec_name in files:
            if not snmprec_name.endswith('.snmprec'):
                continue

            snmprec_file = os.path.join(cur, snmprec_name)
            tmpl_file = os.path.join(args.templates_dir, 'snmprec.j2')
            rst_file = os.path.join(rst_dir, os.path.splitext(snmprec_name)[0], 'index.rst')

            comment = ''

            with open(snmprec_file) as fl:
                for line in fl:
                    if line.startswith('#'):
                        comment += line
                        continue

                    record = line.split('|', 1)

                    if len(record) != 2:
                        LOG.warning('parse error in file %s', snmprec_file)
                        comment = ''
                        continue

                    oid = record[0]

                    for oid_prefix in prefixes(oid):
                        try:
                            mib_names = mib_index['oids'][oid_prefix]
                            break

                        except KeyError:
                            continue

                    else:
                        LOG.error('OID %s of %s does not resolve into any MIB', oid, snmprec_file)
                        continue

                    try:
                        load_mibs(*mib_names)

                    except Exception as exc:
                        LOG.warning('MIBs %s fail to load: %s', mib_names, exc)




            # locate MIB module and compile it into JSON

            # resolve OID into MIB object

            # render RsT for MIB scalar, column, row and table objects



if __name__ == '__main__':
    sys.exit(main())
