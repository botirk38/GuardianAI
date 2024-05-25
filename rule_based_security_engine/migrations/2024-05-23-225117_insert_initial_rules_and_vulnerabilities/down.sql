-- This file should undo anything in `up.sql`

-- Delete vulnerabilities entries
DELETE FROM vulnerabilities WHERE rule_id IN (SELECT id FROM rules WHERE name IN (
    'Reentrancy Attack',
    'Authority Check',
    'Signature Verification',
    'Arithmetic Safety',
    'Frozen Account Modification'
));

-- Delete rules entries
DELETE FROM rules WHERE name IN (
    'Reentrancy Attack',
    'Authority Check',
    'Signature Verification',
    'Arithmetic Safety',
    'Frozen Account Modification'
);

