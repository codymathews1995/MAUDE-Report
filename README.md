# MAUDE Process

## Introduction

This program is intended to take FDA generated Manufacturer and User Facility
Device Experience (MAUDE) Database CSVs and make helpful reports on the data provided.

## Current Shortcoming

So far, because of how FDA generates this data. The data will need to be fixed in order for processing to occur.
I am working on learning on handling the openFDA API to make this process more automatic.
For now, the following steps will need to occur before processing a .CSV:

## Preliminary Steps

1. Perform a search on MAUDE Database
<https://www.accessdata.fda.gov/scripts/cdrh/cfdocs/cfmaude/search.cfm>

2. When satisfied with search, click on "Export to Excel."

3. Move downloaded file (e.g., maudeExcelReport#.csv) to project folder

4. Open the MAUDE report file in Excel, or whatever program you use for spreadsheets

5. Delete the first empty column in the spreadsheet

6. Scroll all the way down to the bottom of the spreadsheet

7. Delete entire disclaimer. Make sure you don't delete any of the data above it.

The rest of these steps will follow Excel's method of file conversion:

8. File > Export > Change File Type > CSV (Comma delimited) (*.csv) > Save in project folder as "data.csv"

## Run the Program

1. Ensure you have R installed

```r
R --version
```

or

```r
R.exe --version
```

If not, install it here: <https://cloud.r-project.org>

2. Run the program

```r
 rscript maude_report.r
```

## Note

This is an active project and may not work as intended. Any collaboration to improve it is welcomed and appreciated.

## ToDo

[] Create a process to search openFDA from the program

[] Create easier executable

[] To be determined
