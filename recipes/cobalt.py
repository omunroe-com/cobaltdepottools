# Copyright 2014 The Chromium Authors. All rights reserved.
# Use of this source code is governed by a BSD-style license that can be
# found in the LICENSE file.

import sys

import recipe_util  # pylint: disable=F0401


# This class doesn't need an __init__ method, so we disable the warning
# pylint: disable=W0232
class Cobalt(recipe_util.Recipe):
  """Basic Recipe class for Cobalt."""

  @staticmethod
  def fetch_spec(props):
    branch = 'COBALT'
    if props.get('branch'):
      branch = props['branch']
    ref = 'remotes/origin/%s' % branch

    url = 'https://lbshell-internal.googlesource.com/chromium.git@%s' % ref
    solution = { 'name'   :'src',
                 'url'    : url,
                 'deps_file': 'DEPS',
                 'managed'   : True,
                 'custom_deps': {},
                 'safesync_url': '',
    }
    spec = {
      'solutions': [solution],
    }
    checkout_type = 'gclient_git'
    spec_type = '%s_spec' % checkout_type
    return {
      'type': checkout_type,
      spec_type: spec,
    }

  @staticmethod
  def expected_root(_props):
    return 'src'


def main(argv=None):
  return Cobalt().handle_args(argv)


if __name__ == '__main__':
  sys.exit(main(sys.argv))
