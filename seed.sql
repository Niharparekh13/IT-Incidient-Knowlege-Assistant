INSERT INTO categories (name, description) VALUES
('Login and Account Access', 'Problems related to passwords, locked accounts, and sign-in errors.'),
('Network and Wi-Fi', 'Problems connecting to campus, office, or home networks.'),
('Software Installation', 'Problems installing, updating, or launching required software.'),
('Email and Communication', 'Problems with email, Teams, notifications, or shared mailboxes.'),
('Device and Hardware', 'Problems with laptops, printers, displays, and peripherals.');

INSERT INTO knowledge_base (category_id, title, symptoms, resolution_steps, escalation_required) VALUES
(
    1,
    'Locked account after multiple failed login attempts',
    'account locked login failed too many attempts password does not work',
    'Wait 15 minutes and try again. Confirm Caps Lock is off. Reset the password using the official password reset portal. If the account remains locked, create an incident for IT support.',
    1
),
(
    1,
    'Password reset request',
    'forgot password cannot login password expired reset password',
    'Open the password reset portal. Verify your identity using the registered recovery method. Create a new password that meets policy requirements. Sign out and sign in again on all devices.',
    0
),
(
    2,
    'Wi-Fi connected but no internet access',
    'wifi connected no internet network error cannot browse',
    'Forget the Wi-Fi network and reconnect. Restart the device. Confirm airplane mode is off. Try another browser or website. If the issue continues, record the network name and location before escalating.',
    1
),
(
    2,
    'Cannot connect to Wi-Fi',
    'cannot connect wifi wireless network authentication failed',
    'Check that Wi-Fi is enabled. Select the correct network. Re-enter credentials carefully. Restart the device. If using a campus network, confirm the account is active.',
    0
),
(
    3,
    'Software installation permission error',
    'software install permission denied admin rights installer blocked',
    'Confirm the installer came from an approved source. Restart the device and try again. If admin rights are required, submit an incident with the software name, version, and business or course reason.',
    1
),
(
    4,
    'Email not syncing',
    'email not syncing outlook messages missing mail not updating',
    'Check internet connectivity. Restart Outlook or the mail app. Confirm mailbox storage is not full. Remove and re-add the account if needed. Escalate if mail is missing on webmail too.',
    0
),
(
    1,
    'MFA code not received',
    'mfa code not received authentication app text message verification login',
    'Check the authenticator app and confirm the phone has signal. Try resend code once. If the device was changed or lost, create an incident so IT can reset MFA registration.',
    1
),
(
    5,
    'Printer not responding',
    'printer not responding print job stuck queue offline device hardware',
    'Confirm the printer is powered on and connected to the network. Clear stuck print jobs, restart the printer, and try printing a test page. Escalate if multiple users are affected.',
    0
),
(
    5,
    'External monitor not detected',
    'monitor display screen not detected hdmi usb c docking station hardware',
    'Check cable connections and power. Try a different display input. Reconnect the docking station or adapter, then restart the laptop if the display is still not detected.',
    0
),
(
    5,
    'Bluetooth device not connecting',
    'bluetooth not working device pairing headphones mouse keyboard wireless hardware',
    'Turn Bluetooth off and on again. Confirm the device is charged and in pairing mode. Remove the old pairing record, restart the computer, then pair the device again. If multiple Bluetooth devices fail, save an incident for hardware or driver review.',
    0
);
