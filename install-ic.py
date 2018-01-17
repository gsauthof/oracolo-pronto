#!/usr/bin/env python3

# install-ic - automatically install, fix and set-up the Oracle Instant client
#              under Linux
#
# 2018, Georg Sauthoff <mail@gms.tf>
#
# SPDX-License-Identifier: GPL-3.0-or-later

import argparse
import glob
import hashlib
import logging
import os
import subprocess
import sys
import zipfile

cnf = { 
        'version':    '12.2.0.1.0',
        'files': [
                ( 'instantclient-basic-linux.x64-{}.zip',
                  '5015e3c9fba84e009f7519893f798a1622c37d1ae2c55104ff502c52a0fe5194' ),
                ( 'instantclient-jdbc-linux.x64-{}.zip',
                  '1a18fcaa41984bc0499a3d3138843292550a5606556217adb47ddc59caa7a0fa' ),
                ( 'instantclient-precomp-linux.x64-{}.zip',
                  'c4822b95f70d2bab5eb3ef2111e6fedc2c3112d5c514ac5ec3804a6dbaf46176' ),
                ( 'instantclient-sdk-linux.x64-{}.zip',
                  '7f404c3573c062ce487a51ac4cfe650c878d7edf8e73b364ec852645ed1098cb' ),
                ( 'instantclient-sqlplus-linux.x64-{}.zip',
                  'd49b2bd97376591ca07e7a836278933c3f251875c215044feac73ba9f451dfc2' ),
                ( 'instantclient-tools-linux.x64-{}.zip',
                  '9c5674a89bb4aad619fe0691a06d8984e5c0d450f2b895db975302dddc15e215' ),
        ]
}

log = logging.getLogger(__name__)

def mk_arg_parser():
    p = argparse.ArgumentParser(
                formatter_class=argparse.RawDescriptionHelpFormatter,
                description='Install and fix the Oracle Instant Client',
                epilog='2018, Georg Sauthoff <mail@gms.tf>, GPLv3+')
    p.add_argument('--dest', '-d', metavar='DIR',
            help='destination (default: /opt/instantclient$short_version')
    p.add_argument('--source', '-s', metavar='DIR', default='.',
            help='download directory of all the instantclient archives (default: .)')
    p.add_argument('--version', '-v', default='12.2.0.1.0',
            help='oracle version (default: 12.2.0.1.0)')
    p.add_argument('--short', default='_12_2',
            help='Short version (default: _12_2)')
    p.add_argument('--insecure', action='store_true',
            help="don't verify file checksums")
    p.add_argument('--dry', '-n', action='store_true',
            help='Dry run, just print commands')
    p.add_argument('--tnsnames',
            help='tnsnames.ora to install')
    return p

def parse_args(*a):
    arg_parser = mk_arg_parser()
    args = arg_parser.parse_args(*a)
    return args

def quote_arg(x):
    def need_quotes(x):
        meta_char = [ '|', '&', ';', '(', ')', '<', '>', ' ', '\t' ]
        other = [ "'", '"', '`', '$' ]
        for c in meta_char + other:
            if c in x:
                return True
        return False
    if need_quotes(x):
        r = x.replace("'", """'"'"'""")
        return "'" + r + "'"
    return x

dry_flag = False

def run(*a):
    cmd = ' '.join(map(quote_arg, a))
    if dry_flag:
        print(cmd)
    else:
        log.info(cmd)
        p = subprocess.run(a, check=True, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                universal_newlines=True)
     

def file_hash(filename):
    h = hashlib.sha256()
    with open(filename, 'rb', buffering=0) as f:
        for b in iter(lambda : f.read(128*1024), b''):
            h.update(b)
    return h.hexdigest()

def which(cmd):
    ps = os.environ['PATH']
    for p in ps.split(':'):
        f = p + '/' + cmd
        if os.path.exists(f):
            return f
    raise LookupError('{} not found in PATH'.format(cmd))

def check_cmds():
    log.debug('Checking for patchelf command etc.')
    for cmd, msg in [('patchelf', 'try e.g. dnf install patchelf'), ('cksum', 'part of coreutils') ]:
        try:
            which(cmd)
        except LookupError as e:
            log.error('{} - hint: {}'.format(e, msg))

def mk_dest(args):
    run('mkdir', '-p', args.dest)

def set_defaults(args):
    if not args.dest:
        args.dest = '/opt/instantclient' + args.short

def check_files(args, cnf):
    if args.insecure:
        return
    for filename, checksum in cnf['files']:
        filename = args.source + '/' + filename.format(cnf['version'])
        h = file_hash(filename)
        if h != checksum:
            raise RuntimeError(
                    'Checksum mismatch: sha256({}) != {}'.format(
                        filename, checksum))


def zip_top_dir(filename):
    with zipfile.ZipFile(filename) as f:
        ls = f.namelist()
        t = ls[0]
        b = t[:t.find('/')]
        if not b:
            raise RuntimeError('zip base dir is empty')
        return b

