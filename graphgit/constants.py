#!/usr/bin/env python
# -*- coding: utf-8 -*-

REPO_DOWNLOAD_LOCATION = '/tmp/graphgit/repos'

# node types
NODE_TYPE_VALS = dict(REPOSITORY='repository',
  BRANCH='branch',
  PERSON='person',
  COMMIT='commit')

# edge labels
EDGE_LABEL_VALS = dict(REPOSITORY_BRANCH='branch',
  PERSON_COMMIT='commit',
  BRANCH_COMMIT='hasCommit')
