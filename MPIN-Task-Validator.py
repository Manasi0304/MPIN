class MPINValidator:
    def __init__(self):
        # Common 4-digit MPINs
        self.common_4digit_pins = {
            '0000', '1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888', '9999',
            '1234', '4321', '1212', '2121', '1122', '2211', '1221', '2112', '0123', '3210',
            '1357', '2468', '0246', '1359', '1470', '2580', '3690', '1379', '2468', '0852',
            '1230', '0123', '9876', '6789', '0987', '7890', '0909', '1010', '2020', '3030',
            '1313', '2424', '5678', '4567', '3456', '2345', '7654', '6543', '5432', '4321'
        }
        
        # Common 6-digit MPINs
        self.common_6digit_pins = {
            '000000', '111111', '222222', '333333', '444444', '555555', '666666', '777777', '888888', '999999',
            '123456', '654321', '112233', '332211', '121212', '212121', '123123', '321321', '010101', '101010',
            '123321', '456789', '987654', '135790', '097531', '246810', '018246', '012345', '543210', '567890',
            '098765', '121314', '141312', '151617', '171615', '192021', '212019', '147258', '258147', '369258',
            '258369', '159357', '753951', '963852', '258963', '741852', '852741', '142536', '635241', '142857'
        }
    
    def _extract_demographic_patterns(self, dob_self=None, dob_spouse=None, anniversary=None):
        """Extract possible patterns from user demographics"""
        patterns = set()
        
        dates = {
            "DEMOGRAPHIC_DOB_SELF": dob_self,
            "DEMOGRAPHIC_DOB_SPOUSE": dob_spouse,
            "DEMOGRAPHIC_ANNIVERSARY": anniversary
        }
        
        for key, date_str in dates.items():
            if not date_str:
                continue
                
            try:
                day, month, year = date_str.split('-')
                day = day.zfill(2)
                month = month.zfill(2)
                year = year
                
                # 4-digit patterns
                patterns.add((day + month, key))
                patterns.add((month + day, key)) 
                patterns.add((day + year[-2:], key))
                patterns.add((month + year[-2:], key))
                patterns.add((year[-2:] + day, key))
                patterns.add((year[-2:] + month, key))
                
                # 6-digit patterns
                patterns.add((day + month + year[-2:], key))
                patterns.add((month + day + year[-2:], key))
                patterns.add((year[-2:] + month + day, key))
                patterns.add((year[-2:] + day + month, key))
                patterns.add((day + year[-4:], key))
                patterns.add((month + year[-4:], key))
                
            except ValueError:
                continue
                
        return patterns
    
    def validate_mpin(self, mpin, dob_self=None, dob_spouse=None, anniversary=None):
        """
        Args:
            mpin (str): The MPIN to validate
            dob_self (str, optional): Date of birth of the user (DD-MM-YYYY)
            dob_spouse (str, optional): Date of birth of spouse (DD-MM-YYYY)
            anniversary (str, optional): Wedding anniversary (DD-MM-YYYY)
            
        Returns:
            dict: A dictionary containing 'strength' and 'reasons'
        """

        mpin = str(mpin)
        reasons = []
        
        if len(mpin) == 4:
            common_pins = self.common_4digit_pins
        elif len(mpin) == 6:
            common_pins = self.common_6digit_pins
        else:
            return {"strength": "INVALID", "reasons": ["INVALID_LENGTH"]}
        
        if mpin in common_pins:
            reasons.append("COMMONLY_USED")
            
        demo_patterns = self._extract_demographic_patterns(dob_self, dob_spouse, anniversary)
        
        for pattern, reason in demo_patterns:
            if len(pattern) == len(mpin) and mpin == pattern:
                reasons.append(reason)
        
        strength = "WEAK" if reasons else "STRONG"
        
        return {
            "strength": strength,
            "reasons": reasons
        }


