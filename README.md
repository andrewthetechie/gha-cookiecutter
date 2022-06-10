# Cookiecutter in GHA

[![Action Template](https://img.shields.io/badge/Action%20Template-Python%20Container%20Action-blue.svg?colorA=24292e&colorB=0366d6&style=flat&longCache=true&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA4AAAAOCAYAAAAfSC3RAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAM6wAADOsB5dZE0gAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAAERSURBVCiRhZG/SsMxFEZPfsVJ61jbxaF0cRQRcRJ9hlYn30IHN/+9iquDCOIsblIrOjqKgy5aKoJQj4O3EEtbPwhJbr6Te28CmdSKeqzeqr0YbfVIrTBKakvtOl5dtTkK+v4HfA9PEyBFCY9AGVgCBLaBp1jPAyfAJ/AAdIEG0dNAiyP7+K1qIfMdonZic6+WJoBJvQlvuwDqcXadUuqPA1NKAlexbRTAIMvMOCjTbMwl1LtI/6KWJ5Q6rT6Ht1MA58AX8Apcqqt5r2qhrgAXQC3CZ6i1+KMd9TRu3MvA3aH/fFPnBodb6oe6HM8+lYHrGdRXW8M9bMZtPXUji69lmf5Cmamq7quNLFZXD9Rq7v0Bpc1o/tp0fisAAAAASUVORK5CYII=)](https://github.com/andrewthetechie/gha-cookiecutter)
[![Actions Status](https://github.com/andrewthetechie/gha-cookiecutter/workflows/Lint/badge.svg)](https://github.com/andrewthetechie/gha-cookiecutter/actions)
[![Actions Status](https://github.com/andrewthetechie/gha-cookiecutter/workflows/Integration%20Test/badge.svg)](https://github.com/andrewthetechie/gha-cookiecutter/actions)

<!-- action-docs-description -->

## Usage

Runs cookiecutter on the specified template, passing in the values input as cookiecutterValues.

This action does not commit or push any files, check out an action like [stefanzweifel/git-auto-commit-action](https://github.com/stefanzweifel/git-auto-commit-action) for a way to commit generated files.

### Example workflow

```yaml
name: Run Cookiecutter
on: [workflow_dispatch]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - name: Run Cookiecutter
      uses: andrewthetechie/gha-cookiecutter@main
      with:
        # can be a link to a git repo or a local path
        template: https://github.com/cjolowicz/cookiecutter-hypermodern-python
        cookiecutterValues:
         {
           foo: "bar",
           baz: "boo",
           num: 2
         }
```

Or to use a cookiecutter in a private repo, use a checkout with a token that has access to that repo

```
name: Run Cookiecutter Private
on: [workflow_dispatch]
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
      with:
        repository: "yourprivatecookiecutter"
        token: ${{ secrets.GITHUB_TOKEN }}
    - name: Run Cookiecutter
      uses: andrewthetechie/gha-cookiecutter@main
      with:
        # path to what you checked out
        template: ./yourprivatecookiecutter
        cookiecutterValues:' {
           foo: "bar",
           baz: "boo",
           num: 2
         }
```
<!-- action-docs-inputs -->

<!-- action-docs-outputs -->

<!-- action-docs-runs -->
