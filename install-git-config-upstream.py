"""For each repo in DEPS, git config an appropriate depot-tools.upstream.

This will allow git new-branch to set the correct tracking branch.
"""
import argparse
import hashlib
import json
import os
import sys
import textwrap

import gclient_utils
import git_common


def _GclientEntriesToString(entries):
  entries_str = json.dumps(entries, sort_keys=True)
  return entries_str


def ConfigUpstream(repo_dir, url):
  """Determine the upstream branch for this repo, and run git config."""

  if not os.path.exists(repo_dir):
    sys.stderr.write('%s not found\n' % repo_dir)
    return False

  os.chdir(repo_dir)
  unused_url, revision = gclient_utils.SplitUrlRevision(url)
  if revision.find('remotes/origin') != -1:
    upstream = revision
  else:
    # Ignore e.g. a pinned sha1, or other unusual remote.
    sys.stderr.write('Skipping %s with upstream %s\n' % (repo_dir, revision))
    return True

  # Check git's current upstream config, if any.
  current_upstream = git_common.root()
  if current_upstream:
    current_upstream = current_upstream.strip()
  if current_upstream != upstream:
    sys.stdout.write(
        'In %s, setting %s to %s\n' %
        (repo_dir, 'depot-tools.upstream', upstream))
    git_common.set_config('depot-tools.upstream', upstream)
  return True


def Main(args):
  """For each repo in the gclient root, set the upstream config."""

  parser = argparse.ArgumentParser(
      formatter_class=argparse.RawDescriptionHelpFormatter,
      description=textwrap.dedent(__doc__))

  parser.add_argument('-f', '--force', required=False, action='store_true',
                      help='Force the script to run, ignoring cached results.')
  options = parser.parse_args(args)

  # We expect this to be run as a hook in the gclient root directory.
  root_dir, gclient_entries = gclient_utils.GetGClientRootAndEntries()

  # Compute a hash combined of the .gclient_entries and this script.
  # We should re-run if either changes.
  md5 = hashlib.md5()
  md5.update(_GclientEntriesToString(gclient_entries))
  with open(__file__) as f:
    md5.update(f.read())
  current_hash = md5.hexdigest()

  already_processed_hash = None
  entries_hash_file = os.path.join(root_dir, '.git_config_entries_hash')
  if os.path.exists(entries_hash_file):
    with open(entries_hash_file) as f:
      already_processed_hash = f.readlines()[0]

  if current_hash == already_processed_hash and not options.force:
    return 0

  results = []
  for dirname in sorted(gclient_entries):
    abs_path = os.path.normpath(os.path.join(root_dir, dirname))
    results.append(ConfigUpstream(abs_path, gclient_entries[dirname]))

  if all(results):
    # Success. Write the new hash to the cached location.
    with open(entries_hash_file, 'wb') as f:
      f.write(current_hash)
    return 0
  else:
    return 1


if __name__ == '__main__':
  sys.exit(Main(sys.argv[1:]))
