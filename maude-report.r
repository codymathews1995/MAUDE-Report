library(httr)
library(jsonlite)
library(dplyr)

# Take User Input
product_code_input <- readline(prompt = "Enter the Product Code:")
start_date_input <- readline(prompt = "Start Date [YYYY-MM-DD]:")
end_date_input <- readline(prompt = "End Date [YYYY-MM-DD]:")

# Construct Query
product_code <- paste("device.device_report_product_code.exact:", product_code_input, sep="")
date_received <- paste("date_received:[",start_date_input,"+TO+",end_date_input,"]", sep="")
separator <- "+AND+"
limit <- "&limit=500"  # Increased limit to get more data

base_endpoint <- "https://api.fda.gov/device/event.json?search="
field_term <- paste(date_received, separator, product_code, sep = "")
query <- paste0(base_endpoint, field_term, limit)

# Fetch Data from OpenFDA
response <- GET(query)

if (http_status(response)$category == "Success") {
    # Parse JSON response
    data <- fromJSON(content(response, "text"), flatten = TRUE)$results
    
    if (length(data) == 0) {
        stop("No results found.")
    }

    # Function to Extract Nested Data
    safe_extract <- function(data, column) {
        if (column %in% names(data)) {
            return(data[[column]])
        } else if (grepl("\\.", column)) {
            # Handle nested columns
            parts <- strsplit(column, "\\.")[[1]]
            if (all(parts %in% names(data))) {
                return(data[[parts[1]]][[parts[2]]])
            }
        }
        return(rep(NA, nrow(data)))
    }

    # Extract Brand Name
    extract_brand_name <- function(device_list) {
        sapply(device_list, function(device) {
            if (is.data.frame(device) && "brand_name" %in% names(device)) {
                return(device$brand_name[1])
            } else {
                return(NA)
            }
        })
    }

    # Create Resultant Data Frame 
    combined_data <- data.frame(
        Report_Number = safe_extract(data, "report_number"),
        Brand_Name = extract_brand_name(data$device),
        Event_Type = I(safe_extract(data, "event_type")),
        Product_Problems = I(safe_extract(data, "product_problems")),
        stringsAsFactors = FALSE
    )

    # Function to unnest list columns
    unnest_column <- function(df, col) {
        unnested <- lapply(df[[col]], function(x) if(length(x) == 0) NA else paste(x, collapse = "; "))
        df[[col]] <- unlist(unnested)
        return(df)
    }

    # Unnest Event_Type and Product_Problems columns
    combined_data <- unnest_column(combined_data, "Event_Type")
    combined_data <- unnest_column(combined_data, "Product_Problems")

    # Brand Name and Event Type Report
    event_report <- combined_data %>%
        group_by(Brand_Name, Event_Type) %>%
        summarise(Event_Count = n(), .groups = 'drop') %>%
        arrange(Brand_Name, desc(Event_Count))

    # Brand Name and Product Problems Report
    problem_report <- combined_data %>%
        group_by(Brand_Name, Product_Problems) %>%
        summarise(Problem_Count = n(), .groups = 'drop') %>%
        arrange(Brand_Name, desc(Problem_Count))

    # Write CSV files
    tryCatch({
        write.csv(event_report, "processed/event_type_report.csv", row.names = FALSE)
        cat("Brand Name and Event Type Report generated: event_type_report.csv\n")
    }, error = function(e) {
        cat("Error writing event_type_report.csv:", conditionMessage(e), "\n")
    })

    tryCatch({
        write.csv(problem_report, "processed/product_problems_report.csv", row.names = FALSE)
        cat("Brand Name and Product Problems Report generated: product_problems_report.csv\n")
    }, error = function(e) {
        cat("Error writing product_problems_report.csv:", conditionMessage(e), "\n")
    })

} else {
    stop("Failed to retrieve data: ", http_status(response)$message)
}