def zip_libs(filename):
    with zipfile.ZipFile(filename) as f:
        libs = []
        ls = f.namelist()
        for l in ls:
            t = l[l.find('/')+1:]
            if '/' not in t and '.so' in t:
                libs.append(t)
        return libs

def extract_archives(args, cnf):
    top = zip_top_dir(args.source + '/'
            + cnf['files'][0][0].format(cnf['version']))
    args.libs = []
    for filename, _ in cnf['files']:
        filename = args.source + '/' + filename.format(cnf['version'])
        run('unzip', '-d', args.dest, filename)
        args.libs += zip_libs(filename)
    run('find', args.dest + '/' + top, '-mindepth', '1', '-maxdepth', '1',
            '-exec', 'mv', '-t', args.dest, '{}', '+')
    run('rmdir', args.dest + '/' + top)

def set_rpath(filename, rpath):
    run('chmod', 'u+w', filename)
    run('patchelf', '--set-rpath', rpath, filename)

def fix_rpath(args):
    path = args.dest
    set_rpath(path + '/sqlplus', '$ORIGIN')
    set_rpath(path + '/sdk/proc', '$ORIGIN/..')
    for f in args.libs:
        f = args.dest + '/' + f
        if not args.dry and os.path.islink(f):
            continue
        if args.dry:
            o = 'not found'
        else:
          o = subprocess.check_output(['ldd', f], universal_newlines=True)
        if 'not found' in o:
            set_rpath(f, '$ORIGIN')

def mk_lib_links(args):
    run('mkdir', args.dest + '/lib')
    for f in args.libs:
        link = args.dest + '/lib/' + f
        run('ln', '-s', '../' + f, link)
    libclntsh = 'libclntsh.so'
    if libclntsh not in args.libs:
        target = [ x for x in args.libs if libclntsh in x ][0]
        run('ln', '-s', target, args.dest + '/lib/' + libclntsh)
        run('ln', '-s', target, args.dest + '/' + libclntsh)

def mk_bin_links(args):
    run('mkdir', args.dest + '/bin')
    run('ln', '-s', '../sqlplus', args.dest + '/bin/sqlplus')
    run('ln', '-s', '../sdk/proc', args.dest + '/bin/proc')

# for compatibility with the non-instant-client
def mk_include_link(args):
    run('ln', '-s', '../sdk/include', args.dest + '/precomp/public')

def gcc_sys_path(cc):
    o = subprocess.run(['cc', '-v', '-c', '-E', '-'],
            check=True,
            stdin =subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE, universal_newlines=True)
    ls = o.stderr.splitlines()
    i = ls.index('#include <...> search starts here:')
    j = ls.index('End of search list.')
    return [ x.strip() for x in ls[i:j] ]

# cf. https://stackoverflow.com/questions/325826/oracle-10-2-proc-precompiler-not-reading-header-file/16324902#16324902
def rewrite_proc_cfg(args):
    gcc = [ x for x in gcc_sys_path('cc') if 'gcc' in x][0]
    sys_include = 'sys_include=($ORACLE_HOME/sdk/include,/usr/include,{},/usr/include/linux)'.format(gcc)

    run('cp', args.dest + '/precomp/admin/pcscfg.cfg', args.dest + '/precomp/admin/pcscfg.cfg.bak')
    run('sed', '-i', 's@^sys_include=.*$@{}@'.format(sys_include),
            args.dest + '/precomp/admin/pcscfg.cfg')

def install_tnsnames(args):
    run('mkdir', '-p', args.dest + '/network/admin')
    if not args.tnsnames:
        return
    run('cp', args.tnsnames, args.dest + '/network/admin/tnsnames.ora')

def print_hints(args):
    run('echo', 'add this to your profile: export ORACLE_HOME={0}; export PATH=$ORACLE_HOME/bin:$PATH'.format(args.dest))

def main(*a):
    args = parse_args(*a)
    global dry_flag
    dry_flag = args.dry
    set_defaults(args)
    check_cmds()
    check_files(args, cnf)
    mk_dest(args)
    extract_archives(args, cnf)
    fix_rpath(args)
    mk_lib_links(args)
    mk_bin_links(args)
    mk_include_link(args)
    rewrite_proc_cfg(args)
    install_tnsnames(args)
    print_hints(args)

if __name__ == '__main__':
    log_format            = '%(asctime)s - %(levelname)-8s - %(message)s'
    log_date_format = '%Y-%m-%d %H:%M:%S'
    logging.basicConfig(format=log_format, datefmt=log_date_format,
            level=logging.DEBUG) # or: loggin.INFO
    try:
        sys.exit(main())
    except subprocess.CalledProcessError as e:
        log.error(str(e) + '\nStdout: ' + e.stdout + '\nStderr: ' + e.stderr)
        sys.exit(1)
    except RuntimeError as e:
        log.error(e)
        sys.exit(1)

