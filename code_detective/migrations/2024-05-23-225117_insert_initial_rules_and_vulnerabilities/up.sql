-- Insert Rules
INSERT INTO rules (name, description) VALUES
('Reentrancy Attack', 'Ensure state changes happen before external calls to prevent reentrancy attacks.'),
('Authority Check', 'Ensure all sensitive functions check for the correct authority.'),
('Signature Verification', 'Ensure all transactions properly verify signatures to prevent unauthorized actions.'),
('Arithmetic Safety', 'Check arithmetic operations for overflows and underflows using safe math practices.'),
('Frozen Account Modification', 'Prevent modifications to accounts that are marked as frozen.');


-- Insert Vulnerabilities with rule_id fetched dynamically from rules table
INSERT INTO vulnerabilities (rule_id, name, description, severity) VALUES
((SELECT id FROM rules WHERE name = 'Reentrancy Attack'), 'Potential Reentrancy Attack', 'State changes must precede external calls to prevent reentrancy.', 'High'),
((SELECT id FROM rules WHERE name = 'Authority Check'), 'Missing Authority Check', 'Sensitive functions missing authority verification.', 'Critical'),
((SELECT id FROM rules WHERE name = 'Signature Verification'), 'Signature Verification Missing', 'Transactions lacking proper signature verification.', 'High'),
((SELECT id FROM rules WHERE name = 'Arithmetic Safety'), 'Arithmetic Overflow or Underflow', 'Arithmetic operations without safe math checks.', 'Medium'),
((SELECT id FROM rules WHERE name = 'Frozen Account Modification'), 'Frozen Account Modification Attempt', 'Modification attempt on frozen account detected.', 'High');

