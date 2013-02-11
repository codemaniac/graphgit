#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import git
import networkx as nx
import constants

def main(argv):  
  # obtain git repo URL
  repo_url = argv[1]  
  # repo name
  repo_name = repo_url[repo_url.rfind('/'):repo_url.rfind('.git')]
  # local repo clone location
  repo_loc = '%s%s' % (constants.REPO_DOWNLOAD_LOCATION, repo_name)  
  # initialize repo
  repo = None
  gitt = git.Git()
  try:
    # check if repo is already cloned
    # if local repo exists, assign
    repo = git.Repo(repo_loc, odbt=git.GitCmdObjectDB)    
    # TODO: check if repo is dirty and if so, update
  except git.exc.NoSuchPathError:
    # local repo doesn't exist. clone
    try:
      gitt.clone(repo_url, repo_loc)
      repo = git.Repo(repo_loc, odbt=git.GitCmdObjectDB)
    except:
      sys.exit(1)
    
  if repo is None:
    sys.exit(1)

  # create a graph for the repo
  G = nx.Graph()

  print repo.branches

if __name__ == "__main__":
  main(sys.argv)
