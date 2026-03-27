use polars::prelude::*;
use std::fs::File;
use std::io::Write;
use std::path::Path;

fn create_dummy_data() -> Result<(), PolarsError> {
    if !Path::new("loan-recovery.csv").exists() {
        let mut file = File::create("loan-recovery.csv").unwrap();
        file.write_all(b"Loan_ID, Recovery_Amount, Last_Contact_Date\n").unwrap();
        file.write_all(b"LP001,1000,2023-01-15\n").unwrap();
        file.write_all(b"LP002, 2000, 2023-01-16\n").unwrap();
        file.write_all(b"LP003,1500, \n").unwrap();
        file.write_all(b"LP001,1000,2023-01-15\n").unwrap(); // duplicate
    }
    Ok(())
}


fn main() -> Result<(), PolarsError> {
    create_dummy_data()?;
    // 1. Load the CSV file into a Polars DataFrame.
    let mut df = CsvReader::from_path("loan-recovery.csv")?
        .finish()?;

    println!("Original DataFrame:\n{}", df);

    // 2. Standardize column names (example: remove whitespace, make lowercase)
    let new_columns: Vec<String> = df.get_column_names().iter()
        .map(|name| name.trim().to_lowercase().replace(" ", "_"))
        .collect();
    let old_columns: Vec<String> = df.get_column_names().iter().map(|s| s.to_string()).collect();
    for (old, new) in old_columns.iter().zip(new_columns.iter()) {
        df.rename(old, new)?;
    }


    // 3. Drop duplicate rows.
    df = df.unique(None, UniqueKeepStrategy::First, None)?;

    // 4. Trim whitespace from string columns
    df = df.lazy().with_column(col("loan_id").str().strip(None)).collect()?;


    // In a real scenario, you would handle missing values, outliers etc.
    // For this example, we'll just show the cleaning up to this point.

    println!("\nCleaned DataFrame:\n{}", df);

    // 5. Write the cleaned DataFrame to a new CSV file.
    let mut file = File::create("cleaned_loan_recovery.csv")?;
    CsvWriter::new(&mut file).finish(&mut df)?;

    Ok(())
}
