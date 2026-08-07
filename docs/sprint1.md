# Sprint 1 - CSV Upload

## Goal
Allow users to upload a CSV file and view its structure.

## User Story

As a user,
I want to upload a CSV file,
So that I can understand its structure before performing any analysis.

## Acceptance Criteria

- User can upload a CSV file.
- The application reads the CSV successfully.
- The system displays:
    - Number of rows
    - Number of columns
    - Column names
    - Data types
    - Missing values
- Invalid file types are rejected with an appropriate error message.

## Technical Tasks

- [ ] Create upload endpoint
- [ ] Read CSV using Pandas
- [ ] Return dataset summary
- [ ] Add error handling
- [ ] Write unit tests