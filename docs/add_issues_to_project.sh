#!/usr/bin/env bash
# Adds all open issues from PerformanceAssistant repo to GitHub Project #3
# Usage: bash docs/add_issues_to_project.sh

REPO="sergsol/PerformanceAssistant"
PROJECT_NUMBER=3
OWNER="sergsol"

echo "Fetching all open issues..."
ISSUES=$(gh issue list --repo $REPO --state open --limit 100 --json url --jq '.[].url')

echo "Adding issues to project $PROJECT_NUMBER..."
for url in $ISSUES; do
  gh project item-add $PROJECT_NUMBER --owner $OWNER --url "$url"
  echo "  Added: $url"
done

echo ""
echo "Done! View your project at: https://github.com/users/sergsol/projects/3"