# Test cases for the MPINValidator
def run_tests():
    validator = MPINValidator()
    test_cases = [
        # Test case 1: Common 4-digit PIN
        {
            "input": {"mpin": "1111"},
            "expected": {"strength": "WEAK", "reasons": ["COMMONLY_USED"]}
        },
        # Test case 2: Strong 4-digit PIN
        {
            "input": {"mpin": "7913"},
            "expected": {"strength": "STRONG", "reasons": []}
        },
        # Test case 3: Common 6-digit PIN
        {
            "input": {"mpin": "123456"},
            "expected": {"strength": "WEAK", "reasons": ["COMMONLY_USED"]}
        },
        # Test case 4: Strong 6-digit PIN
        {
            "input": {"mpin": "791345"},
            "expected": {"strength": "STRONG", "reasons": []}
        },
        # Test case 5: DOB-based 4-digit PIN (DDMM)
        {
            "input": {"mpin": "0201", "dob_self": "02-01-1998"},
            "expected": {"strength": "WEAK", "reasons": ["DEMOGRAPHIC_DOB_SELF"]}
        },
        # Test case 6: DOB-based 4-digit PIN (MMDD)
        {
            "input": {"mpin": "0102", "dob_self": "02-01-1998"},
            "expected": {"strength": "WEAK", "reasons": ["DEMOGRAPHIC_DOB_SELF"]}
        },
        # Test case 7: DOB-based 4-digit PIN (YYMM)
        {
            "input": {"mpin": "9801", "dob_self": "02-01-1998"},
            "expected": {"strength": "WEAK", "reasons": ["DEMOGRAPHIC_DOB_SELF"]}
        },
        # Test case 8: DOB-based 4-digit PIN (YYDD)
        {
            "input": {"mpin": "9802", "dob_self": "02-01-1998"},
            "expected": {"strength": "WEAK", "reasons": ["DEMOGRAPHIC_DOB_SELF"]}
        },
        # Test case 9: Spouse DOB-based PIN
        {
            "input": {"mpin": "1205", "dob_spouse": "12-05-1997"},
            "expected": {"strength": "WEAK", "reasons": ["DEMOGRAPHIC_DOB_SPOUSE"]}
        },
        # Test case 10: Anniversary-based PIN
        {
            "input": {"mpin": "2506", "anniversary": "25-06-2020"},
            "expected": {"strength": "WEAK", "reasons": ["DEMOGRAPHIC_ANNIVERSARY"]}
        },
        # Test case 11: Both common and DOB-based
        {
            "input": {"mpin": "1234", "dob_self": "12-03-1994"},
            "expected": {"strength": "WEAK", "reasons": ["COMMONLY_USED"]}
        },
        # Test case 12: Multiple demographic reasons
        {
            "input": {"mpin": "1010", "dob_self": "10-10-1990", "anniversary": "10-10-2010"},
            "expected": {"strength": "WEAK", "reasons": ["COMMONLY_USED", "DEMOGRAPHIC_DOB_SELF", "DEMOGRAPHIC_ANNIVERSARY"]}
        },
        # Test case 13: 6-digit DOB-based PIN (DDMMYY)
        {
            "input": {"mpin": "020198", "dob_self": "02-01-1998"},
            "expected": {"strength": "WEAK", "reasons": ["DEMOGRAPHIC_DOB_SELF"]}
        },
        # Test case 14: 6-digit Anniversary-based PIN (YYMMDD)
        {
            "input": {"mpin": "200625", "anniversary": "25-06-2020"},
            "expected": {"strength": "WEAK", "reasons": ["DEMOGRAPHIC_ANNIVERSARY"]}
        },
        # Test case 15: Strong PIN with demographics present
        {
            "input": {"mpin": "8426", "dob_self": "02-01-1998", "dob_spouse": "12-05-1997", "anniversary": "25-06-2020"},
            "expected": {"strength": "STRONG", "reasons": []}
        },
        # Test case 16: Invalid length PIN
        {
            "input": {"mpin": "123"},
            "expected": {"strength": "INVALID", "reasons": ["INVALID_LENGTH"]}
        },
        # Test case 17: 6-digit strong PIN with demographics
        {
            "input": {"mpin": "947362", "dob_self": "02-01-1998", "anniversary": "25-06-2020"},
            "expected": {"strength": "STRONG", "reasons": []}
        },
        # Test case 18: Common 6-digit pattern
        {
            "input": {"mpin": "121212"},
            "expected": {"strength": "WEAK", "reasons": ["COMMONLY_USED"]}
        },
        # Test case 19: 6-digit PIN using spouse's DOB (DDMMYY)
        {
            "input": {"mpin": "120597", "dob_spouse": "12-05-1997"},
            "expected": {"strength": "WEAK", "reasons": ["DEMOGRAPHIC_DOB_SPOUSE"]}
        },
        # Test case 20: 4-digit PIN with consecutive numbers but not in common list
        {
            "input": {"mpin": "2345"},
            "expected": {"strength": "WEAK", "reasons": ["COMMONLY_USED"]}
        }
    ]
    
    results = []
    for i, test in enumerate(test_cases, 1):
        input_data = test["input"]
        mpin = input_data.pop("mpin")
        result = validator.validate_mpin(mpin, **input_data)
        expected = test["expected"]
        
        passed = result["strength"] == expected["strength"] and set(result["reasons"]) == set(expected["reasons"])
        status = "PASS" if passed else "FAIL"
        
        results.append({
            "test_case": i,
            "input": test["input"],
            "expected": expected,
            "actual": result,
            "status": status
        })
    
    # Print test results
    passed = sum(1 for r in results if r["status"] == "PASS")
    print(f"Test Results: {passed}/{len(test_cases)} passed")
    
    for result in results:
        if result["status"] == "FAIL":
            print(f"\nTest Case #{result['test_case']} FAILED")
            print(f"Input: {result['input']}")
            print(f"Expected: {result['expected']}")
            print(f"Actual: {result['actual']}")
    
    return results


if __name__ == "__main__":
    
    validator = MPINValidator()
    
    result_a = validator.validate_mpin("1234")
    print("Result of Common 4-digit MPIN:", result_a)
    
    result_b = validator.validate_mpin("0201", dob_self="02-01-1998")
    print("Result of MPIN with demographics:", result_b)
    
    result_c = validator.validate_mpin("0201", dob_self="02-01-1998", dob_spouse="12-05-1997", anniversary="25-06-2020")
    print("Result of MPIN with all demographics:", result_c)
    
    result_d = validator.validate_mpin("020198", dob_self="02-01-1998")
    print("Result of 6-digit MPIN:", result_d)
    
    # Test cases
    print("\nRunning test cases...")
    run_tests()