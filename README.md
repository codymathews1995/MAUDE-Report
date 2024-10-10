# MAUDE Process

## Introduction

This program is intended to utilize data acquired from the Manufacturer and User Facility
Device Experience (MAUDE) Database using the openFDA API to make helpful reports on the data provided.

## Current Shortcoming

So far, this program only takes Product Codes and Start/End Dates for custom search queries.
Working on making this more customizable.

## How to Run

1. Ensure you have R installed

```r
R --version
```

or

```r
R.exe --version
```

If not, install it here: <https://cloud.r-project.org>

2. Start an active R shell

```r
R
```

or

```r
R.exe
```

3. Run the script
```r
source("maude-report.r")
```

## Note

This is an active project and may not work as intended. Any collaboration to improve it is welcomed and appreciated.

## ToDo

[X] Create a process to search openFDA from the program

[] Make the query constructor more diverse, similar to MAUDE Database search

[] Create easier executable

[] To be determined
