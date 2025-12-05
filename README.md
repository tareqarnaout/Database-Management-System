# Database Management System (DBMS) Indexing Project

A Python-based database indexing system that demonstrates the performance benefits of different indexing techniques compared to linear file scans. This project implements Primary Index and Clustering Index structures to optimize data retrieval operations.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Indexing Techniques](#indexing-techniques)
- [Performance Benchmarks](#performance-benchmarks)
- [Dataset](#dataset)
- [Team](#team)

## 🎯 Overview

This project was developed as part of a Database Management Systems course to explore and compare various data indexing techniques. The system loads student records from a CSV file and implements different indexing strategies to demonstrate their efficiency in query execution.

The project benchmarks the performance of:
- **File Scan** (Linear Search)
- **Primary Index** (on ID field)
- **Clustering Index** (on Major field)

## ✨ Features

- **Data Loading**: Efficiently loads and processes CSV data containing student records
- **Primary Index**: Binary search-based index on the ID field (primary key)
- **Clustering Index**: Optimized index for queries on the Major field
- **Exact Match Queries**: Support for finding specific records by ID or Major
- **Range Queries**: Efficient range searches on indexed fields
- **Performance Benchmarking**: Built-in timing and block access counting for performance comparison
- **Block-based Storage**: Simulates disk block access with configurable block size

## 📦 Prerequisites

- Python 3.6 or higher
- Standard Python libraries (csv, os, time, math)

## 🚀 Installation

1. Clone the repository:
```bash
git clone https://github.com/tareqarnaout/Database-Management-System.git
cd Database-Management-System
```

2. Ensure the dataset file (`uni.csv`) is in the same directory as the Python script.

3. No additional dependencies are required as the project uses only Python standard libraries.

## 💻 Usage

Run the main script to execute the indexing system and view performance benchmarks:

```bash
python "dbms project.py"
```

The script will:
1. Load 10,000 student records from `uni.csv`
2. Build Primary and Clustering indexes
3. Execute benchmark queries comparing different access methods
4. Display a performance comparison table showing:
   - Query type
   - Search key
   - Access method used
   - Number of disk blocks accessed
   - Execution time in milliseconds

### Sample Output

```
Loaded 10000 records.
Query Type      Key              Method            Blocks  Time (ms)
----------------------------------------------------------------------
Exact by ID     id=5001          File scan         7       0.023003 
Exact by ID     id=5001          Primary index     2       0.008957 
Range by ID     4951..5051       File scan         2       0.019346 
Range by ID     4951..5051       Primary index     3       0.016992 
Exact by Major  major='English'  File scan         100     0.377    
Exact by Major  major='English'  Clustering index  1       0.010
```

## 📁 Project Structure

```
Database-Management-System/
├── dbms project.py    # Main Python script with indexing implementation
├── uni.csv            # Dataset with 10,000 student records
└── README.md          # Project documentation (this file)
```

### Key Components in `dbms project.py`:

- **`load_data()`**: Loads student records from CSV file
- **`PrimaryIndex`**: Implements sparse index on sorted ID field
  - `build()`: Creates the index structure
  - `exact_match()`: Binary search for exact ID match
  - `range_query()`: Retrieves records within an ID range
- **`ClusteringIndex`**: Implements index on Major field with physically clustered data
  - `build()`: Creates the clustering index
  - `exact_match()`: Retrieves all records for a specific major
- **File Scan Functions**: Linear search implementations for comparison
  - `file_exact_search()`: Linear scan for exact matches
  - `file_exact_search_id_first()`: Binary search on sorted file
  - `file_range_search_id()`: Range search on sorted file

## 🔍 Indexing Techniques

### Primary Index
- **Type**: Sparse index on primary key (ID)
- **Structure**: Stores first ID of each block with block number
- **Search Method**: Binary search on index, then linear scan within block
- **Use Case**: Optimal for exact match and range queries on primary key
- **Block Size**: 100 records per block (configurable)

### Clustering Index
- **Type**: Dense index on non-key field (Major)
- **Structure**: Records are physically sorted by Major; index maps each unique major to its starting block
- **Search Method**: Direct block access via index
- **Use Case**: Efficient for queries on the clustering field
- **Advantage**: All records with same major are stored contiguously

## 📊 Performance Benchmarks

The system demonstrates significant performance improvements using indexes:

| Query Type | Access Method | Typical Block Accesses | Performance Gain |
|------------|---------------|------------------------|------------------|
| Exact by ID | File Scan | ~7 blocks | Baseline |
| Exact by ID | Primary Index | ~2 blocks | 3.5x faster |
| Exact by Major | File Scan | 100 blocks | Baseline |
| Exact by Major | Clustering Index | 1 block | 100x faster |

**Key Insights:**
- Primary indexes reduce block access significantly for ID-based queries
- Clustering indexes provide dramatic improvements for queries on the clustering field
- Index overhead is minimal compared to query performance gains

## 📊 Dataset

The project uses `uni.csv`, which contains 10,000 student records with the following schema:

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Unique student identifier (1-10000) |
| name | String | Student name |
| major | String | Academic major (e.g., Computer Science, Engineering, Biology) |

Sample records:
```csv
id,name,major
1,David Andrews,Biology
2,John King,Psychology
3,Juan Davis,Computer Science
```

## 👥 Team

This project was developed as a collaborative team effort for a Database Management Systems course.

## 📝 License

This project is available for educational purposes.

## 🙏 Acknowledgments

- Developed as part of a Database Management Systems (DBMS) course project
- Demonstrates practical implementation of database indexing concepts
- Thanks to all team members who contributed to this project

---

**Note**: This is an educational project designed to demonstrate database indexing concepts and their performance characteristics. The implementation simulates disk block access patterns but operates entirely in memory using Python data structures.
