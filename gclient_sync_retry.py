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
  command = [
      ('gclient' if os.name != 'nt' else 'gclient.bat'),
      'sync',
      '--verbose',
      # Calls git reset --hard HEAD on each
      # repository
      '--reset',
      # Force update even for unchanged
      # repositories
      '--force'
  ]

  print command

  max_runs = 3
  fail_string = 'Failed to connect'
  os.environ['GIT_CURL_VERBOSE'] = '1'
  for run in range(1, max_runs + 1):
    sys.stdout.write('Attempt %d\n' % run)
    p = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        stdin=subprocess.PIPE)
    p_stdout, p_stderr = p.communicate('')
    sys.stdout.write(p_stdout)
    sys.stderr.write(p_stderr)
    if run < max_runs and (fail_string in p_stderr or fail_string in p_stdout):
      sys.stdout.write('Retrying gclient sync\n')
      time.sleep(5 * random.randint(0, 2**run - 1))
      continue
    break


if __name__ == '__main__':
  sys.exit(main())
