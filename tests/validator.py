#!/usr/bin/env python3
"""Simple unit test for .asf.yaml"""
import os
import sys
sys.path.extend(
    (
        "./",
        "../",
    )
)
# If run locally inside the tests dir, we'll move one dir up for imports
if "tests" in os.getcwd():
    os.chdir("..")
import pytest
import asfyaml.asfyaml
import asfyaml.dataobjects

# Rewire the notifications path, so we can test with a mock json file
import asfyaml.feature.notifications
asfyaml.feature.notifications.VALID_LISTS_FILE = "tests/mailinglists.json"

# Set .asf.yaml to debug mode
asfyaml.DEBUG = True


def test_basic_yaml():
    expected_envs = {"production", "quietmode"}  # We expect these two envs enabled
    expected_minimum_features = {"test"}
    repo_path = "./repos/private/whimsy/whimsy-private.git"
    os.environ["PATH_INFO"] = "whimsy-site.git/git-receive-pack"
    os.environ["GIT_PROJECT_ROOT"] = "./repos/private"
    if not os.path.isdir(repo_path):  # Make test repo dir
        os.makedirs(repo_path, exist_ok=True)
    basic_yaml = open("tests/basic-dev-env.yaml", "r").read()
    testrepo = asfyaml.dataobjects.Repository(repo_path)
    a = asfyaml.asfyaml.ASFYamlInstance(testrepo, "humbedooh", basic_yaml)
    a.run_parts()



    # We should have both prod+dev envs enabled here
    assert a.environments_enabled == expected_envs
    # We should have at least our 'test' feature in the set
    assert expected_minimum_features.issubset(a.enabled_features.keys())

    # The repo should be marked as private by asfyaml
    assert testrepo.is_private is True, "Expected testrepo.private to be True, but wasn't!"

    # Assert that we know the project name and the hostname
    assert testrepo.project == "whimsy", f"Expected project name whimsy, but got {testrepo.project}"
    assert testrepo.hostname == "whimsical", f"Expected project hostname whimsical, but got {testrepo.hostname}"

