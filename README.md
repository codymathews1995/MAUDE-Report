# MAUDE Report

## Introduction

This program utilizes data from the Manufacturer and User Facility Device Experience (MAUDE) Database through the openFDA API to generate insightful reports.

⚠ WARNING: This is a work in progress and is not yet complete.

## Features

- **User-Friendly Interface**: Simple form for entering product code and date range.
- **Data Fetching**: Retrieves device event data from the FDA's openFDA API.
- **Database Storage**: Saves fetched data into a SQLite database.
- **Results Display**: Presents the fetched data in a clean, organized table.
- **Reports Generation**: Offers insights into event counts and product problems.
- **Responsive Design**: Works seamlessly on both desktop and mobile devices.

## Technologies Used

- **Frontend**: HTML, CSS (with a dark theme)
- **Backend**: Python, Flask
- **Database**: SQLite
- **API**: openFDA API for device event data
- **Containerization**: Docker

## Getting Started

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed on your machine.
- Basic understanding of Python and Flask is beneficial.

### Installation

1. **Clone the repository**:

   ```bash
   git clone https://github.com/yourusername/fda-device-event-fetcher.git
   cd fda-device-event-fetcher
   ```

2. **Build and run the Docker container**:

    ```bash
    docker-compose up --build
    ```

3. **Access the application**:

Open your web browser and navigate to `http://localhost:5000`

## Usage

1. Enter the Product Code for the device you're interested in.
2. Select the Start Date and End Date for your search.
3. Click the Fetch Data button.
4. View the results displayed in a table format. You can also access reports for additional insights.

## API Details

This application interacts with the openFDA API. For more information on the API endpoints and data structure, visit openFDA.

## Contributions

Contributions are welcome! If you would like to contribute to this project, please fork the repository and create a pull request with your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

Thanks to the openFDA API for providing accessible device event data and Flask community for their extensive documentation and resources.