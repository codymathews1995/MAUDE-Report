library(dplyr)

# Load data.csv
data <- read.csv("data.csv")

# Declare variables
report_number <- data$Report.Number
manufacturer <- data$Manufacturer
product_code <- data$Product.Code
event_type <- data$Event.Type
brand_name <- data$Brand.Name
device_problem <- sapply(strsplit(data$Device.Problem, ";"), '[',1)

# Combined Data
combined_data <- data.frame(
    Report_Number = report_number,
    Manufacturer = manufacturer,
    Brand_Name = brand_name,
    Product_Code = product_code,
    Event_Type = event_type,
    Device_Problem = device_problem
)

# Event Report
event_report <- combined_data %>%
    group_by(Brand_Name, Event_Type) %>%
    summarise(Event_Count = n(), .groups = 'drop') %>%
    arrange(Brand_Name, Event_Type)

write.csv(event_report, "processed/event_report.csv", row.names = FALSE)


# Device Problem Report
problem_report <- combined_data %>%
    group_by(Brand_Name, Event_Type) %>%
    summarise(Device_Problem = n(), .groups = 'drop') %>%
    arrange(Brand_Name, Event_Type)

write.csv(problem_report, "processed/problem_report.csv", row.names = FALSE)