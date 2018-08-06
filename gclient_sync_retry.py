# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Gclient sync, retry if failed to connect."""

import os
import random
import subprocess
import sys
import time


def main():
  gclient_str = ('gclient' if os.name != 'nt' else 'gclient.bat')
  sync_command = [
      gclient_str,
      'sync',
      '--verbose',
      # Calls git reset --hard HEAD on each
      # repository
      '--reset',
      # Force update even for unchanged
      # repositories
      '--force'
  ]

  revert_command = [
      gclient_str,
      'revert',
      '--verbose',
  ]

  print sync_command

  max_runs = 6
  os.environ['GIT_CURL_VERBOSE'] = '1'

  # Run sync_command. If it fails, rerun with exponential backoff.
  # Return 0 if it runs successfully, 1 if all retries fail.
  for run in range(1, max_runs + 1):
    sys.stdout.write('Attempt %d\n' % run)
    p = subprocess.Popen(
        sync_command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE)
    p_stdout, p_stderr = p.communicate()
    sys.stdout.write(p_stdout)
    sys.stderr.write(p_stderr)

    if p.returncode == 0:
      return 0

    if run == 1:
      sys.stdout.write("Reverting uncommitted changes with:\n  " \
                       + ' '.join(revert_command) + '\n')
      p = subprocess.Popen(revert_command,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           stdin=subprocess.PIPE)
      p_stdout, p_stderr = p.communicate()
      sys.stdout.write(p_stdout)
      sys.stderr.write(p_stderr)

    if run < max_runs:
      sys.stdout.write('Sync failed. Retrying.\n')
      time.sleep(2**(run - 1) + 2 * random.random())

  sys.stdout.write('Permanent gclient sync failure.\n')
  return 1


if __name__ == '__main__':
  sys.exit(main())
