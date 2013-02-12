#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import logging
import git
import networkx as nx
import constants

def safe_str(obj):
  """ return the byte string representation of obj """
  try:
    return str(obj)
  except UnicodeEncodeError:
    # obj is unicode
    return unicode(obj).encode('unicode_escape')

def graph_repo(repo_url, output_loc):  
  """ generates graphml for a git repository """
  log = logging.getLogger("graphgit")
  # repo name
  repo_name = repo_url[repo_url.rfind('/')+1:repo_url.rfind('.git')]
  log.info ("Processing git repository: %s" % repo_name)
  # local repo clone location
  repo_loc = '%s/%s' % (constants.REPO_DOWNLOAD_LOCATION, repo_name)  
  # initialize repo
  repo = None
  gitt = git.Git()
  try:
    # check if repo is already cloned
    # if local repo exists, assign
    repo = git.Repo(repo_loc, odbt=git.GitCmdObjectDB)    
    log.info( "Repository already cloned... Going ahead and using it..." )
    # TODO: check if repo is dirty and if so, update
  except git.exc.NoSuchPathError:
    # local repo doesn't exist. clone
    try:
      log.info( "Cloning repository... please wait !" )
      gitt.clone(repo_url, repo_loc)
      log.info( "Git clone completed..." )  
      repo = git.Repo(repo_loc, odbt=git.GitCmdObjectDB)
    except:
      sys.exit(1)
    
  if repo is None:
    sys.exit(1)

  # create a graph for the repo
  G = nx.DiGraph()
  # root node
  G.add_node(repo_name, type=constants.NODE_TYPE_VALS['REPOSITORY'])
  # branches & commits
  for branch in repo.branches:
    log.debug ("Processing branch %s" % branch)
    G.add_node(branch, type=constants.NODE_TYPE_VALS['BRANCH'])
    G.add_edge(repo_name, branch, 
      label=constants.EDGE_LABEL_VALS['REPOSITORY_BRANCH'])
    for commit in repo.iter_commits(branch):
      author = safe_str(commit.author)
      ts = commit.committed_date
      message = safe_str(commit.message.strip())      
      sha = str(commit)
      log.debug ("%s> %s --[commit]--> %s" % (branch, author, sha))
      G.add_node(author, type=constants.NODE_TYPE_VALS['PERSON'])
      G.add_node(sha, ts=ts, message=message, 
        type=constants.NODE_TYPE_VALS['COMMIT'])
      G.add_edge(author, sha, label=constants.EDGE_LABEL_VALS['PERSON_COMMIT'])
      G.add_edge(branch, sha, label=constants.EDGE_LABEL_VALS['BRANCH_COMMIT'])

  log.info( "Graph built ! saving..." )

  # save graphml
  output_file_name = '%s.graphml' % repo_name
  output_file_loc = '%s/%s' % (output_loc, output_file_name)
  output_file = open(output_file_loc,'w')
  nx.write_graphml(G, output_file)

  log.info( "Saved to %s !" % output_file_loc )
