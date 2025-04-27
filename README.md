# MPIN Validator

A robust implementation for validating Mobile PIN (MPIN) strength based on common patterns and user demographics.

## Overview

This project implements an MPIN validation system that evaluates the strength of Mobile PINs used in banking applications. The validator checks if a PIN is easily guessable by considering:

1. Common PIN patterns that are frequently used
2. Demographic information that might be used to create predictable PINs
3. Support for both 4-digit and 6-digit PINs

## Features

- Validates 4-digit and 6-digit MPINs
- Identifies commonly used PIN patterns
- Detects PINs derived from personal demographic information:
  - Date of birth
  - Spouse's date of birth
  - Wedding anniversary
- Provides detailed reasons for PIN weakness
- Includes comprehensive test suite with 20 test cases

## Implementation Details

The system classifies PINs as either "STRONG" or "WEAK" based on predefined criteria. If a PIN is classified as weak, the system provides specific reasons why:

- COMMONLY_USED: PIN is in the list of commonly used PINs
- DEMOGRAPHIC_DOB_SELF: PIN is derived from the user's date of birth
- DEMOGRAPHIC_DOB_SPOUSE: PIN is derived from the spouse's date of birth
- DEMOGRAPHIC_ANNIVERSARY: PIN is derived from the wedding anniversary

## Usage Examples

python
validator = MPINValidator()

# Part A: Check if 4-digit MPIN is commonly used
result_a = validator.validate_mpin("1234")
print("Result of Common 4-digit MPIN:", result_a)

# Part B: Check strength considering demographics
result_b = validator.validate_mpin("0201", dob_self="02-01-1998")
print("Result of MPIN with demographics:", result_b)

# Part C: Enhanced output with specific reasons
result_c = validator.validate_mpin("0201", dob_self="02-01-1998", dob_spouse="12-05-1997", anniversary="25-06-2020")
print("Result of MPIN with all demographics:", result_c)

# Part D: 6-digit PIN
result_d = validator.validate_mpin("020198", dob_self="02-01-1998")
print("Result of 6-digit MPIN:", result_d)

![PART_A-D](https://github.com/user-attachments/assets/8ac2aac8-1184-4f6f-96e3-e9b741793da0)






## Test Results

The implementation includes a comprehensive test suite with 20 test cases covering different scenarios:

- Common and uncommon 4-digit PINs
- Common and uncommon 6-digit PINs
- PINs derived from user demographics in various formats
- PINs that match multiple weakness criteria
- PINs with invalid length
- Various combinations of inputs

All test cases pass successfully:

![Test Results]

![image](https://github.com/user-attachments/assets/6a49a42b-ef4b-4af0-b6f1-ec3525a013b6)

## Project Structure

- mpin_validator.py: Main implementation of the MPINValidator class
- test_mpin_validator.py: Test suite for the MPINValidator
- images/: Directory containing screenshots of usage examples and test results

## How It Works

1. The validator maintains a database of common 4-digit and 6-digit PINs.
2. When validating a PIN, it first checks if the PIN is in the list of common PINs.
3. If demographic information is provided, it generates various patterns from these dates.
4. It then checks if the PIN matches any of these patterns.
5. Based on these checks, it determines the strength of the PIN and provides reasons if it's weak.

## Requirements

- Python 3.6+

## Installation

bash
git clone https://github.com/Manasi0304/MPIN-validator.git
cd mpin-validator

## About

This project was developed as part of an assignment for OneBanc Technologies Pvt. Ltd. It addresses the security concern of easily guessable MPINs in mobile banking applications.
