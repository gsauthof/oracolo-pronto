This repository contains a Python script for automatically
installing and setting up the [Oracle Instant Client][1] under Linux.

Example usage:

    1. [Get the Oracle Instant client][2] `.zip` archive file
    2. Install under `/opt`: `./install-ic.py --dry`

2018, Georg Sauthoff <mail@gms.tf>, [GPLv3+][gpl]

## Features

Since Oracle is unable to publish cryptographically secure
checksums for their downloads (as of early 2018) the script
includes some and validates them before continuing.

Besides the obvious unzipping, the script fixes some issues 
and inconsistencies created by Oracle:

- It fixes the runtime linker path (RPATH) in the executables and shared
  libraries such that there is no need to apply any
  [`LD_LIBRARY_PATH` hacks][3].
- It creates missing symbolic links to shared libraries such that
  basic usage like `-lclntsh` works, as expected.
- It creates subdirectories like `bin`, `lib` and `precomp/public` and
  puts the necessary symbolic links into them such that basic
  user expectations are met and software written for the
  non-instant client doesn't have to change any relative paths.
- A provided `tnsnames.ora` is put into the right path, even when
  some Oracle documentation may confuse the average Oracle DBA.

The resulting installation under - say - `/opt/oracle-12` is
**completely relocatable**. That means that it can be moved around
and copied to another system without the need to change any
files. Only the `ORACLE_HOME` environment variable has to
adjusted, as well.

The script has a dry-mode where all the planned steps are printed
as shell commands to stdout. Thus, alternatively to running the
Python script in non-dry mode one can do something like this:

    $ ./install-ic.py --dry > dry-stdout.sh
    $ bash dry-stdout.sh

This features comes handy for testing and when you want to setup
a remote system that already have the necessary `.zip` files
available but doesn't come with Python 3. It is also convenient
when you work in a very bureaucratic corporation where different
silos are involved in installing a single package (e.g.
'Enterprise Security', 'Enterprise Infrastructure', 'Enterprise
Compliance', ...). In such an environment where some poor Joe
have to create - say - several tickets that have to include in
minute detail each installation step such that even an off-shored
pseudo-admin is able to execute them, the reassuring way out is
to just capture the stdout of a dry-run and copy'n'paste it
into the tickets.

See also `dry-stdout.sh`.

## Requirements

- Python 3
- [PatchELF][4]

[1]: http://www.oracle.com/technetwork/database/features/instant-client/index-097480.html
[2]: http://www.oracle.com/technetwork/topics/linuxx86-64soft-092277.html
[3]: https://gms.tf/ld_library_path-considered-harmful.html
[4]: http://nixos.org/patchelf.html
[gpl]: https://www.gnu.org/licenses/gpl.html
