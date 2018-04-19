#!/usr/bin/env bash

set -eo pipefail

: "${GITHUB_TOKEN:?Need to set GITHUB_TOKEN non-empty}"

build_path="/build/$(date +%s)"
mkdir -p $build_path

cd $build_path
git init
git pull "https://mstewa34:${GITHUB_TOKEN}@github.com/mstewa34/resume.git"

pdflatex -jobname=resume       resume.tex
pdflatex -jobname=resume_print resume.tex
chmod 666 resume*.pdf
mv resume*.pdf /out/
